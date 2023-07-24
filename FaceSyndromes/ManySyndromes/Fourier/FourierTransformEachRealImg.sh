#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

datadir=/data/duongdb

datapath=/data/duongdb/ManyFaceConditions01312022/
codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 

cd $codepath


mainpath=/data/duongdb/ManyFaceConditions01312022/

 
imgpath=$mainpath/RmBgAlign9Cond+WS22qTrain
foutdir=$mainpath/'fft_'RmBgAlign9Cond+WS22qTrain
mkdir $foutdir

csv=$mainpath/Classify/ManyCondition-Normal-Other-RmBg-train.csv # ! need detail age, so we call this file... probably need to redo input later
filtercol='detail_label'
filterval='2y'

for labelname in KS CdLS PWS RSTS1 WHS Down NS BWS WS 22q11DS
do
python3 FourierTransformEachFakeImg.py --csv $csv --filtercol $filtercol --filterval $filterval --imgpath $imgpath --foutdir $foutdir --labelname $labelname
done 



# parser.add_argument("--csv", type=str, default=None)
# parser.add_argument("--filtercol", type=str, default=None)
# parser.add_argument("--filterval", type=str, default=None)


# sbatch --time=24:30:00 --mem=8g --cpus-per-task=8 
# sbatch --partition=gpu --time=2:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4

# BWS      
# CdLS     
# Down     
# KS       
# NS       
# PWS      
# RSTS1    
# WHS      