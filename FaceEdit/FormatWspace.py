import os,sys,re,pickle
import numpy as np 
import pandas as pd 

# ---------------------------------------------------------------------------- #

# ! format W space into a single numpy matrix (sample size x num latent layer x 512)

datadir = '/data/duongdb/ManyFaceConditions01312022/ExampleProjection/projection-wplus-wavgstart-sgan2'
np_out_path = '/data/duongdb/ManyFaceConditions01312022/ExampleProjection/projection-wplus-wavgstart-sgan2.pickle'


all_w = dict()

np_arr = [os.path.join(datadir,n) for n in sorted ( os.listdir(os.path.join(datadir)) ) if n.endswith('npy') ] 

for img in np_arr: 
  # better to make a dict, so we can filter using label
  # format name: projected22q11DS_early100_22q11DSyoungchild_wplus_wavg_final.npy
  imgname = re.sub('projected','',img)
  imgname = re.sub('_wplus_wavg_final','',imgname)
  imgname = re.sub('npy','png',imgname)
  all_w[imgname.split('/')[-1]] = np.load(img) # something like (1, 14, 512)

#
print (len(all_w))
pickle.dump(all_w, open(np_out_path,'wb'))
