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

today = date.today() - timedelta(days=1)
yesterday = str(today - timedelta(days=1))



@click.command()
@click.option('--drive-folder', default="ERA5")
@click.option('--local-folder', default="ERA5")
@click.option('--from-date', default=yesterday)
@click.option('--to-date', default=str(today))
@click.option('--log-dir', default="logs")
@click.option('--service-account', envvar='AIRMOVE_SERVICE_ACCOUNT', default=None)
@click.option('--service-file', envvar='AIRMOVE_SERVICE_FILE',default=None)
def download_era5(
    drive_folder, local_folder, from_date, to_date, log_dir,
    service_account, service_file
):

    logger = get_logger(
        script_name="download_era5",
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

    _info(f"ERA5 processing from: {from_date} to {to_date}.")

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

    era5 = ee.ImageCollection(
        'ECMWF/ERA5/DAILY').select(
            'mean_2m_air_temperature',
            'total_precipitation',
            'u_component_of_wind_10m',
            'v_component_of_wind_10m').filterBounds(philippines).filter(
                ee.Filter.date(from_date, to_date))

    extra = dict(sat="ERA5")
    geetools.batch.Export.imagecollection.toDrive(
            collection=era5,
            folder=drive_folder,
            region=philippines,
            namePattern='{sat}_{system_date}',
            scale=31000,
            datePattern='yMMdd',
            extra=extra,
            verbose=True,
    )


if __name__ == '__main__':
    download_era5()
