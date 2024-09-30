import argparse
import os
import sys

### Training settings
parser = argparse.ArgumentParser(description='select qualified biopsy samples from TCGA Data.')
parser.add_argument('--masks_dir',   type=str, help='')
parser.add_argument('--diagnostic_svs_dir',   type=str, help='')
parser.add_argument('--patches_dir',   type=str, help='')

def get_diagnostic_samples():
  diagnostic_sample_list = []
  for fi in os.listdir(args.diagnostic_svs_dir):
    recs = os.path.splitext(fi)
    sample_name, ext_name = recs[0], recs[1]
    if ext_name != '.svs':
      print(f"*warning: a non svs file: {fi} found")
      continue
    if sample_name not in diagnostic_sample_list:
      diagnostic_sample_list.append(sample_name)
  return diagnostic_sample_list

def stat_patch_num():
  
