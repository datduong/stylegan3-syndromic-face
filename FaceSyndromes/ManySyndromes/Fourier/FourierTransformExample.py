

import sys,os,pickle
from tkinter import image_names
import numpy as np
import cv2
from matplotlib import pyplot as plt

imgpath = 'C:/Users/duongdb/Documents/ManyFaceConditions01072022/Align1024BlankBackgroundCenter'

# image_name = 'KSSlide63' # 'CdLSSlide4' # 'BWSSlide70'

# ['22q11DS', 'BWS', 'CdLS', 'Down', 'KS', 'NS', 'Normal', 'PWS', 'RSTS1', 'WHS', 'WS']

image_name_list = "PWSSlide3 BWSSlide12 PWSSlide20 BWSSlide32 BWSSlide70 BWSSlide22 CdLSSlide4 CdLSSlide55 DownSlide21 DownSlide88 KSSlide54 KSSlide63 NSSlide82 NSSlide105 PWSSlide18 PWSSlide98 RSTS1Slide2 RSTS1Slide3 WHSSlide34 WHSSlide88".split() 

image_name_list = sorted([n.strip() for n in image_name_list])

for image_name in image_name_list: 
    
  img = cv2.imread(os.path.join(imgpath,image_name+'.png'),0)

  dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)

  # magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))
  magnitude_spectrum, phase = cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1])


  plt.subplot(121),plt.imshow(img, cmap = 'gray')
  plt.title('Input Image'), plt.xticks([]), plt.yticks([])
  # plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
  plt.subplot(122),plt.imshow(phase, cmap = 'gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.savefig('C:/Users/duongdb/Documents/ManyFaceConditions01072022/'+image_name+'_fftphase.png')


# ! normal obama 

img = cv2.imread(os.path.join('C:/Users/duongdb/Documents/100-shot-obama/29.jpg'),0)

dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

magnitude_spectrum, phase = cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1])


magnitude_spectrum, phase = 20*np.log(cv2.cartToPolar(dft_shift[:,:,0],dft_shift[:,:,1]))

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(phase, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.savefig('C:/Users/duongdb/Documents/ManyFaceConditions01072022/obama_fft.png')

# ! celeb 

import re 
# img = cv2.imread(os.path.join('C:/Users/duongdb/Documents/CelebA/Example/24.jpg'),0)

path = 'C:/Users/duongdb/Documents/CelebA/Example'
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
  plt.savefig(os.path.join('C:/Users/duongdb/Documents/ManyFaceConditions01072022/Celeb/',re.sub(r'\.jpg','',imgname)+'_fft.png'))


# ! WS + 22q 

imgpath = 'C:/Users/duongdb/Documents/WS22qOther_08102021/Align512BlankBackgroundCenter'

image_name_list = "22q11DS_early106_22q11DSyoungchild 22q11DS_inter10_22q11DSyoungchild WS_inter37_WSadolescence WS_inter112_WSyoungchild WS_late143_WSolderadult 22q11DS_late213_22q11DSyoungchild".split() 

image_name_list = sorted([n.strip() for n in image_name_list])

for image_name in image_name_list: 
    
  img = cv2.imread(os.path.join(imgpath,image_name+'.png'),0)

  dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
  dft_shift = np.fft.fftshift(dft)

  magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

  plt.subplot(121),plt.imshow(img, cmap = 'gray')
  plt.title('Input Image'), plt.xticks([]), plt.yticks([])
  plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
  plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
  plt.savefig('C:/Users/duongdb/Documents/ManyFaceConditions01072022/'+image_name+'_fft.png')


# ! NF1

img = cv2.imread(os.path.join('C:/Users/duongdb/Documents/SkinConditionImages07092021/Crop/NF1/TrimWhiteSpaceNoBorder/NF1Slide211.jpg'),0)

dft = cv2.dft(np.float32(img),flags = cv2.DFT_COMPLEX_OUTPUT)
dft_shift = np.fft.fftshift(dft)

magnitude_spectrum = 20*np.log(cv2.magnitude(dft_shift[:,:,0],dft_shift[:,:,1]))

plt.subplot(121),plt.imshow(img, cmap = 'gray')
plt.title('Input Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(magnitude_spectrum, cmap = 'gray')
plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
plt.savefig('C:/Users/duongdb/Documents/ManyFaceConditions01072022/NF1Slide211_fft.png')


