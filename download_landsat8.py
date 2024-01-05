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
@click.option('--drive-folder', default="LANDSAT8")
@click.option('--from-date', default=yesterday)
@click.option('--to-date', default=str(today))
@click.option('--log-dir', default="logs")
@click.option('--service-account', envvar='AIRMOVE_SERVICE_ACCOUNT', default=None)
@click.option('--service-file', envvar='AIRMOVE_SERVICE_FILE',default=None)
@click.option('--ncr-bounds-file', envvar='NCR_BOUNDS_FILE', default='shared/NCRBoundary.json')
def download_landsat8(
    drive_folder, from_date, to_date, log_dir,
    service_account, service_file, ncr_bounds_file
):

    logger = get_logger(
        script_name="download_landsat8",
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

    _info(f"LANDSAT8 processing from: {from_date} to {to_date}.")

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

    with open(ncr_bounds_file) as f:
        ncr_shape = json.load(f)
    ncr_shape = ee.FeatureCollection(ncr_shape)

    '''
    * Function to mask clouds based on the pixel_qa band of Landsat 8 SR data.
    * @param {ee.Image} image input Landsat 8 SR image
    * @return {ee.Image} cloudmasked Landsat 8 image
    '''
    def maskL8sr(image):
        cloud_shadow_bit_mask = (1 << 4)
        clouds_bit_mask = (1 << 3)
        qa = image.select('QA_PIXEL')
        mask = qa.bitwiseAnd(cloud_shadow_bit_mask).eq(0) and (qa.bitwiseAnd(clouds_bit_mask).eq(0))
        return image.updateMask(mask)

    ls08 = ee.ImageCollection(
        'LANDSAT/LC08/C02/T1_L2').filter(
            ee.Filter.eq('WRS_PATH', 116)).filter(
                ee.Filter.eq('WRS_ROW', 50)).filterBounds(
                    ncr_shape).filterDate(
                        from_date, to_date).filterMetadata(
                            'CLOUD_COVER', 'less_than', 70).map(maskL8sr)


    geetools.batch.Export.imagecollection.toDrive(
        collection=ls08,
        folder=drive_folder,
        region=ncr_box,
        scale=30,
        namePattern='LS08_{system_date}',
        datePattern='yMMdd',
        verbose=True
    )

if __name__ == '__main__':
    download_landsat8()
