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
conda create -n airmove python=3.8
conda activate data-processing-tools
pip install -r requirements.txt
```
#### Windows
```
conda create -n dpt-pyqt3 -c conda-forge python=3.7 gdal rasterio geopandas fiona opencv cartopy arosics pyqt
conda activate dpt-pyqt3
pip install -r requirements.txt --user
```

## Usage


**(Recommended) Prepare environment variables containing your default paramters**
This is to avoid having to type the gcp and depacketed image paths every run.

Set the following variables to your `.bashrc` or `.zshrc`. Make sure to change the paths to your actual directories.:
```
export DIWATA1_GCP_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-unshare/GRASPED Ops Team Georeferenced Data Repository/Diwata-1/**/D1_SMI_*.points"

export DIWATA1_RAW_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Extracted Images"

export DIWATA2_GCP_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared drives/GRASPED Product Development Team Drive/Products/Diwata 2/Collection 1/**/D2_SMI_*.points"

export DIWATA2_RAW_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Testing/Extracted_Images/diwata-2"
```


### Diwata-1

**Prepare files**
This step moves files into a working directory for processing.


For regular processing:
```
python prepare-files.py diwata-1 /data/GRASPED/Processing/2020-02-12 \
    --gcp-source="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-unshare/GRASPED Ops Team Georeferenced Data Repository/Diwata-1/**/D1_SMI_*.points" \
    --img-source="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Testing/Extracted_Images/diwata-1"
```

or, if you have set your environment variables...

```
python prepare-files.py diwata-1 /data/GRASPED/Processing/2020-02-12
```


**Process data**
```
python process-data.py diwata-1 /data/GRASPED/Processing/2020-02-12
```


### Diwata-2

**Prepare files**
This step moves files into a working directory for processing.


For regular processing:
```
python prepare-files.py diwata-2 /data/GRASPED/Processing/2020-02-12/Diwata-2 \
    --gcp-source="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared drives/GRASPED Product Development Team Drive/Products/Diwata 2/Collection 1/**/D2_SMI_*.points" \
    --img-source="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Testing/Extracted_Images/diwata-2"
```


For devs:
```
python prepare-files.py diwata-2 temp/Diwata-2 \
    --gcp-source="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared drives/GRASPED Product Development Team Drive/Products/Diwata 2/Collection 1/**/D2_SMI_*.points" \
    --img-source sample_data/Extracted_Images/diwata-2 \
    --no-check-duplicates
```

or, if you have set your environment variables...

```
python prepare-files.py diwata-2 /data/GRASPED/Processing/2020-02-12
```

### 
Run L1A Correction

```
python run-correction.py diwata-2 /data/GRASPED/Processing/2020-03-16\ -\ Special\ Request/Depacketed /data/GRASPED/Processing/2020-03-16\ -\ Special\ Request/L1A\ Test
```


## For Developers

`sample_data` can be found at 


** Run Tests **

```
python -m unittest
```

** Set envrionment variables **
```
python set_environment_variables.py
```

# Common Configurations

Diwata-1 w/ old extracted images
```
export DIWATA1_GCP_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-unshare/GRASPED Ops Team Georeferenced Data Repository/Diwata-1/**/D1_SMI_*.points"
export DIWATA1_RAW_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Extracted_Images"
```

Diwata1 w/ new extracted images
```
export DIWATA1_GCP_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-unshare/GRASPED Ops Team Georeferenced Data Repository/Diwata-1/**/D1_SMI_*.points"
export DIWATA1_RAW_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Testing/Extracted_Images/diwata-1"
```

Diwata-2
```
export DIWATA2_GCP_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared drives/GRASPED Product Development Team Drive/Products/Diwata 2/Collection 1/**/D2_SMI_*.points"
export DIWATA2_RAW_PATH="/home/benjiao/Insync/benjiao@stamina4space.upd.edu.ph/Google Drive - Shared with me/diwata1-UPD-share/Testing/Extracted_Images/diwata-2"
```

# Diwata Image Depacketer and Uploader

### Diwata Image Depacketer for Merged Raw Images
```
python depacket_merged_raw_images.py --source_folder /home/user/merged_raw_images
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to save depacketed images. Default is 'depacket'. |
| --quiet | disable printing of messages per depacketing of rg3. Does not disable image-depacketer messages |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to depacketing of found rg3/bin |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only depackets the first merged_raw_image found. |
| --log-dir | where to save logs generated by the script. |

