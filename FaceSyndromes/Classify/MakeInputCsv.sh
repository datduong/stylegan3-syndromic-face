#!/bin/bash

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sinteractive --time=2:00:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8
# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:p100:2 --mem=24g --cpus-per-task=24 

#----------------------------------------------------------------------------
# ! generate images, using labels indexing
# ! let's try same random vector, but different label class

 /data/duongdb/WS22qOther_12082021/Stylegan3Model/Res256WS22qOther10kNormalGenderNpr0
00000-stylegan2-Res256WS22qOther10kNormalGenderNpr0-gpus4-batch64-gamma0.2048-multilabel network-snapshot-008064.pkl 6.808743232942438

 /data/duongdb/WS22qOther_12082021/Stylegan3Model/Res256WS22qOther10kNormalGenderNpr2
00000-stylegan2-Res256WS22qOther10kNormalGenderNpr2-gpus4-batch64-gamma0.2048-multilabel network-snapshot-004233.pkl 7.074362280544196

 /data/duongdb/WS22qOther_12082021/Stylegan3Model/Res256WS22qOther2500NormalGenderNpr2Up2
00000-stylegan2-Res256WS22qOther2500NormalGenderNpr2Up2-gpus4-batch64-gamma0.2048-multilabel network-snapshot-006249.pkl 8.31637625385269

 /data/duongdb/WS22qOther_12082021/Stylegan3Model/Res256WS22qOther2500NormalGenderNpr0Up2
00000-stylegan2-Res256WS22qOther2500NormalGenderNpr0Up2-gpus4-batch64-gamma0.2048-multilabel network-snapshot-007862.pkl 7.95499424065086

 /data/duongdb/WS22qOther_12082021/Stylegan3Model/Res256WS22qOther2500NormalGenderNpr0Up5
00000-stylegan2-Res256WS22qOther2500NormalGenderNpr0Up5-gpus4-batch64-gamma0.2048-multilabel network-snapshot-005040.pkl 8.917018466742118

 /data/duongdb/WS22qOther_12082021/Stylegan3Model/Res256WS22qOther2500NormalGenderNpr2Up5
00000-stylegan2-Res256WS22qOther2500NormalGenderNpr2Up5-gpus4-batch64-gamma0.2048-multilabel network-snapshot-003830.pkl 9.306245712477157

/data/duongdb/WS22qOther_12082021/Stylegan3Model/Res1024WS22qOther10kNormalGenderNpr0Up10
00000-stylegan2-Res1024WS22qOther10kNormalGenderNpr0Up10-gpus4-batch16-gamma5-multilabel network-snapshot-005200.pkl 7.36291857187342
00001-stylegan3-t-Res1024WS22qOther10kNormalGenderNpr0Up10-gpus4-batch16-gamma6.6-multilabel network-snapshot-004560.pkl 7.057475733595947

cd /data/duongdb/stylegan3-FaceSyndromes

cd FaceSyndromes/Classify 

run_path=/data/duongdb/WS22qOther_12082021/Stylegan3Model

for mod in Res1024WS22qOther10kNormalGenderNpr0Up10/00000-stylegan2-Res1024WS22qOther10kNormalGenderNpr0Up10-gpus4-batch16-gamma5-multilabel/network-snapshot-005200.pkl
do 

folder_path=$run_path/$mod'Interpolate'
# '4,[0-9]+,6,[0-9]+T0.6M.'
# ',9[0-9]+,[0-9]+,10T0.6M.' 

folder_keyword='8Static'
csv_output_name='FakeStaticTestT0.8.csv'

python3 MakeInputCsv.py --folder_path $folder_path --folder_keyword $folder_keyword --csv_output_name $csv_output_name --exclude_str 'yes'

done 

