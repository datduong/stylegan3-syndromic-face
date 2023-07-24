

source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37

module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sbatch --partition=gpu --time=1:00:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=6 
# sinteractive --time=3:00:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8


# ! make json label 
cd /data/duongdb/stylegan3-FaceSyndromes/FaceSyndromes/PrepareData
datapath=/data/duongdb/WS22qOther_12082021

previous_path=/data/duongdb/WS22qOther_08102021/Classify
normal_fin='normal-img-gan-fold0.csv,normal-img-gan-fold1.csv,normal-img-gan-fold2.csv,normal-img-gan-fold3.csv,normal-img-gan-fold4.csv'
# syndrome_fin=train+blankcenter+WS+22q11DS+Control+Normal+Split.csv # ! train 
syndrome_fin=train+blankcenter+WS+22q11DS+Control+Normal+Split.csv,test+blankcenter+WS+22q11DS+Control+Normal+Split.csv # ! test+train together


csvjsonbasename=train+testWS22qOther10kNormalGenderNpr0 # ! NAME OF CSV AND JSON

json_path=$datapath/$csvjsonbasename.json
new_df_path=$datapath/$csvjsonbasename.csv

# python3 MakeLabelJson.py --json_path $json_path --previous_path $previous_path --normal_fin $normal_fin --syndrome_fin $syndrome_fin --new_df_path $new_df_path 

gender_csv='/data/duongdb/FairFace/age_ws_22q_controls_format.csv,/data/duongdb/FairFace/FairFace-aligned-60k-agegroup-06012021-BlankBackgroundCenter-label_formated.csv'

python3 MakeLabelJson.py --json_path $json_path --previous_path $previous_path --normal_fin $normal_fin --syndrome_fin $syndrome_fin --new_df_path $new_df_path --gender_csv $gender_csv --np_round_digit 0 --reduce_normal_fraction 0

# --reduce_normal_fraction 0.5 --gender_csv $gender_csv

# --skip_normal --disease='WS,22q11DS,Controls'

cd $datapath

# ! make data into pytorch image datast 
datapath=/data/duongdb/

source_in=$datapath/WS22qOther_08102021/Align512BlankBackgroundCenter

upsample=10

for resolution in 1024 # 1024 256
do 

  csvjsonbasename=WS22qOther10kNormalGenderNpr0 # ! NAME OF CSV INPUT AND JSON

  dest_folder=$datapath/WS22qOther_12082021/Res$resolution$csvjsonbasename'Up'$upsample

  img_csv=$datapath/WS22qOther_12082021/$csvjsonbasename.csv
  meta_fname=$datapath/WS22qOther_12082021/$csvjsonbasename.json

  cd /data/duongdb/stylegan3-FaceSyndromes
  python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname --upsample-label 'WS,22q11DS,Control' --upsample-time $upsample

  # python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname 

done 

cd $dest_folder

