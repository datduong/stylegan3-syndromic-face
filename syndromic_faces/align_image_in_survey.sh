#!/bin/bash

# ---------------------------------------------------------------------------- #

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0


# ---------------------------------------------------------------------------- #

resolution=720

codepath=/data/duongdb/stylegan3-syndromic-faces/syndromic_faces/ # ! 

headfolder=/data/duongdb/syndromic-faces-workdir/SurveyImgAlign
img_path=$headfolder/Noonan

colorcode=0

foutpath=$headfolder/Noonan_align_$colorcode'pix'

cd $codepath
python3 align_image.py --input_file_path $img_path --output_file_path $foutpath --output_size $resolution --centerface '0,0,720,720' --colorcode $colorcode --notblur --enable_padding

