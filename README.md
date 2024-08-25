# OV-Prognostic-Model-Computational-Pathology
# Environment:

Operating System: ubuntu

Terminal Setting: anaconda windows PowerShell from *https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Windows-x86_64.exe*

# Step1 Download diagnostic svs files
## 1.1 Prepare manifest file
Download two manifest files (Diagnostic.svs.manifest.txt TCGA-OV.manifest.txt ) from *https://portal.gdc.cancer.gov/projects/TCGA-OV*

*It is important to discriminate "Diagnostic Slide" and "Tissue Slide", usually we need diagnostic slide to train our models.*
*However I have not found a convenient way to directly download diagnostic slide by cancer type*
*So I wrote a python script (extract.diagnostic.svs.py) to extract TCGA-OV diagnostic slide svs file from these two files*

```
python extract.diagnostic.svs.py Diagnostic.svs.manifest.txt TCGA-OV.manifest.txt TCGA-OV.diagnostic_slide.manifest.txt
```

## 1.2 Download svs files
*Then we could download diagnostic svs file using TCGA-OV.diagnostic_slide.manifest.txt*

```
./gdc-client download -m ./TCGA-OV.diagnostic_slide.manifest.txt -d TCGA-OV-SVS
```

*After downloading task finished, you will get 107 diagnostic slide svs files*

# Step2 Check svs file's hierarchical structure
