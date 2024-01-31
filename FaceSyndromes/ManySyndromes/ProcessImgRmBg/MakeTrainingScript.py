import time,os,sys,re,pickle
from datetime import datetime

# ---------------------------------------------------------------------------- #

# ! make the training script for StyleGAN2-Ada

script = """#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh 
conda activate py37

module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# ---------------------------------------------------------------------------- #

datapath=/data/duongdb/ManyFaceConditions08172022

img_folder=$datapath/IMG_FOLDER

outdir=$datapath/Stylegan3Model/OUT_FOLDER

# ---------------------------------------------------------------------------- #

# ! note, loading models: https://github.com/NVlabs/stylegan3/issues/23#issuecomment-970706600
# ! https://catalog.ngc.nvidia.com/orgs/nvidia/teams/research/models/stylegan3/files

nvidia_pretrain=/data/duongdb/stylegan3-FaceSyndromes/NvidiaPretrainedModel/stylegan2-ffhq-256x256.pkl

# ---------------------------------------------------------------------------- #

# ! follow instruction on hyper-parameters at https://github.com/NVlabs/stylegan3/blob/main/docs/configs.md
# ! batch=32 at res=256 may be okay with 2gpus, batch 24 takes 10/16gb 
# ! batch=16 at res=1024 hits 15/16gb with 2 gpus 

# ---------------------------------------------------------------------------- #

# ! train 

cd /data/duongdb/stylegan3-FaceSyndromes

python train.py --outdir=$outdir --data=$img_folder \
--resume=$nvidia_pretrain \
--cfg=stylegan2 --gpus=4 --batch=64 --gamma=0.2048 --glr=0.0025 --dlr=0.0025 --cbase=16384 \
--kimg=10000 --snap=10 \
--mirror=1 \
--aug=ada \
--cond=True \
--label_embed_dim=512 \
--metrics=fid5k_full \
--label_combo_dict='{"label1":[0,11],"label2":[11,16],"label3":[16,18]}' \
--label_emb_dict='{"label1":256,"label2":128,"label3":128}' \

# ---------------------------------------------------------------------------- #

"""

now = datetime.now() # current date and time
date_time = now.strftime("%m%d%Y%H%M%S")

os.chdir('/data/duongdb/ManyFaceConditions08172022')

IMG_FOLDER = 'Res256AlignPix0-NoExternalUp1-4' # ! input folder: image resolution 256x256, aligned, no background (pix_val=0 for background), no external data added to our own datasets, increase weight of rarer diseases to. 
 
OUT_FOLDER = IMG_FOLDER # ! make life easy, set output folder name as same name of input


newscript = re.sub('IMG_FOLDER',IMG_FOLDER,script)
newscript = re.sub('OUT_FOLDER',OUT_FOLDER,newscript)
fname = 'script'+date_time+'.sh'
fout = open(fname,'w')
fout.write(newscript)
fout.close()


os.system('sbatch --partition=gpu --time=16:00:00 --gres=gpu:p100:4 --mem=32g --cpus-per-task=12 '+fname) # ! submit script to GPU

