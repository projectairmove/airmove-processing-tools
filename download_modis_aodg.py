import os
import hashlib
from pathlib import Path, PurePath
import shutil
import datetime
import click
import glob
from utilities import get_logger
import ee
import geetools
from datetime import date, timedelta
import json



today = date.today() - timedelta(days=1)
yesterday = str(today - timedelta(days=1))



@click.command()
@click.option('--drive-folder', default="MODIS_AODG")
@click.option('--local-folder', default="MODIS_AODG")
@click.option('--from-date', default=yesterday)
@click.option('--to-date', default=str(today))
@click.option('--log-dir', default="logs")
@click.option('--service-account', envvar='AIRMOVE_SERVICE_ACCOUNT', default=None)
@click.option('--service-file', envvar='AIRMOVE_SERVICE_FILE',default=None)
def download_modis_aodg(
    drive_folder, local_folder, from_date, to_date, log_dir,
    service_account, service_file
):

    logger = get_logger(
        script_name="download_modis_aodg",
        log_directory=log_dir
    )
    def _info(message):
        click.echo(message)
        logger.info(message)
    def _error(message):
        click.echo(message)
        logger.error(message)
    
    if not service_account or not service_file:
        _error("Service account or service file is invalid.")
        exit(1)

    credentials = ee.ServiceAccountCredentials(service_account, service_file)
    ee.Initialize(credentials)
    _info("Service account ok.")

    _info(f"MODIS_AODG processing from: {from_date} to {to_date}.")

    philippines = ee.Geometry.Polygon(
        [[[116.71687839753203, 18.744929081691417],
          [116.71687839753203, 5.019622515938524],
          [126.91219089753203, 5.019622515938524],
          [126.91219089753203, 18.744929081691417]]], None, False)


    ncr_box = ee.Geometry.Polygon(
        [[[120.88626682729029, 14.33788811927746],
          [121.15543186635279, 14.33788811927746],
          [121.15543186635279, 14.792458281417941],
          [120.88626682729029, 14.792458281417941],
          [120.88626682729029, 14.33788811927746]]], None, False)


    ncr_bounds = '/home/dev/airmove/airmove-processing-tools/shared/NCRBoundary.json'

    with open(ncr_bounds) as f:
        ncr_shape = json.load(f)
    ncr_shape = ee.FeatureCollection(ncr_shape)

    _from = from_date.split("-")
    _to = to_date.split("-")
    collection = ee.ImageCollection('MODIS/006/MCD19A2_GRANULES').select('Optical_Depth_055').filterBounds(ncr_shape)

    ncr_bound = ncr_shape.geometry()
    startDate = ee.Date.fromYMD(int(_from[0]), int(_from[1]), int(_from[2]))
    endDate = ee.Date.fromYMD(int(_to[0]), int(_to[1]), int(_to[2]))
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
        
        sysIndexinfo = ee.String(f"MODIS_AODG_{from_date}_{to_date}")
        return datared.set('year', year).set('month', month).set('day', day).set('system:time_start', ini.millis()).set("system:index", sysIndexinfo)
    
    dailyAve_Listversion = daysList.map(getDailyAve)
    dailyAve_Colversion = ee.ImageCollection(dailyAve_Listversion)

    geetools.batch.Export.imagecollection.toDrive(
        collection=dailyAve_Colversion,
        namePattern='MODIS_AODG_{system_date}',
        folder=drive_folder,
        region=ncr_box,
        scale=1000,
        verbose=True
)


if __name__ == '__main__':
    download_modis_aodg()
