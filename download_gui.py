import tkinter as tk
from tkcalendar import DateEntry
import ee
import geetools
import os
from datetime import datetime, timedelta

service_account = 'earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com'
service_file = os.path.join(os.getcwd(), 'shared', 'service_account_file.json')

try:
  credentials = ee.ServiceAccountCredentials(service_account, service_file)
  ee.Initialize(credentials)
  philippines = ee.Geometry.Polygon(
    [[[116.71687839753203, 18.744929081691417],
      [116.71687839753203, 5.019622515938524],
      [126.91219089753203, 5.019622515938524],
      [126.91219089753203, 18.744929081691417]]], None, False)

  ncr = ee.Geometry.Polygon(
    [[[120.86737688113851, 14.816322084944211],
      [120.86737688113851, 14.31656392558974],
      [121.16400774051351, 14.31656392558974],
      [121.16400774051351, 14.816322084944211]]], None, False)
  
  ncr_box = ee.Geometry.Polygon(
    [[[120.88626682729029, 14.33788811927746],
      [121.15543186635279, 14.33788811927746],
      [121.15543186635279, 14.792458281417941],
      [120.88626682729029, 14.792458281417941],
      [120.88626682729029, 14.33788811927746]]], None, False)
  
  service_accountok = 1
except:
  service_accountok = 0

now = datetime.now()
weekago = now - timedelta(days = 7)

window = tk.Tk()
window.title('Downloader GUI')
window.geometry('500x300')
window.resizable(False, False)

satelliteLabel = tk.Label(window, text = 'Satellite Image')

dropdownValue = tk.StringVar(window)
dropdownValue.set('Select Satellite Image to Download')
options = ['ERA5',
           'Landsat 8',
           'MODIS AODB',
           'MODIS AODG',
           'Sentinel 5P NO2',
           'Sentinel 5P SO2']

satelliteDropdown = tk.OptionMenu(window, dropdownValue, *options)
satelliteDropdown.config(width = 56)

sDateLabel = tk.Label(window, text = 'Start Date')

startDate = DateEntry(window, selectmode = 'day',
                     year = weekago.year,
                     month = weekago.month,
                     day = weekago.day)

eDateLabel = tk.Label(window, text = 'End Date')

endDate = DateEntry(window, selectmode = 'day',
                     year = now.year,
                     month = now.month,
                     day = now.day)

#       ERA5 Downloader       #
def downloadERA5(start, end):
  era5 = ee.ImageCollection('ECMWF/ERA5/DAILY').select(
    'mean_2m_air_temperature',
    'total_precipitation',
    'u_component_of_wind_10m',
    'v_component_of_wind_10m'
    ).filterBounds(philippines).filter(ee.Filter.date(start, end))
  
  extra = dict(sat="ERA5")
  geetools.batch.Export.imagecollection.toDrive(
    collection=era5,
    folder='ERA5',
    region=philippines,
    namePattern='{sat}_{system_date}',
    scale=31000,
    datePattern='yMMdd',
    extra=extra,
    verbose=False,
  )

#       L8 Downloader       #
def maskL8sr(image):
    cloud_shadow_bit_mask = (1 << 4)
    clouds_bit_mask = (1 << 3)
    qa = image.select('QA_PIXEL')
    mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) and (qa.bitwiseAnd(clouds_bit_mask).eq(0))
    return image.updateMask(mask)

def downloadL8(start, end):
  ls08 = ee.ImageCollection('LANDSAT/LC08/C02/T1_L2'
    ).filter(ee.Filter.eq('WRS_PATH', 116)
    ).filter(ee.Filter.eq('WRS_ROW', 50)
    ).filterBounds(ncr
    ).filterDate(start, end
    ).filterMetadata('CLOUD_COVER', 'less_than', 70
    ).map(maskL8sr)
  
  geetools.batch.Export.imagecollection.toDrive(
    collection=ls08,
    folder='LANDSAT8',
    region=ncr_box,
    scale=30,
    namePattern='LS08_{system_date}',
    datePattern='yMMdd',
    verbose=False
    )
  