### Diwata Merged Raw Images Uploader
```
python upload_merged_raw_images.py --source_folder /home/user/merged_raw_images
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to save depacketed images. Default is 'upload-merged-raws'. Will not happen if '--no-move' is used |
| --satellite | What satellite will be saved. |
| --quiet | disable printing of messages per depacketing of rg3. Does not disable image-depacketer messages |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to depacketing of found rg3/bin |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only uploads the first merged_raw_image found. |
| --log-dir | where to save logs generated by the script. |
| --api-url | Endpoint where to upload Depacketed Files. Default is 'https://api.ops.dev.phl-microsat.upd.edu.ph' |
| --api-username | Username for API authentication. Default is "test@phl-microsat.xyz" |
| --api-password | Password for API authentication. Default is "diwatadiwata" |
| --check-duplicates/--no-check-duplicates | Checks first if files exist in the repository before uploading it. Use --no-check-duplicates to bypass checking for duplicates |


### Diwata Image Depacketer Files Uploader
```
python upload_image_depacketer_files.py --source_folder /home/user/image_depacketer_files
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to save uploaded files. Default is 'upload-output'. Will not happen if '--no-move' is used |
| --satellite | What satellite will be saved. |
| --quiet | disable printing of messages per depacketing of rg3. Does not disable image-depacketer messages |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to depacketing of found rg3/bin |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only uploads the first json (and its corresponding files) found. |
| --log-dir | where to save logs generated by the script. |
| --api-url | Endpoint where to upload Depacketed Files. Default is 'https://api.ops.dev.phl-microsat.upd.edu.ph' |
| --api-username | Username for API authentication. Default is "test@phl-microsat.xyz" |
| --api-password | Password for API authentication. Default is "diwatadiwata" |
| --check-duplicates/--no-check-duplicates | Checks first if files exist in the repository before uploading it. Use --no-check-duplicates to bypass checking for duplicates |

Run the following tests:
```
python -m unittest tests.test_depacket_merged_raw_images
python -m unittest tests.test_upload_merged_raw_images
python -m unittest tests.test_upload_image_depacketer_files
```


### XTLM Depacketer
```
python depacket_xtlm.py --source_folder "~/bins"
```
| Option | Description |
| ----- | ----- |
| --source_folder | XTLM directory |
| --satellite | XTLM source satellite |
| --output-directory | output depacketed images |
| --move/--no-move | boolean to move TLM file after depacketed |
| --log-dir | XTLM source satellite |

### TLM Uploader
```
python upload_tlm.py --source_folder "~/bins"
```
| Option | Description |
| ----- | ----- |
| --source_folder | XTLM directory |
| --tlm-type | TLM file type with default 'XTLM' |
| --satellite | XTLM source satellite |
| --receiving-station | XTLM source GRS |
| --compute-md5/--no-compute-md5 | Boolean to compute md5 |
| --output-directory | output depacketed images |
| --move/--no-move | boolean to move TLM file after depacketed |
| --url | OPS-SOFTWARE URL |
| --app-id | OPS-SOFTWARE app ID |
| --app-token | OPS-SOFTWARE app token |
| --username | OPS-SOFTWARE username |
| --password | OPS-SOFTWARE password |
| --watchman-called | Flag one by one processing |
| --log-dir | XTLM source satellite |
| --check-duplicates | Does not upload if duplicate is found |

### Raw Image Uploader
```
python upload_raw_images.py --source_folder "~/bins"
```
| Option | Description |
| ----- | ----- |
| --source_folder | XTLM directory |
| --parent-tlm | Flag to use if get `from_tlm` to source folder |
| --custom-tlm | Use custom name for `from_tlm` |
| --depacketer-version | Version of depacketer |
| --compute-md5/--no-compute-md5 | Boolean to compute md5 |
| --move/--no-move | boolean to move TLM file after depacketed |
| --output-directory | output depacketed images |
| --url | OPS-SOFTWARE URL |
| --app-id | OPS-SOFTWARE app ID |
| --app-token | OPS-SOFTWARE app token |
| --username | OPS-SOFTWARE username |
| --password | OPS-SOFTWARE password |
| --check-duplicates | Does not upload if duplicate is found |


### Capture Upload
```
python upload_l1.py --source_folder "/data/GRASPED/Archive/**/D2*"
```

| Option | Description |
| ----- | -----|
| source_folder | Must be a directory containing files of a single capture, or a glob expression returning a list of capture folders (eg. "D2_SMI_2018-12-14T045351064_V550")
| --dry-run/--no-dry-run | List down files to be uploaded |



