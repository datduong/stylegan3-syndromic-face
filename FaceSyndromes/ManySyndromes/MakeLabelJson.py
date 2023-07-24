import os,sys,re,pickle
from numpy.lib.shape_base import split
import pandas as pd 
import numpy as np 

import json

from copy import deepcopy

import argparse

# ------------------------------------------------------------------------------------------------------------

def sort_parse_comma_separated_list(s):
  if isinstance(s, list):
    return sorted(s)
  return sorted( [i.strip() for i in s.split(',') ] ) 


# ------------------------------------------------------------------------------------------------------------

def make_label(fname,label_type_dict): 
  keys = sorted (list (label_type_dict.keys() )) # ! sort will make back-track easier 
  label_array = []
  for k in keys : # go over each key name
    onehot = [0] * len(label_type_dict[k])
    for i,x in enumerate(label_type_dict[k]): # all possible choices of this key k
      if k == 'label1': 
        if bool ( re.findall('^'+x,fname) ) : 
          onehot[i] = 1
      else: # ! other "label"
        if x in fname: 
          onehot[i] = 1
    # 
    label_array = label_array + onehot # concat list 

  # assert np.sum(label_array) == len(label_type_dict) # must have unique name in each "type of label"
  return label_array
  

# ------------------------------------------------------------------------------------------------------------

parser = argparse.ArgumentParser()
parser.add_argument("--json_path", type=str, default=None)
parser.add_argument("--csv_label", type=str, default=None)
parser.add_argument("--age_bracket",type=sort_parse_comma_separated_list,default='2y,adolescence,olderadult,youngadult,youngchild')
parser.add_argument("--disease",type=sort_parse_comma_separated_list,default='WS,22q11DS,Controls,Normal')
parser.add_argument("--skip_gender", action='store_true', default=False)
parser.add_argument("--skip_normal", action='store_true', default=False)
parser.add_argument("--skip_controls", action='store_true', default=False)
parser.add_argument("--skip_age", action='store_true', default=False)
parser.add_argument("--new_df_path", type=str, default=None)

args = parser.parse_args()

np.random.seed(seed=1)

df = pd.read_csv(args.csv_label)
df = df.sample(frac=1, random_state=1999).reset_index(drop=True) # ! random ordering 

if args.skip_controls: 
  df = df[df["label"].str.contains("Controls")==False]
  
if args.skip_normal: 
  df = df[df["label"].str.contains("Normal")==False]

# ! make json 

json_label = {}
json_label['labels'] = []

label_type_dict = {'label1':args.disease, 'label2':args.age_bracket}
print (label_type_dict)

for idx, row in df.iterrows(): # name,path,label,fold,is_ext
  try: 
    onehot = make_label(row['label'],label_type_dict)
    if args.skip_age: 
      onehot = onehot[0:len(args.disease)] # skip age because low count? 
  except: 
    print (row)
    exit()
  # add gender ? why not. 
  if not args.skip_gender : 
    if row['gender'] == -1: 
      onehot = onehot + [ 0, 0 ] # no gender label? 
    elif row['gender'] == 1:
      onehot = onehot + [ 1, 0 ] # female 
    elif row['gender'] == 0: 
      onehot = onehot + [ 0, 1 ] # male 

  #
  json_label['labels'].append ( [row['name'], onehot ] )


df = df.reset_index(drop=True) # ! save csv anyway? 
df.to_csv (args.new_df_path , index=False)

with open(args.json_path, 'w') as outfile:
  json.dump(json_label, outfile)


