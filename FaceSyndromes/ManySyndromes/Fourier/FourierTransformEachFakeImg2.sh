#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

datadir=/data/duongdb

datapath=/data/duongdb/ManyFaceConditions01072022/
codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 

cd $codepath


mainpath=/data/duongdb/ManyFaceConditions01072022/Stylegan3Model/Res256ManyCondition+10kNormal-Other-SkipAgeUp2-10/00001-stylegan2-Res256ManyCondition+10kNormal-Other-SkipAgeUp2-10-gpus2-batch64-gamma0.2048-multilabel/network-snapshot-001693.pklInterpolate

for class in '5' '6' '7' '8' '9' '10' 
do 
imgpath=$mainpath/$class',11T.9Static'
foutdir=$mainpath/'fft_'$class',11T.9Static'
mkdir $foutdir
python3 FourierTransformEachFakeImg.py --imgpath $imgpath --foutdir $foutdir
done 



# sbatch --time=4:30:00 --mem=4g --cpus-per-task=12 
# sbatch --partition=gpu --time=2:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4

