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


dlatents_dict=/data/duongdb/ManyFaceConditions01312022/ExampleProjection/projection-wplus-wavgstart-sgan2.pickle

style='0-14'
num_ws=14 

label1='Unaffected'

for label2 in PWS # BWS CdLS Down KS NS PWS RSTS1 WHS WS 22q11DS

do 

  direction_output=/data/duongdb/ManyFaceConditions01312022/ExampleProjection/projection-wplus-wavgstart-sgan2-direction$style$label1$label2.pickle

  losstype=hinge

  cd /data/duongdb/stylegan3-FaceSyndromes/FaceEdit
  python3 LogitRegression.py --dlatents_dict $dlatents_dict --num_ws $num_ws --style $style --direction_output $direction_output --losstype $losstype --label1 $label1 --label2 $label2



  #----------------------------------------------------------------------------
  # ! generate image from W space and using direction vector 

  cd /data/duongdb/stylegan3-FaceSyndromes

  workdir=/data/duongdb/ManyFaceConditions01312022

  direction_output=$workdir/ExampleProjection/projection-wplus-wavgstart-sgan2-direction$style$label1$label2.pickle

  wdir=$workdir/ExampleProjection/projection-wplus-wavgstart-sgan2

  network=$workdir/Stylegan3Model/Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pkl

  outdir=$workdir/ExampleProjection/$label1$label2
  mkdir $outdir

  for scale in .3 .4 .5 #  .7 .8 .9 1 1.1 1.2 0
  # 0 -.1 -.2 -.3 -.4 -.5 -.6 -.7 -.8 -.9 -1 
  do 
    # WS_early179_WSyoungchild WS_early178_WSyoungchild WS_early15_WS2y WS_early188_WS2y WS_early151_WS2y
    # 22q11DS_early15_22q11DSyoungchild 22q11DS_early105_22q11DSyoungchild 22q11DS_inter27_22q11DSyoungchild 22q11DS_inter120_22q11DSadolescence 22q11DS_early120_22q11DSyoungchild

    for img in UnaffectedSlide114 UnaffectedSlide115 UnaffectedSlide116 UnaffectedSlide125 UnaffectedSlide48 UnaffectedSlide20 UnaffectedSlide3
    do 
    projected_w=$wdir/projected$img'_wplus_wavg_final.npy' # projectedWS_early178_WSyoungchild_wplus_wavg_final.npy

    # noise = const or none or random

    python generate.py images --projected-w=$projected_w \
    --network=$network \
    --trunc=.8 \
    --noise-mode='const' \
    --outdir=$outdir \
    --direction-vec=$direction_output \
    --direction-scale=$scale \
    --description='generate-images-scale'$scale
    done 
  done 

  echo $outdir


done 
