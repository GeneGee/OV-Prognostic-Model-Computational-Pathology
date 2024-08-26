# OV-Prognostic-Model-Computational-Pathology
# Environment

Operating System: ubuntu

Terminal Setting: anaconda windows PowerShell from *https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh*

# 1 Download diagnostic svs files
## 1.1 Prepare manifest file for TCGA-OV diagnostic WSIs (whole slide images )
Download two manifest files (Diagnostic.svs.manifest.txt TCGA-OV.manifest.txt ) from *https://portal.gdc.cancer.gov/projects/TCGA-OV*

*Note: It is important to discriminate "Diagnostic Slide" and "Tissue Slide", usually we need diagnostic slide to train our models.*
*However I have not found a convenient way to directly download diagnostic slide by cancer type*
*So I wrote a python script (extract.diagnostic.svs.py) to extract TCGA-OV diagnostic slide svs file from these two files*

```
python extract.diagnostic.svs.py Diagnostic.svs.manifest.txt TCGA-OV.manifest.txt TCGA-OV.diagnostic_slide.manifest.txt
```
After finishing scripts, you will  

## 1.2 Download TCGA-OV diagnostic WSIs with gdc-client tool
Then we could download diagnostic svs file using TCGA-OV.diagnostic_slide.manifest.txt

```
./gdc-client download -m ./TCGA-OV.diagnostic_slide.manifest.txt -d TCGA-OV-SVS
```

After downloading task finished, you will get 107 diagnostic slide svs files stored in TCGA-OV-SVS

# 2 Segmentation, Patching, and Feature extraction of svs files
## 2.1 Extract basic information of all svs files
*Note: It is important to firstly check the basic information of all svs files, and output a file named as svs.info.txt*
*However I have not found a convenient way to automatically extract the information*
*So I wrote a python script (extract.info.svs.py) to extract the information from svs files, mainly using OpenSlide-python*

```
python extract.info.svs.py --svs_dir SVS_DATA_DIR --info_file SVS_INFO_FILE
```

## 2.2 Segmentation and patching of all svs files
*Note: It is important to segment all svs files and divide them into patches, and here I took use of CLAM https://github.com/mahmoodlab/CLAM/tree/master to finish this task*
*Here I only use default setting in tcga.csv, alternatively you may choose ostu method to achieve a better segmentation result*
*Different patch size may have very tremendous impacts on downstream model training, here I chose 256X256 pixel size for each patch*
```
python create_patches_fp.py --source SVS_DATA_DIR --save_dir PATCH_DIR --patch_size 256 --seg --patch --stitch --preset tcga.csv
```
After segmentation task finished, you will get results in PATCH_DIR

## 2.3 Feature extraction of all patch files
```
python extract_features_fp.py --data_h5_dir PATCH_DIR --data_slide_dir SVS_DIR --csv_path PATCH_DIR\process_list_autogen.csv --feat_dir FEATURE_DIR --batch_size 126 --slide_ext .svs
```

# 3 Clinical information preparation




