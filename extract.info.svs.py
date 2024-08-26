import os
import openslide
import numpy as np
import pandas as pd
import cv2
import argparse

# set svs directory path
parser = argparse.ArgumentParser(description='Configurations for WSIs info extraction')
parser.add_argument('--svs_dir', type=str, default=None, help='WSIs directory')
parser.add_argument('--info_file', type=str, default=None, help='output file stored WSIs info')
args = parser.parse_args()

def extract_wsi_info(wsi_path):
  slide = openslide.open_slide(wsi_path)
  width, height = slide.dimensions
  num_levels = slide.level_count
  dimensions = slide.level_dimensions
  if 'aperio.AppMag' in slide.properties.keys():
    level_0_magnification = int(slide.properties['aperio.AppMag'])
    print('aperio.AppMag')
  elif 'openslide.mpp-x' in slide.properties.keys():
    level_0_magnification = 40 if int(np.floor(float(slide.properties['openslide.mpp-x'])*10))==2 else 20
    print('openslide.mpp-x')
  else:
    level_0_magnification = 40
    print('default')
  info_list = [width, height, num_levels, dimensions, level_0_magnification]
  #properties = []
  #for key in slide.properties.keys():
  #  properties.append([key, slide.properties[key]])
  #  print([key, slide.properties[key]])
  #info_list.append(properties)
  #magnification = 5
  #downsample = level_0_magnification/5
  #level = slide.get_best_level_for_downsample(downsample)
  #image = slide.read_region((0,0), slide.level_count-5, slide.level_dimensions[5])
  #image = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGR)
  #cv2.imwrite(output_path, image)
  return info_list

def main():
  fw = open(args.info_file, "w")
  fw.write("\t".join(["Width","Height","Levels","Dimensions","Level_0_magnification"])+"\n")
  for file in os.listdir(args.svs_dir):
    file_path = os.path.join(args.svs_dir, file)
    if not file_path.endswith('.svs'):
      continue
    info_recs = extract_wsi_info(file_path)
    fw.write("\t".join([str(rec) for rec in info_recs])+"\n")
  fw.close()
  
if __name__ == "__main__":
    results = main()
    print("finished!")
    print("end script")
