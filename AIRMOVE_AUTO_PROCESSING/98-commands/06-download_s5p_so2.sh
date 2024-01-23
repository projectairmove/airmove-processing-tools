#!/bin/bash
source ~/.bashrc
source ./vars.sh

now=$(date +%Y-%m-%d)
to_date=$now
from_date=$(date +%Y-%m-%d -d "7 days ago")

today_log=$LOG_DIR/$now
storage=$DOWNLOAD_DIR/06-S5P_SO2

mkdir -p $today_log
mkdir -p $storage

if [ $# -gt 0 ]; then
	from_date=$1
fi

if [ $# -gt 1 ]; then
	to_date=$2
fi

echo "Processing from $from_date to $to_date"
conda run -n $PROCESSING_ENV python $PROCESSING_SCRIPTS_DIR/download_s5p_so2.py --log-dir $today_log --from-date $from_date --to-date $to_date

rclone copy processing_drive:AIRMOVE_PROCESSING/EE/S5P_NO2/ $storage/  --max-age 7d --drive-shared-with-me --ignore-existing
