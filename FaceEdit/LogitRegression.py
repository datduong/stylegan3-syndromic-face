import os,sys,re
import pickle

import gzip
import json

import numpy as np
from tqdm import tqdm_notebook

import warnings
import matplotlib.pylab as plt

import numpy as np 
import pandas as pd 

from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.linear_model import Ridge

from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.metrics import accuracy_score

import PIL.Image

import argparse

# ---------------------------------------------------------------------------- #

def parse_string_to_range(s): 
  if s is None: 
    return None
  s = [int(i.strip()) for i in s.split('-')]
  return np.arange(s[0],s[1])

# ---------------------------------------------------------------------------- #

parser = argparse.ArgumentParser()
parser.add_argument("--dlatents_dict", type=str, default=None)
parser.add_argument("--label_csv", type=str, default=None)
parser.add_argument("--num_ws", type=int, default=14)
parser.add_argument("--losstype", type=str, default='log')
parser.add_argument("--style", type=parse_string_to_range, default=None)
parser.add_argument("--direction_output", type=str, default=None)
parser.add_argument("--label1", type=str, default=None)
parser.add_argument("--label2", type=str, default=None)

args = parser.parse_args()

# ---------------------------------------------------------------------------- #
# ! fit logit regression on flatten W

dlatents_dict = pickle.load(open(args.dlatents_dict,'rb'))

if args.style is not None: 
  args.num_ws = len(args.style)

# ---------------------------------------------------------------------------- #
# ! separate w latents into numpy format based on label

# ! let's try age group 

X_data = []
Y_logit = [] # label 
for img,w_np in dlatents_dict.items():
  if bool(re.findall('^'+args.label1, img) ): 
    Y_logit.append(0)
  elif bool(re.findall('^'+args.label2, img) ): 
    Y_logit.append(1)
  else: 
    continue # ! skip... doing pairwise SVM ? 
  #
  if args.style is not None: 
    w_np = w_np [:,args.style,:] # get direction from these layers
  #
  w_np = np.squeeze( w_np.reshape((-1, args.num_ws*512)) ) # make into 1D array
  X_data.append(w_np)
  

# 
X_data = np.array(X_data)
Y_logit = np.array(Y_logit) # wants (n_samples, )

print ('X_data', X_data[0:10], X_data.shape)
print ('Y_logit', set(Y_logit), Y_logit[0:10], Y_logit.shape)

# ! fit model 
clf = SGDClassifier(args.losstype, n_iter_no_change=500, max_iter=1000, class_weight='balanced') # SGB model for performance sake
clf.fit(X_data, Y_logit)
fitted_coef = clf.coef_.reshape((args.num_ws, 512))
fitted_coef = np.array([fitted_coef]) # match w dim which is something like [1,14,512]
print ('fitted_coef',fitted_coef.shape)

# output    
score = clf.score(X_data, Y_logit)
print('logit score {}'.format(score))

pickle.dump(fitted_coef, open(args.direction_output,'wb'))

  