
#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

#----------------------------------------------------------------------------
# ! after project images into W space (or W+ space) 
# ! we will now style-mix 

cd /data/duongdb/stylegan3-FaceSyndromes

workdir=/data/duongdb/ManyFaceConditions01312022

outdir=$workdir/ExampleProjection

w_npy=$workdir/ExampleProjection/SelectKSStyleMix

network=$workdir/Stylegan3Model/Res256ManyCondition-Normal-Other-RmBgUp1-4/00000-stylegan2-Res256ManyCondition-Normal-Other-RmBgUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001129.pkl


python3 style_mixing.py grid \
--network $network \
--outdir $outdir \
--trunc 0.25 \
--description StyleMixKS \
--row-seeds 4-8 \
--col-seeds 0-3 \
--styles 0-3 \
--W_vec_dir $w_npy



Unaff 
108 
90
112
122
129

KS 
113
85
27
5

