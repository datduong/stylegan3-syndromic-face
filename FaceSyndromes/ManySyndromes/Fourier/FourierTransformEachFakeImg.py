

from copy import deepcopy
import enum
import sys,os,pickle,re
from tkinter import image_names
import numpy as np
import cv2
from matplotlib import pyplot as plt

from PIL import Image

import pandas as pd 
from tqdm import tqdm 

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--imgpath", type=str, default=None)
parser.add_argument("--foutdir", type=str, default=None)
parser.add_argument("--labelname", type=str, default=None)
parser.add_argument("--csv", type=str, default=None)
parser.add_argument("--filtercol", type=str, default=None)
parser.add_argument("--filterval", type=str, default=None)


args = parser.parse_args()

if not os.path.exists(args.foutdir): 
  os.mkdir(args.foutdir)

image_name_list = os.listdir ( args.imgpath )
image_name_list = sorted([n.strip() for n in image_name_list])

if args.labelname is not None: 
  temp = []
  for i in image_name_list: 
    if bool(re.findall('^'+args.labelname,i)): 
      temp.append(i)
  # 
  image_name_list = deepcopy ( temp )


# ---------------------------------------------------------------------------- #

if args.csv is not None: 
  print ('number img before filter', len(image_name_list))
  df = pd.read_csv(args.csv)
  # df = df [ df[args.filtercol] == args.filterval ]
  df = df[df[args.filtercol].str.contains(args.filterval)]
  image_name_list = list ( set(df['name'].values).intersection(set(image_name_list)) ) 
  print ('number img after filter', len(image_name_list))
  
# ---------------------------------------------------------------------------- #


# Build up average pixel intensities, casting each image as an array of floats

for index, im in tqdm ( enumerate(image_name_list) ):
  
  img = cv2.imread(os.path.join(args.imgpath,im),0)

  # ! fourier 
  dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)

  magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  plt.subplot(121),plt.imshow(img, cmap = 'gray')
  plt.title('Img'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.savefig(os.path.join(args.foutdir,re.sub(r'\.png','',im)+'_fft.png'))


  # ! changing frequencies 
  rows, cols = img.shape
  crow, ccol = int(rows/2) , int(cols/2)

  for SHIFT_BY in [5,10,25,50] : 
    
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
    plt.savefig(os.path.join(args.foutdir,re.sub(r'\.png','',im)+'_'+str(SHIFT_BY)+'_highfft.png'))