### Capture Group Products Uploader
```
python upload_capture_group_product.py "~\MOSAIC_OUTPUT\Mosaic" --product-type Mosaic --payload SMI --compute-md5
```
| Option | Description |
| ----- | ----- |
| --source_folder | Mosaic or stacked directory |
| --thumbnails | Thumbnails of mosaic or stacked directory |
| --payload | Payload type of product to upload |
| --product-type | Product type of the batch upload, Stacked or Mosaic |
| --is-published | When flagged product is published |
| --compute-md5/--no-compute-md5 | Boolean to compute md5 |
| --copy | Flag to copy capture group product file after uploaded |
| --copy-to | Directory where to place uploaded or failed |
| --check-duplicates | Flag to check first if files exist in the repository before uploading it. Use --no-check-duplicates to bypass checking for duplicates |
| --url | OPS-SOFTWARE URL |
| --app-id | OPS-SOFTWARE app ID |
| --app-token | OPS-SOFTWARE app token |
| --username | OPS-SOFTWARE username |
| --password | OPS-SOFTWARE password |
| --log-dir | Directory of logs |

### Diwata GCP Files Uploader
```
python upload_gcp_files.py --source_folder /home/user/gcp_files
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to move uploaded gcp files. Default is 'upload-gcp-files'. Will not happen if '--no-move' is used |
| --quiet | disable printing of messages. |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to upload |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only uploads 1 file at a time. |
| --log-dir | where to save logs generated by the script. |
| --api-url | Endpoint where to upload GCP Files. Default is 'https://api.ops.dev.phl-microsat.upd.edu.ph' |
| --api-username | Username for API authentication. Default is "test@phl-microsat.xyz" |
| --api-password | Password for API authentication. Default is "diwatadiwata" |
| --check-duplicates/--no-check-duplicates | Checks first if files exist in the repository before uploading it. Use --no-check-duplicates to bypass checking for duplicates |
| --convert-to-json | Converts the file to json string before uploading the data. Skips uploading of the file. Will still follow --check-duplicates flag |


## COMMANDS CHEATSHEET FOR BATCH UPLOADS

First, run the script `init_folders.sh` to initialize the working directory. The following folders will be created under `~/DATA_PROCESSING`:
```
00-xtlm_data_asti (Put new xtlms here!!!)
01-upload_xtlm
02-depacket_xtlm
03-upload_raw_images
04-merge_raw_images
05-upload_merged_raw_images
06-depacket_merged_raw_images
07-upload_image_depacketer_files

99-logs_dir
```
*Diwata-1 and Diwata-2 subfolders are automatically created for applicable processes*

### PROD COMMANDS 

| Process | Command |
| ----- | ----- |
| 01-upload_xtlm | `python upload_tlm.py  --source-folder ~/DATA_PROCESSING/00-xtlm_data_asti/ --output-directory ~/DATA_PROCESSING/01-upload_xtlm/ --identify-satellite --log-dir ~/DATA_PROCESSING/99-logs_dir/ --move --url https://api.ops.phl-microsat.upd.edu.ph --compute-md5 --app-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --app-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --username admin --password diwatadiwata --check-duplicates` |
| 02-depacket_xtlm | `python depacket_xtlm.py --source-folder ~/DATA_PROCESSING/01-upload_xtlm/uploaded --output-directory ~/DATA_PROCESSING/02-depacket_xtlm/ --move --sort-by-satellite --log-dir ~/DATA_PROCESSING/99-logs_dir` |

#### For Diwata-1:

