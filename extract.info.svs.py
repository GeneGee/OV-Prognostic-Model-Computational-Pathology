import os
import openslide
import numpy as np
import pandas as pd
import cv2
import pyvips
import argparse

# set svs directory path
parser = argparse.ArgumentParser(description='Configurations for WSIs info extraction')
parser.add_argument('--magnification', type=float, default=20.0, help='Magnification')
parser.add_argument('--svs_dir', type=str, default=None, help='WSIs directory')
parser.add_argument('--new_dir', type=str, default=None, help='new WSIs directory')
parser.add_argument('--info_file', type=str, default=None, help='output file stored WSIs info')
args = parser.parse_args()

def extract_wsi_info(wsi_path, new_path):
  slide = openslide.open_slide(wsi_path)
  width, height = slide.dimensions
  num_levels = slide.level_count
  dimensions = slide.level_dimensions
  downsamples = slide.level_downsamples
  if 'aperio.AppMag' in slide.properties.keys():
    level_0_magnification = int(slide.properties['aperio.AppMag'])
    print('aperio.AppMag')
  elif 'openslide.mpp-x' in slide.properties.keys():
    level_0_magnification = 40 if int(np.floor(float(slide.properties['openslide.mpp-x'])*10))==2 else 20
    print('openslide.mpp-x')
  else:
    level_0_magnification = 40
    print('default')
  info_list = [width, height, num_levels, downsamples, dimensions, level_0_magnification]
  magnification = args.magnification
  downsample = float(magnification)/level_0_magnification
  new_image = pyvips.Image.new_from_file(wsi_path)
  resize_image = new_image.resize(downsample)
  resize_image.wirte_to_file(new_path)
  return info_list

def main():
  fw = open(args.info_file, "w")
  fw.write("\t".join(["Width","Height","Levels","Downsamples","Dimensions","Level_0_magnification"])+"\n")
  for file in os.listdir(args.svs_dir):
    sample = '.'.join(file.split('.')[:-1])
    file_path = os.path.join(args.svs_dir, file)
    new_file_path = os.path.join(args.new_dir, sample+".tiff")
    if not file_path.endswith('.svs'):
      continue
    info_recs = extract_wsi_info(file_path, new_file_path)
    fw.write("\t".join([str(rec) for rec in info_recs])+"\n")
  fw.close()
  
if __name__ == "__main__":
    results = main()
    print("finished!")
    print("end script")
