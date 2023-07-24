
import os,sys,re,pickle
from tabnanny import verbose
import cv2
import numpy as np

import pixellib
from pixellib.tune_bg import alter_bg

from tqdm import tqdm

# ! https://pixellib.readthedocs.io/en/latest/change_image_bg.html?highlight=color_bg#image-tuning-with-pixellib
change_bg = alter_bg()
change_bg.load_pascalvoc_model("/data/duongdb/deeplabv3_xception_tf_dim_ordering_tf_kernels.h5")

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--imagepath", type=str, default=None)
parser.add_argument("--foutpath", type=str, default=None)
parser.add_argument("--colorcode", type=int, default=255)
parser.add_argument("--namesuffix", type=str, default=None)
parser.add_argument("--start", type=int, default=None)
parser.add_argument("--end", type=int, default=None)
parser.add_argument("--resolution", type=int, default=None)
parser.add_argument("--verbose", action='store_true', default=False) # skip already created file

args = parser.parse_args()


# imagepath = '/data/duongdb/ManyFaceConditions01312022/ExampleSurveyIRB01312022Fake'
# foutpath = '/data/duongdb/ManyFaceConditions01312022/ExampleSurveyIRB01312022FakeRemoveBg'


if not os.path.exists(args.foutpath): 
  os.mkdir (args.foutpath)

# 
os.chdir(args.imagepath)
imagelist = np.array(sorted(os.listdir(args.imagepath)))

if args.start is not None: 
  if args.end > len(imagelist): 
    args.end = len(imagelist)
  #
  imagelist = imagelist[args.start:args.end]

# ---------------------------------------------------------------------------- #

for imagename in tqdm(imagelist): 
  
  if args.verbose: 
    print ('remove background ', imagename)
    output = change_bg.color_bg(imagename, colors = (args.colorcode, args.colorcode, args.colorcode))
  else: 
    try: 
      output = change_bg.color_bg(imagename, colors = (args.colorcode, args.colorcode, args.colorcode))
    except:
      print ('fail remove background ', imagename)
      continue
    
  if args.resolution is not None: 
    output = cv2.resize(output,(args.resolution,args.resolution))
    
  if args.namesuffix is not None: 
    if imagename.endswith('png') : 
      imagename = re.sub(r'\.png','',imagename)+args.namesuffix+".png"
    else: 
      imagename = re.sub(r'\.jpg','',imagename)+args.namesuffix+".png"
  #
  cv2.imwrite( os.path.join( args.foutpath, imagename ) , output) 