| Process | Command |
| ----- | ----- |
| 03-upload_raw_images | `python upload_raw_images.py --source-folder ~/DATA_PROCESSING/02-depacket_xtlm/output/Diwata-1/ --output-directory ~/DATA_PROCESSING/03-upload_raw_images/Diwata-1/ --log-dir ~/DATA_PROCESSING/99-logs_dir/ --url https://api.ops.phl-microsat.upd.edu.ph --app-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --app-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --username admin --password diwatadiwata --check-duplicates --move --parent-tlm --compute-md5 --satellite Diwata-1` |
| 04-merge_raw_images | `python merge_raw_images.py --source-folder ~/DATA_PROCESSING/03-upload_raw_images/Diwata-1/uploaded/ --output-folder ~/DATA_PROCESSING/04-merge_raw_images/Diwata-1/ --log-dir ~/DATA_PROCESSING/99-logs_dir/ --rg3-images-folder ~/DATA_PROCESSING/04-merge_raw_images/Diwata-1/success` |
| 05-upload_merged_raw_images | `python upload_merged_raw_images.py --source-folder ~/DATA_PROCESSING/04-merge_raw_images/Diwata-1/merged_raw_images/ --output-folder ~/DATA_PROCESSING/05-upload_merged_raw_images/Diwata-1/ --satellite Diwata-1 --api-url https://api.ops.phl-microsat.upd.edu.ph --api-application-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --api-application-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --api-username admin --api-password diwatadiwata --log-dir ~/DATA_PROCESSING/99-logs_dir/` |
| 06-depacket_merged_raw_images | `python depacket_merged_raw_images.py --source-folder ~/DATA_PROCESSING/05-upload_merged_raw_images/Diwata-1/success/ --output-folder ~/DATA_PROCESSING/06-depacket_merged_raw_images/Diwata-1/ --log-dir ~/DATA_PROCESSING/99-logs_dir/` 
| 07-upload_image_depacketer_files | `python upload_image_depacketer_files.py --source-folder ~/DATA_PROCESSING/06-depacket_merged_raw_images/Diwata-1/output/ --output-folder ~/DATA_PROCESSING/07-upload_image_depacketer_files/Diwata-1/ --log-dir ~/DATA_PROCESSING/99-logs_dir/ --api-url https://api.ops.phl-microsat.upd.edu.ph --api-application-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --api-application-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --api-username admin --api-password diwatadiwata` |

#### For Diwata-2:

| Process | Command |
| ----- | ----- |
| 03-upload_raw_images | `python upload_raw_images.py --source-folder ~/DATA_PROCESSING/02-depacket_xtlm/output/Diwata-2/ --output-directory ~/DATA_PROCESSING/03-upload_raw_images/Diwata-2/ --log-dir ~/DATA_PROCESSING/99-logs_dir/ --url https://api.ops.phl-microsat.upd.edu.ph --app-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --app-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --username admin --password diwatadiwata --check-duplicates --move --parent-tlm --compute-md5 --satellite Diwata-2` |
| 04-merge_raw_images | `python merge_raw_images.py --source-folder ~/DATA_PROCESSING/03-upload_raw_images/Diwata-2/uploaded/ --output-folder ~/DATA_PROCESSING/04-merge_raw_images/Diwata-2/ --log-dir ~/DATA_PROCESSING/99-logs_dir/ --rg3-images-folder ~/DATA_PROCESSING/04-merge_raw_images/Diwata-2/success` |
| 05-upload_merged_raw_images | `python upload_merged_raw_images.py --source-folder ~/DATA_PROCESSING/04-merge_raw_images/Diwata-2/merged_raw_images/ --output-folder ~/DATA_PROCESSING/05-upload_merged_raw_images/Diwata-2/ --satellite Diwata-2 --api-url https://api.ops.phl-microsat.upd.edu.ph --api-application-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --api-application-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --api-username admin --api-password diwatadiwata --log-dir ~/DATA_PROCESSING/99-logs_dir/` |
| 06-depacket_merged_raw_images | `python depacket_merged_raw_images.py --source-folder ~/DATA_PROCESSING/05-upload_merged_raw_images/Diwata-2/success/ --output-folder ~/DATA_PROCESSING/06-depacket_merged_raw_images/Diwata-2/ --log-dir ~/DATA_PROCESSING/99-logs_dir/` 
| 07-upload_image_depacketer_files | `python upload_image_depacketer_files.py --source-folder ~/DATA_PROCESSING/06-depacket_merged_raw_images/Diwata-2/output/ --output-folder ~/DATA_PROCESSING/07-upload_image_depacketer_files/Diwata-2/ --log-dir ~/DATA_PROCESSING/99-logs_dir/ --api-url https://api.ops.phl-microsat.upd.edu.ph --api-application-id sbp095XIvFAX7SR6OlBzBxoGHgwrPIilPPTNHtw1 --api-application-token 1fED5kWZHSAeDmLgQEq7wVdeWdQST0fze7NOw7beXTpmmPypR3Fzgo4HspZXURxHD8Wjl75LRlgpE8WcNB2IxEYyo2oenDeJX06wbXM3O7heh4MjVUKL39FZeu1NFoLP --api-username admin --api-password diwatadiwata` |