#       Modis Downloader       #
def downloadMODIS(start, end, band):
  if band == 'blue':
    collection = ee.ImageCollection('MODIS/061/MCD19A2_GRANULES'
      ).filter(ee.Filter.stringContains('system:index', 'h29v07')
      ).select('Optical_Depth_047')
    fn = 'MODIS_AODB'
  elif band == 'green':
    collection = ee.ImageCollection('MODIS/061/MCD19A2_GRANULES'
      ).filter(ee.Filter.stringContains('system:index', 'h29v07')
      ).select('Optical_Depth_055')
    fn = 'MODIS_AODG'

  startDate = ee.Date(start)
  endDate = ee.Date(end)

  nDays = ee.Number(endDate.difference(startDate, 'day')).round()
  daysList = ee.List.sequence(0, nDays)

  def getDailyAve(n):
    ini = startDate.advance(n, 'day')
    end = ini.advance(1, 'day')
    datared = collection.filterDate(ini, end).mean()
    day = ini.get("day")
    month = ini.get("month")
    year = ini.get("year")

    day = ee.String(ini.get("day"))
    month = ee.String(ini.get("month"))
    year = ee.String(ini.get("year"))
    
    sysIndexinfo = ee.String(f"{fn}_{str(startDate)}_{str(endDate)}")
    return datared.set('year', year).set('month', month).set('day', day).set('system:time_start', ini.millis()).set("system:index", sysIndexinfo)

  dailyAve_Listversion = daysList.map(getDailyAve)
  dailyAve_Colversion = ee.ImageCollection(dailyAve_Listversion)

  geetools.batch.Export.imagecollection.toDrive(
    collection=dailyAve_Colversion,
    namePattern=f'{fn}_''{system_date}',
    folder=f'{fn}',
    region=ncr_box,
    scale=1000,
    verbose=False,
  )

#       Sentinel5P Downloader       #
def downloadS5P(start, end, pol):
  collection = ee.ImageCollection(f'COPERNICUS/S5P/NRTI/L3_{pol}').select(f'{pol}_column_number_density').filterBounds(ncr).filterDate(start, end)
  
  geetools.batch.Export.imagecollection.toDrive(
    collection=collection,
    namePattern=f'S5P_{pol}''_{system_date}',
    folder=f'S5P_NO2',
    region=ncr_box,
    verbose=False
  )

def run():
  sat = dropdownValue.get()
  sDate = startDate.get_date()
  eDate = endDate.get_date()

  if (eDate - sDate) <= timedelta(days = 0):
    console_text.insert(tk.END, 'Check Start and End Dates\n')
    console_text.see('end')
    return

  try:
    if sat == 'Select Satellite Image to Download':
      console_text.insert(tk.END, 'Check Satellite\n')
      console_text.see('end')
      return
    elif sat == 'ERA5':
      downloadERA5(str(sDate), str(eDate))
      console_text.insert(tk.END, 'ERA5 Processing DONE\nFrom {} to {}\n'.format(str(sDate),str(eDate)))
      console_text.see('end')
    elif sat == 'Landsat 8':
      downloadL8(str(sDate), str(eDate))
      console_text.insert(tk.END, 'Landsat 8 Processing DONE\nFrom {} to {}\n'.format(str(sDate),str(eDate)))
      console_text.see('end')
    elif sat == 'MODIS AODB':
      downloadMODIS(str(sDate), str(eDate), 'blue')
      console_text.insert(tk.END, 'MODIS AODB Processing DONE\nFrom {} to {}\n'.format(str(sDate),str(eDate)))
      console_text.see('end')
    elif sat == 'MODIS AODG':
      downloadMODIS(str(sDate), str(eDate), 'green')
      console_text.insert(tk.END, 'MODIS AODG Processing DONE\nFrom {} to {}\n'.format(str(sDate),str(eDate)))
      console_text.see('end')
    elif sat == 'Sentinel 5P NO2':
      downloadS5P(str(sDate), str(eDate), 'NO2')
      console_text.insert(tk.END, 'Sentinel5P NO2 Processing DONE\nFrom {} to {}\n'.format(str(sDate),str(eDate)))
      console_text.see('end')
    elif sat == 'Sentinel 5P SO2':
      downloadS5P(str(sDate), str(eDate), 'SO2')
      console_text.insert(tk.END, 'Sentinel5P SO2 Processing DONE\nFrom {} to {}\n'.format(str(sDate),str(eDate)))
      console_text.see('end')
  except:
    console_text.insert(tk.END, 'Download Error\n')
    console_text.see('end')


console_text = tk.Text(window,
                       width = 59,
                       height = 8,
                       bd = 3)
runButton = tk.Button(text = 'Run',
                    command = run)

#packing widgets

row1 = 25
row2 = 60
row3 = 95
row4 = 120
row5 = 275

satelliteLabel.place(x = 10, y = row1, anchor = 'w')
satelliteDropdown.place(x = 100, y = row1, relwidth = 0.7, anchor = 'w')

sDateLabel.place(x = 10, y = row2, anchor = 'w')
startDate.place(x = 105, y = row2, anchor = 'w')

eDateLabel.place(x = 10, y = row3, anchor = 'w')
endDate.place(x = 105, y = row3, anchor = 'w')

console_text.place(x = 10, y = row4, relwidth = 0.97, anchor = 'nw')

console_text.insert(tk.END, 'Service account: earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com\n')
console_text.insert(tk.END, 'Service file: {}\n'.format(service_file))

if service_accountok:
  console_text.insert(tk.END, '\nService account OK\n\n')
  runButton.place (x = 10, y = row5, anchor = 'w')
else:
  console_text.insert(tk.END, '\nService account or service file is invalid.\n')
  runButton.config(state = 'disabled')
  runButton.place (x = 10, y = row5, anchor = 'w')

window.mainloop()