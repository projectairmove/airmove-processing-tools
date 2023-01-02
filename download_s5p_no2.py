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
@click.option('--drive-folder', default="S5P_NO2")
@click.option('--local-folder', default="S5P_NO2")
@click.option('--from-date', default=yesterday)
@click.option('--to-date', default=str(today))
@click.option('--log-dir', default="logs")
@click.option('--service-account', envvar='AIRMOVE_SERVICE_ACCOUNT', default=None)
@click.option('--service-file', envvar='AIRMOVE_SERVICE_FILE',default=None)
def download_s5p_no2(
    drive_folder, local_folder, from_date, to_date, log_dir,
    service_account, service_file
):

    logger = get_logger(
        script_name="download_s5p_no2",
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

    _info(f"S5P_NO2 processing from: {from_date} to {to_date}.")

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
    ncr_bound = ncr_shape.geometry()

    no2 = ee.ImageCollection('COPERNICUS/S5P/NRTI/L3_NO2').select('NO2_column_number_density').filterBounds(ncr_shape).filterDate(from_date, to_date)
    val_max = 0.0002
    val_min = 0
    band_viz = {
        "min": val_min,
        "max": val_max, 
        "opacity": 1.0, 
        "palette": ["black","blue","purple","cyan","green","yellow","red"]
    }

    NCR_mean = no2.mean()
    
    geetools.batch.Export.imagecollection.toDrive(
        collection=no2,
        namePattern="S5P_NO2_{system_date}",
        folder=drive_folder,
        region=ncr_box,
        verbose=True)



if __name__ == '__main__':
    download_s5p_no2()
