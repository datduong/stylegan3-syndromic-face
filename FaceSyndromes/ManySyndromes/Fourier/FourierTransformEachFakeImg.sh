#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

datadir=/data/duongdb

codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 

mainpath=/data/duongdb/ManyFaceConditions01312022/Stylegan3Model/Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pklInterpolate

for class in '0' '1' '2' '3' '4' '5' '6' '7' '8' '9' '10' 
do 
imgpath=$mainpath/$class',11,16T.7Static'
foutdir=$mainpath/'fft_'$class',11,16T.7Static'
mkdir $foutdir
cd $codepath
python3 FourierTransformEachFakeImg.py --imgpath $imgpath --foutdir $foutdir
done 



# sbatch --time=8:30:00 --mem=4g --cpus-per-task=6 
# sbatch --partition=gpu --time=2:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4

