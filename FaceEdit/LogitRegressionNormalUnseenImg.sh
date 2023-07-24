#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# ---------------------------------------------------------------------------- #

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

# ---------------------------------------------------------------------------- #

cd /data/duongdb/stylegan3-FaceSyndromes/FaceEdit

dlatents_dict=/data/duongdb/ManyFaceConditions01312022/NormalUnseenExampleRmBgAlign1024Projection/projection-wplus-wavgstart-sgan2.pickle

style='0-14'

direction_output=/data/duongdb/ManyFaceConditions01312022/ExampleProjectionWS22q/projection-wplus-wavgstart-sgan2-direction$style.pickle

num_ws=14 

losstype=hinge

# python3 LogitRegression.py --dlatents_dict $dlatents_dict --num_ws $num_ws --style $style --direction_output $direction_output --losstype $losstype



#----------------------------------------------------------------------------
# ! generate image from W space and using direction vector 

cd /data/duongdb/stylegan3-FaceSyndromes

workdir=/data/duongdb/ManyFaceConditions01312022

wdir=$workdir/NormalUnseenExampleRmBgAlign1024Projection/projection-wplus-wavgstart-sgan2

network=$workdir/Stylegan3Model/Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pkl

for scale in -.2 .2 -.4 .4
do 
  # WS_early179_WSyoungchild WS_early178_WSyoungchild WS_early15_WS2y WS_early188_WS2y WS_early151_WS2y
  for img in 'unnamed.jpg' '29.jpg' '78.jpg'
  do 
  projected_w=$wdir/projected$img'_wplus_wavg_final.npy' # projectedWS_early178_WSyoungchild_wplus_wavg_final.npy

  outdir=$workdir/NormalUnseenExampleRmBgAlign1024Projection

  python generate.py images --projected-w=$projected_w \
  --network=$network \
  --trunc=1 \
  --noise-mode='none' \
  --outdir=$outdir \
  --direction-vec=$direction_output \
  --direction-scale=$scale \
  --description='generate-images-scale'$scale
  done 
done 

echo $outdir

