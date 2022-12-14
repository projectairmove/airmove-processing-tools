import os
import re
import logging
import datetime
from pathlib import Path
import pytz

def get_logger(
        script_name,
        log_directory,
        log_format='%(asctime)s;%(name)s;%(levelname)s;%(message)s',
        log_level=logging.DEBUG):

    logger = logging.getLogger(script_name)
    logger.setLevel(log_level)
    Path(str(log_directory)).mkdir(parents=True, exist_ok=True)
    fh = logging.FileHandler(os.path.join(
        log_directory,
        datetime.datetime.strftime(
            datetime.datetime.now(),
            f"%Y-%m-%dT%H%M%S.{script_name}.log")))

    formatter = logging.Formatter(log_format)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    return logger

