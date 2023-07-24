

import enum
import sys,os,pickle,re
from tkinter import image_names
import numpy as np
import cv2
from matplotlib import pyplot as plt

from PIL import Image

import pandas as pd 
from tqdm import tqdm 

foutdir = '/data/duongdb/ManyFaceConditions01072022/FourierTransformEach'
imgpath = '/data/duongdb/ManyFaceConditions01072022/Align1024BlankBackgroundCenter'

# foutdir = '/data/duongdb/ManyFaceConditions01072022/FourierTransform'
# imgpath = '/data/duongdb/WS22qOther_08102021/Align512BlankBackgroundCenter'

# SHIFT_BY = 20

img_list = os.listdir(imgpath)

# ['22q11DS', 'BWS', 'CdLS', 'Down', 'KS', 'NS', 'Normal', 'PWS', 'RSTS1', 'WHS', 'WS']
# label_list =  ['22q11DS', 'BWS', 'CdLS', 'Down', 'KS', 'NS', 'PWS', 'RSTS1', 'WHS', 'WS']

label_list = ['BWS','CdLS']

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
  for index, im in tqdm ( enumerate(image_name_list) ):
    
    img = cv2.imread(os.path.join(imgpath,im),0)

    # ! fourier 
    dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)

    magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

    plt.subplot(121),plt.imshow(img, cmap = 'gray')
    plt.title('Img'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
    plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
    plt.savefig(os.path.join(foutdir,re.sub(r'\.png','',im)+'_fft.png'))


    # ! changing frequencies 
    rows, cols = img.shape
    crow, ccol = int(rows/2) , int(cols/2)

    for SHIFT_BY in [5,10,15,20,30,40,50] : 
      
      # create a mask 
      mask = np.ones((rows,cols,2),np.uint8) * 1000 # all 1 or 0 ? 
      mask[crow-SHIFT_BY:crow+SHIFT_BY, ccol-SHIFT_BY:ccol+SHIFT_BY] = 0 # set center as 0 ? 
      # apply mask and inverse DFT
      fshift = dft_shift*mask
      f_ishift = np.fft.ifftshift(fshift)
      img_back = cv2.idft(f_ishift)
      img_back = cv2.magnitude(img_back[:,:,0],img_back[:,:,1])

      magnitude_spectrum = 20*np.log(cv2.magnitude(fshift[:,:,0],fshift[:,:,1]))

      plt.subplot(121),plt.imshow(img_back, cmap = 'gray')
      plt.title('Img'), plt.xticks([]), plt.yticks([])
      plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
      plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
      plt.savefig(os.path.join(foutdir,re.sub(r'\.png','',im)+'_'+str(SHIFT_BY)+'_highfft.png'))

