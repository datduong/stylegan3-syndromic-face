

import sys,os,pickle
from tkinter import image_names
import numpy as np
import cv2
from matplotlib import pyplot as plt

import re 

path = 'C:/Users/duongdb/Documents/NF1BeforeAfterInter03182021/aligned_images_late'
imglist = os.listdir(path)
for imgname in imglist : 

  img = cv2.imread(os.path.join(path,imgname),0)

  dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)

  magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  plt.subplot(121),plt.imshow(img, cmap = 'gray')
  plt.title('Input Image'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.savefig(os.path.join('C:/Users/duongdb/Documents/ManyFaceConditions01072022/NF1/',re.sub(r'\.png','',imgname)+'_fft.png'))


