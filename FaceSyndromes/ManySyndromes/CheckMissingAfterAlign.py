import os,sys,re,pickle
import pandas as pd 
import numpy as np 

# ! some images will not align because auto-detection may not work well. 

original_source = '/data/duongdb/ManyFaceConditions12012022/TrimImg'

# original_source = '/data/duongdb/ManyFaceConditions12012022/TrimImg_align_255pix'

new_source = '/data/duongdb/ManyFaceConditions12012022/TrimImg_align_255pix' 
test_img = '' # '/data/duongdb/ManyFaceConditions12012022/TrimImg_no_bg_255pix_align_testset' 

check_these_img = '/data/duongdb/ManyFaceConditions12012022/ManualCheck'+new_source.split('/')[-1]

if os.path.exists(check_these_img): 
  os.system('rm -rf ' + check_these_img) # ! always start fresh 

#
os.mkdir(check_these_img)

original_img_list = set ( os.listdir(original_source) ) 
new_img_list = set ( os.listdir(new_source) )

missing_img_list = original_img_list - new_img_list
missing_img_list = list ( missing_img_list ) 

if len ( test_img ) > 0: 
  missing_img_list = [i for i in missing_img_list if i not in os.listdir(test_img)]

print ( len ( missing_img_list))
sorted( list ( missing_img_list ))


for i in missing_img_list: 
  os.system( 'scp -r ' + os.path.join(original_source,i) + ' ' + os.path.join(check_these_img) ) # copy over 

# ---------------------------------------------------------------------------- #

# ---------------------------------------------------------------------------- # 

# ! copy missing to @new_source 
for i in missing_img_list: 
  os.system( 'scp ' + os.path.join(original_source,i) + ' ' + os.path.join(new_source) ) # copy over 

# ---------------------------------------------------------------------------- # 

# ! check test images are strictly unique from train images. 
x1 = set (os.listdir(new_source))
x2 = set (os.listdir(test_img))

assert len ( x1.intersection(x2) ) == 0
assert len ( x2.intersection(x1) ) == 0