## LOGS DEPACKETER
```
python depacket_logs.py --source-folder /home/user/acu_logs
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to move uploaded rg3 files. Default is 'depacket_logs'. Will not happen if '--no-move' is used |
| --quiet | disable printing of messages. |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to upload |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only uploads 1 file at a time. |
| --log-dir | where to save logs generated by the script. |
| --satellite | Specify the satellite of the rg3 file. Default is Diwata-1 |

### Raw Log Files Uploader
```
python upload_raw_log_files.py --source_folder /home/user/raw_log_files
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to move uploaded raw files. Default is 'upload-raw-log-files'. Will not happen if '--no-move' is used |
| --satellite | Satellite parameter for the raw log file Default is 'Diwata-1' | 
| --receiving-station | Receiving station parameter. Default is 'ASTI' |
| --quiet | disable printing of messages. |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to upload |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only uploads 1 file at a time. |
| --log-dir | where to save logs generated by the script. |
| --api-url | Endpoint where to upload GCP Files. Default is 'https://api.ops.dev.phl-microsat.upd.edu.ph' |
| --api-username | Username for API authentication. Default is "test@phl-microsat.xyz" |
| --api-password | Password for API authentication. Default is "diwatadiwata" |
| --check-duplicates/--no-check-duplicates | Checks first if files exist in the repository before uploading it. Use --no-check-duplicates to bypass checking for duplicates |

### CSV Log Files Uploader
```
python upload_csv_log_files.py --source_folder /home/user/csv_log_files
```
Additional options:

| Option | Description |
| ----- | ----- |
| --output-folder | Where to move uploaded csv files. Default is 'upload-csv-log-files'. Will not happen if '--no-move' is used |
| --satellite | Satellite parameter for the raw log file Default is 'Diwata-1' | 
| --quiet | disable printing of messages. |
| --no-confirm | disable asking for a confirmation. Automatically proceeds to upload |
| --no-move | Uploader automatically moves finished files into the output-folder. Use this to prevent moving of files. |
| --watchman-called | watchman-specific flag. Don't use this as this only uploads 1 file at a time. |
| --log-dir | where to save logs generated by the script. |
| --api-url | Endpoint where to upload GCP Files. Default is 'https://api.ops.dev.phl-microsat.upd.edu.ph' |
| --api-username | Username for API authentication. Default is "test@phl-microsat.xyz" |
| --api-password | Password for API authentication. Default is "diwatadiwata" |
| --check-duplicates/--no-check-duplicates | Checks first if files exist in the repository before uploading it. Use --no-check-duplicates to bypass checking for duplicates |


### Mosaicing and Stacking
```
python mosaic_images.py [source_directrory] --destination-folder /data/GRASPED/Mosaic
```

Required arguments
| Argument | Description|
| ----- | ----- |
| source_directory | A directory containing Diwata captures inside folders grouped by mission. Each mission folder should be named using the standard Mission ID (eg. D2_SMI_2018-12-14T045331_2018-12-14T160239)

Additional options:


| Option | Description |
| ----- | ----- |
| --destination-folder | Consolidated folder for all output. This will create mosaic, stacked, rgb, simplest cbm, and pub directires if present|
| --mosaic-directory | output folder of mosaiced images |
| --stack-directory | output folder of stacked images | 
| --rgb-directory | output folder of RGB of stacked images |
| --simplest-cb-directory | output folder if improved RGB images |
| --pub-directory| output folder of publication material of RGB images |
| --log-dir | where to save logs generated by the script |
| --quiet | disable printing of messages |


##### Commands Cheatsheet
```
python depacket_logs.py --source-folder ~/DATA_PROCESSING/80-acu_logs --output-folder ~/DATA_PROCESSING/81-depacket_logs --satellite Diwata-1
python upload_raw_log_files.py --source-folder ~/DATA-PROCESSING/80-acu_logs --api-url http://localhost:8000 --satellite Diwata-1
python upload_csv_log_files.py --source-folder ~/DATA-PROCESSING/81-acu_logs --api-url http://localhost:8000 --satellite Diwata-1
```


### HPT Stacking Fixed Point
```
python stack_hpt_fixed_fixed_points.py --copy-from /home/user/collections/extracted_images/ --source_folder /home/user/hpt_pipeline/00-combined_hpt_folder --output-folder /home/user/hpt_pipeline/01-image_coregistration
```
Additional options:

| Option | Description |
| ----- | ----- |
| --copy-from | (Optional.) Folder containing the extracted images. Everything gathered here will be organized and copied to the `source-folder`. |
| --source-folder | The location of organized and processable HPT folders. Default is `stacked_hpt_fixed_points/00-combined_hpt_folder`|
| --output-folder | Where to save generated files (png, tif, and xlsx). Default is `stacked_hpt_fixed_points/01-image_coregistration`. |
| --quiet | Flag to disable printing of most messages. |
| --no-confirm | Flag to disable asking for a confirmation. Automatically proceeds to process. |
| --no-move | Prevents the automatic moving of finished missions from the `source-folder` to  `output-folder`/`finished_hpt_folders`. |



