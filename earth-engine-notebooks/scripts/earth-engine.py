import ee
import geetools

service_account = 'earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com'
credentials = ee.ServiceAccountCredentials(service_account, 'earth-engine-airmove-596be0e84b06.json')
ee.Initialize(credentials)

philippines = ee.Geometry.Polygon(
        [[[116.71687839753203, 18.744929081691417],
          [116.71687839753203, 5.019622515938524],
          [126.91219089753203, 5.019622515938524],
          [126.91219089753203, 18.744929081691417]]], None, False)

start_date = '2018-06-29'
end_date = '2018-07-01'

era5 = ee.ImageCollection('ECMWF/ERA5/DAILY').select('mean_2m_air_temperature','total_precipitation','u_component_of_wind_10m','v_component_of_wind_10m').filterBounds(philippines).filter(ee.Filter.date(start_date, end_date))
print(era5)



extra = dict(sat='ERA5')

tasks = geetools.batch.Export.imagecollection.toDrive(
            collection=era5,
            folder='try/era5-py',
            region=philippines,
            namePattern='{sat}_{system_date}',
            scale=31000,
            datePattern='ddMMMy',
            extra=extra,
            verbose=True,
        )