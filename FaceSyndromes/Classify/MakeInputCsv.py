

import os,sys,re,pickle
from numpy.lib.shape_base import split
import pandas as pd 
import numpy as np 

import json

from copy import deepcopy

import argparse

# ! make input csv to test fake images. 

# ------------------------------------------------------------------------------------------------------------

def sort_parse_comma_separated_list(s):
  if isinstance(s, list):
    return sorted(s)
  return sorted( s.split(',') ) 

# ------------------------------------------------------------------------------------------------------------


parser = argparse.ArgumentParser()
parser.add_argument("--folder_path", type=str, default=None)
parser.add_argument("--folder_keyword", type=str, default=None)
parser.add_argument("--csv_output_name", type=str, default=None)
parser.add_argument("--exclude_str", type=str, default=None)


args = parser.parse_args()

images_dict = {'name':[], 
               'path':[], 
               'label': [], 
               'fold': [], 
               'is_ext': [] # ! so we can exclude normal faces
              }

for f in os.listdir(args.folder_path): 
  if args.exclude_str is not None: 
    if ('M1' in f) or ('M0' in f): 
      continue
        
  if bool ( re.search ( args.folder_keyword, f ) ) :    
    print (f)
    # WS,22q11DS,Controls
    if f[0] == '0': 
      condition = '22q11DS'
    elif f[0] == '3': 
      condition = 'WS'
    elif f[0] == '1': 
      condition = 'Controls'
    elif f[0] == '2': 
      condition = 'Normal'
      
    for i in os.listdir(os.path.join(args.folder_path,f)):
      #
      images_dict['label'].append(condition) 
      images_dict['name'].append(f+condition+i) # backtrack easier. 
      images_dict['path'].append(os.path.join(args.folder_path, f, i) ) # path to image
      images_dict['fold'].append(5)
      images_dict['is_ext'].append(0)

#
df = pd.DataFrame.from_dict(images_dict)
print ('df size' , df.shape)

df.to_csv(os.path.join(args.folder_path,args.csv_output_name), index=False)

