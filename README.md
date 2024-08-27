## Environment
Operating System: Linux

Anaconda built from *https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh*

## Prepare manifest file for TCGA-OV diagnostic WSIs
Download two manifest files **Diagnostic.svs.manifest.txt**(all diagnostic svs files), **TCGA-OV.manifest.txt**(all files of TCGA-OV) from *https://portal.gdc.cancer.gov/projects/TCGA-OV*

*Note: It is important to discriminate "**Diagnostic Slide**" and "**Tissue Slide**", usually we need use **Diagnostic Slide** to train models.*
*However I have not found a direct way of downloading diagnostic slide by cancer type.*
*So I wrote a python script (**extract.diagnostic.svs.py**) to extract TCGA-OV diagnostic slide files*

```
python extract.diagnostic.svs.py Diagnostic.svs.manifest.txt TCGA-OV.manifest.txt TCGA-OV.diagnostic_slide.manifest.txt
```
After finishing scripts, you will get a manifest file **TCGA-OV.diagnostic_slide.manifest.txt** to download TCGA-OV diagnostic slide files.

## Download TCGA-OV diagnostic WSIs with gdc-client tool
Then we could download diagnostic svs files using **TCGA-OV.diagnostic_slide.manifest.txt** with gdc-client tool

https://gdc.cancer.gov/system/files/public/file/gdc-client_2.0.0_Ubuntu_x64-py3.8-ubuntu-20.04.zip

```
./gdc-client download -m ./TCGA-OV.diagnostic_slide.manifest.txt -d TCGA-OV-SVS_DIR
```

After downloading task finished, you will get 107 diagnostic slide svs files stored in directory: **TCGA-OV-SVS_DIR**.

## Rename WSIs files
*Note: Because there are differences between the name of WSIs files and their respective samples' name in clinical information file,*
*We need to rename WSIs files to keep accordance with downstream analysis. Here, I wrote a script to finish this task.*

```
python rename.wsi.py TCGA-OV-SVS_DIR
```
## Extract svs information
*Note: It is important to firstly check the basic information of all svs files, and output a file named as svs.info.txt*
*However I have not found a convenient way to automatically extract the information*
*So I wrote a python script (extract.info.svs.py) to extract the information from svs files, mainly using OpenSlide-python*

```
python extract.info.svs.py --svs_dir SVS_DATA_DIR --info_file SVS_INFO_FILE
```

## Segmentation and patching
*Note: It is important to segment all svs files and divide them into patches, and here I took use of **create_patches_fp.py** and **extract_features_fp.py** from CLAM https://github.com/mahmoodlab/CLAM/tree/master to finish this task*
*Here I only use default setting by **tcga.csv in CLAM** , alternatively you may manually choose a modified setting to achieve a better segmentation result.*
*Different patch size may have very tremendous impacts on downstream model training, here I chose 256X256 pixel size for each patch.*
```
python create_patches_fp.py --source SVS_DATA_DIR --save_dir PATCH_DIR --patch_size 256 --seg --patch --stitch --preset tcga.csv
```
After segmentation task finished, you will get results in PATCH_DIR.

## Feature extraction
*Note: By default, CLAM use a truncated pretrained model (ResNet50) to extract a 1024D vector for each patch, you may also choose foundation models CONCH or UNI*
*which will take a much longer time and computation resource to finish this task.*
```
python extract_features_fp.py --data_h5_dir PATCH_DIR --data_slide_dir SVS_DIR --csv_path PATCH_DIR\process_list_autogen.csv --feat_dir FEATURE_DIR --batch_size 12 --slide_ext .svs
```

## Download clinical information
*Download clinical information from cbioportal https://cbioportal-datahub.s3.amazonaws.com/ov_tcga.tar.gz*
*Note: to generate clinical information file which would be used for labelling of samples, that is to divide samples by prognosis*
*Firstly, use **pretreat.clinical_info.r** to merge **data_clinical_patient.txt** and **data_clinical_sample.txt**, and select patients who had os data*
```
Rscript pretreat.clinical_info.r
```
Then you will get a clinical info file: **tcga_ov_clin.csv**
In addition, we need choose samples which have respective diagnostic slide WSIs file
So, I wrote a python script **select_samples_with_WSI.py**
```
python select_samples_with_WSI.py tcga_ov_clin.csv process_list_autogen.csv tcga_ov_clin.prognosis.csv
```

## Training Splits
```
python create_splits_seq.ov_prognosis.py --task task_1_ov_prognosis --seed 1 --k 10
```

## GPU Training for Prognosis Good vs. Bad Classification
```
python main.ov_prognosis.py --drop_out 0.25 --early_stopping --lr 2e-4 --k 10 --exp_code task_1_ov_prognosis --weighted_sample --bag_loss ce --inst_loss svm --task task_1_ov_prognosis --model_type clam_sb --embed_dim 1024
```

## Evaluation Model
```
python eval.ov_prognosis.py --k 10 --models_exp_code task_1_ov_prognosis_s1 --save_exp_code task_1_ov_prognosis_s1_cv --task task_1_ov_prognosis --model_type clam_sb
```

## Heatmap Visualization
```
python create_heatmaps.py --config config.ov_prognosis.yaml
```
