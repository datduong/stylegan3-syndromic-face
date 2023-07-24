

import enum
import sys,os,pickle,re
from tkinter import image_names
import numpy as np
import cv2
from matplotlib import pyplot as plt

from PIL import Image

import pandas as pd 
from tqdm import tqdm 

# foutdir = '/data/duongdb/ManyFaceConditions01072022/FourierTransform'
# imgpath = '/data/duongdb/ManyFaceConditions01072022/Align1024BlankBackgroundCenter'

foutdir = '/data/duongdb/ManyFaceConditions01072022/FourierTransform'
imgpath = '/data/duongdb/WS22qOther_08102021/Align512BlankBackgroundCenter'


img_list = os.listdir(imgpath)

# ['22q11DS', 'BWS', 'CdLS', 'Down', 'KS', 'NS', 'Normal', 'PWS', 'RSTS1', 'WHS', 'WS']
label_list =  ['22q11DS', 'BWS', 'CdLS', 'Down', 'KS', 'NS', 'PWS', 'RSTS1', 'WHS', 'WS']


if not os.path.exists(foutdir): 
  os.mkdir(foutdir)

for label in tqdm(label_list): 

  image_name_list = []
  for i in img_list: 
    if bool ( re.findall('^'+label, i) ) : 
      image_name_list.append(i)

  if len(image_name_list) == 0: 
    continue
  
  image_name_list = sorted([n.strip() for n in image_name_list])

  # Build up average pixel intensities, casting each image as an array of floats
  for index, im in enumerate(image_name_list):
    im = os.path.join(imgpath,im)
    if index == 0 :
      arr = np.array(Image.open(im).convert('RGB'),dtype=np.float)
    else: 
      try: 
        arr = arr + np.array(Image.open(im).convert('RGB'),dtype=np.float)
      except: 
        pass

  # Round values in array and cast as 8-bit integer
  arr=np.array(np.round(arr/len ( image_name_list ) ),dtype=np.uint8)

  arr2=Image.fromarray(arr,mode="RGB")
  arr2.save(os.path.join(foutdir,label+"_ave.png"))
      
  # 
  img_col = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR) 
  img = cv2.cvtColor(img_col, cv2.COLOR_BGR2GRAY)
  cv2.imwrite(os.path.join(foutdir,label+"_ave_gray.png"), img)

  # ! fourier 
  dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)

  magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  plt.subplot(121),plt.imshow(img_col)
  plt.title('Ave Img'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.savefig(os.path.join(foutdir,label+'_fft.png'))

