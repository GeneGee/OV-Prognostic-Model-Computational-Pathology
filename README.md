## Environment
Operating System: ubuntu
Terminal Setting: anaconda ubuntu PowerShell 
built from *https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh*

## Download diagnostic svs files
## Prepare manifest file for TCGA-OV diagnostic WSIs
Download two manifest files **Diagnostic.svs.manifest.txt**(all diagnostic svs files), **TCGA-OV.manifest.txt**(all files of TCGA-OV) from *https://portal.gdc.cancer.gov/projects/TCGA-OV*

*Note: It is important to discriminate "**Diagnostic Slide**" and "**Tissue Slide**", usually we need **Diagnostic Slide** to train models.*
*However I have not found a direct way of downloading diagnostic slide by cancer type.*
*So I wrote a python script (**extract.diagnostic.svs.py**) to extract TCGA-OV diagnostic slide files*

```
python extract.diagnostic.svs.py Diagnostic.svs.manifest.txt TCGA-OV.manifest.txt TCGA-OV.diagnostic_slide.manifest.txt
```
After finishing scripts, you will get a manifest file **TCGA-OV.diagnostic_slide.manifest.txt** to download TCGA-OV diagnostic slide files.

## Download TCGA-OV diagnostic WSIs with gdc-client tool
Then we could download diagnostic svs files using **TCGA-OV.diagnostic_slide.manifest.txt** with gdc-client tool https://gdc.cancer.gov/system/files/public/file/gdc-client_2.0.0_Ubuntu_x64-py3.8-ubuntu-20.04.zip

```
./gdc-client download -m ./TCGA-OV.diagnostic_slide.manifest.txt -d TCGA-OV-SVS_DIR
```

After downloading task finished, you will get 107 diagnostic slide svs files stored in directory: **TCGA-OV-SVS**.

## Rename WSIs files
*Note: Because there are differences between the name of WSIs files and their respective samples' name in clinical information file,*
*We need to rename WSIs files to keep accordance with downstream analysis. Here, I wrote a script to finish this task.*

```
python rename.wsi.py TCGA-OV-SVS_DIR
```
## 2 Segmentation, Patching, and Feature extraction
## 2.1 Extract svs information
*Note: It is important to firstly check the basic information of all svs files, and output a file named as svs.info.txt*
*However I have not found a convenient way to automatically extract the information*
*So I wrote a python script (extract.info.svs.py) to extract the information from svs files, mainly using OpenSlide-python*

```
python extract.info.svs.py --svs_dir SVS_DATA_DIR --info_file SVS_INFO_FILE
```

## 2.2 Segmentation and patching
*Note: It is important to segment all svs files and divide them into patches, and here I took use of **create_patches_fp.py** and **extract_features_fp.py** from CLAM https://github.com/mahmoodlab/CLAM/tree/master to finish this task*
*Here I only use default setting in tcga.csv, alternatively you may choose ostu method to achieve a better segmentation result*
*Different patch size may have very tremendous impacts on downstream model training, here I chose 256X256 pixel size for each patch*
```
python create_patches_fp.py --source SVS_DATA_DIR --save_dir PATCH_DIR --patch_size 256 --seg --patch --stitch --preset tcga.csv
```
After segmentation task finished, you will get results in PATCH_DIR

## 2.3 Feature extraction
```
python extract_features_fp.py --data_h5_dir PATCH_DIR --data_slide_dir SVS_DIR --csv_path PATCH_DIR\process_list_autogen.csv --feat_dir FEATURE_DIR --batch_size 126 --slide_ext .svs
```

## 3 Clinical information preparation
## 3.1 Download clinical information
*Download clinical information from cbioportal https://cbioportal-datahub.s3.amazonaws.com/ov_tcga.tar.gz*





