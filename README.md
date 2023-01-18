# airmove-processing-tools
Automation scripts to download satellite data from different sources

| Script | Description | Sample Usage | 
| ----- | ----- | ----- |
| download_era5.py | Download mean 2m air temp, total precipitation, u and v component of wind 10m from ERA5 satellite | python download_era5.py --from-date 2023-01-17 --to-date 2023-01-18 |
| download_landsat8.py | Download cloud cover data from landsat 8 | python download_landsat8.py --from date 2023-01-17 --to-date 2023-01-18 |
| download_modis_aodb.py | Download MODIS AOD Blue data | python download_modis_aodb.py --from-date 2023-01-17 --to-date 2023-01-18 |
| download_modis_aodg.py | Download MODIS AOD Green data | python download_modis_aodg.py --from-date 2023-01-17 --to-date 2023-01-18 |
| download_s5p_no2.py | Download COPERNICUS NO2 data | python download_s5p_no2.py --from-date 2023-01-17 --to-date 2023-01-18 |



## Setup

#### Debian
```
# Clone the repository.
git clone https://github.com/projectairmove/airmove-processing-tools.git
cd airmove-processing-tools

# Create a conda environment
conda create -n airmove-processing-tools python=3.8

# Activate the environment and install dependencies
conda activate airmove-processing-tools
pip install -r requirements.txt
```

## Usage


**(Recommended) Prepare environment variables containing your default paramters**
This is to avoid having to type the gcp and depacketed image paths every run.

Set the following variables to your `.bashrc` or `.zshrc`. Make sure to change the paths to your actual directories.:
```
export AIRMOVE_SERVICE_ACCOUNT=earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com
export AIRMOVE_SERVICE_FILE=/home/dev/airmove/airmove-processing-tools/shared/service_account_file.json
export NCR_BOUNDS_FILE=/home/dev/airmove/airmove-processing-tools/shared/NCRBoundary.json

```

## Storage
All files are processed using Google Earth Engine and then automatically uploaded to a Google Drive linked to the given service account. To have access to this folders, contact the developers:
https://drive.google.com/drive/folders/1m1NYn1lWe8odC3Vks9QhZKhfleOR0Wq0


### download_era5.py

Regular usage:
```
python download_era5.py --from-date 2023-01-17 --to-date 2023-01-18 --service-account earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com --service-file home/dev/airmove/airmove-processing-tools/shared/service_account_file.json
```
or, if you have set your environment variables...

```
python download_era5.py
```

Processed files directory:
https://drive.google.com/drive/folders/10M3Yk6W9YtKx30YbYDD7JYBuy2Njr5Yc

| Options | Description | Default |
| ----- | ----- | ----- |
| drive-folder | Drive folder where processed data are saved | ERA5 |
| from-date | First date to get for processing | 2023-01-17 (example only. default is yesterday's date of the current running time) | 
| to-date | Last date to get for processing | 2023-01-18 (example only. default is today's date of the current running time) | 
| log-dir | The directory where logs are saved | logs |
| service-account | The service account to be used to connect to GEE | earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com |
| service-file | The service file that is linked to the service account. This must be kept confidential and safe | airmove-processing-tools/shared/service_account_file.json |



### download_landsat8.py

Regular usage:
```
python download_landsat8.py --from-date 2023-01-17 --to-date 2023-01-18 --service-account earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com --service-file home/dev/airmove/airmove-processing-tools/shared/service_account_file.json --ncr-bounds-file /home/dev/airmove/airmove-processing-tools/shared/NCRBoundary.json
```
or, if you have set your environment variables...

```
python download_landsat8.py --from-date 2023-01-17 --to-date 2023-01-18
```

Processed files directories:
| Script | Default | Google Drive Directory |
| ----- | ----- | ----- |
| download_landsat8.py | LANDSAT8 | https://drive.google.com/drive/folders/1p9rZ4MaS5rmuNsn8J3XLXZdk1tQYQ3Ar |
| download_modis_aodb.py | MODIS_AODB | https://drive.google.com/drive/folders/1nSERd7-5W83q-Q6Q8DEYmRtRgF4t1JCg |
| download_modis_aodg.py | MODIS_AODG | https://drive.google.com/drive/folders/12iQX6Z3UNRyGVH0T7rq0hOKcgg904wrF |
| download_s5p_no2.py | S5P_NO2 | https://drive.google.com/drive/folders/1j1JeNb1sy2ZCaGgdiVVSGfGBehlxKzSw |

The following options are also applicable for all the scripts below:
| Options | Description | Default |
| ----- | ----- | ----- |
| drive-folder | Drive folder where processed data are saved | *see table above |
| from-date | First date to get for processing | 2023-01-17 (example only. default is yesterday's date of the current running time) | 
| to-date | Last date to get for processing | 2023-01-18 (example only. default is today's date of the current running time) | 
| log-dir | The directory where logs are saved | logs |
| service-account | The service account to be used to connect to GEE | earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com |
| service-file | The service file that is linked to the service account. This must be kept confidential and safe | airmove-processing-tools/shared/service_account_file.json |
| ncr-bounds-file | The NCR bounds file to be used for processing | airmove-processing-tools/shared/NCRBoundary.json |


### download_modis_aodb.py / download_modis_aodg.py

Regular usage:
```
python download_modis_aodb.py --from-date 2023-01-17 --to-date 2023-01-18 --service-account earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com --service-file home/dev/airmove/airmove-processing-tools/shared/service_account_file.json --ncr-bounds-file /home/dev/airmove/airmove-processing-tools/shared/NCRBoundary.json

python download_modis_aodg.py --from-date 2023-01-17 --to-date 2023-01-18 --service-account earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com --service-file home/dev/airmove/airmove-processing-tools/shared/service_account_file.json --ncr-bounds-file /home/dev/airmove/airmove-processing-tools/shared/NCRBoundary.json
```
or, if you have set your environment variables...

```
python download_modis_aodb.py --from-date 2023-01-17 --to-date 2023-01-18

python download_modis_aodg.py --from-date 2023-01-17 --to-date 2023-01-18
```


### download_s5p_no2.py

Regular usage:
```
python download_s5p_no2.py --from-date 2023-01-17 --to-date 2023-01-18 --service-account earth-engine-robot@earth-engine-airmove.iam.gserviceaccount.com --service-file home/dev/airmove/airmove-processing-tools/shared/service_account_file.json --ncr-bounds-file /home/dev/airmove/airmove-processing-tools/shared/NCRBoundary.json
```
or, if you have set your environment variables...

```
python download_s5p_no2.py --from-date 2023-01-17 --to-date 2023-01-18
```
