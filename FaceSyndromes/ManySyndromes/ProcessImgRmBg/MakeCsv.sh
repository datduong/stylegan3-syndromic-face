
source /data/$USER/conda/etc/profile.d/conda.sh
conda activate py37
module load CUDA/11.0
module load cuDNN/8.0.3/CUDA-11.0
module load gcc/8.3.0

# sbatch --partition=gpu --time=2-00:00:00 --gres=gpu:v100x:2 --mem=24g --cpus-per-task=24 
# sbatch --partition=gpu --time=2:30:00 --gres=gpu:p100:1 --mem=8g --cpus-per-task=8 
# sinteractive --time=1:30:00 --gres=gpu:p100:1 --mem=4g --cpus-per-task=4

# ---------------------------------------------------------------------------- #
# ! make csv 
datapath=/data/duongdb/ManyFaceConditions08172022/
codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 
extracsv=/data/duongdb/WS22qOther_12082021/train+testWS22qOther10kNormalGenderNpr0.csv # ! add more images, have to call normal in @ManyCondition+10kNormal.csv even if we don't use normal
cd $codepath
python3 MakeCsv.py --filelist 'BWS.csv,CdLS.csv,Down.csv,KS.csv,NS.csv,PWS.csv,RSTS1.csv,WHS.csv,Unaffected.csv' --outputname $datapath/'ManyCondition+10kNormal.csv' --imagepath $datapath/Align1024RmBgCenter --extracsv $extracsv --headfolder '/data/duongdb/ManyFaceConditions08172022'


# ---------------------------------------------------------------------------- #
# ! make csv not adding in normal "free on internet" faces 
datapath=/data/duongdb/ManyFaceConditions08172022/
codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 

cd $codepath
python3 MakeCsv.py --filelist 'BWS.csv,CdLS.csv,Down.csv,KS.csv,NS.csv,PWS.csv,RSTS1.csv,WHS.csv,Unaffected.csv,22q11DS.csv,WS.csv' --outputname $datapath/'ManualMetaDataLabel.csv' --imagepath $datapath/TrimImg_no_bg_0pix_align --headfolder '/data/duongdb/ManyFaceConditions08172022'



# ---------------------------------------------------------------------------- #
# ! make json 
datapath=/data/duongdb/ManyFaceConditions08172022/
codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 
cd $codepath
experimentname=ManyCondition-Normal-Other # -SkipAge-SkipGender
json_path=$datapath/$experimentname.json
csv_label=$datapath/ManyCondition+10kNormal.csv
new_df_path=$datapath/$experimentname.csv
# keeps only @disease
python3 MakeLabelJson.py --json_path $json_path --csv_label $csv_label --disease 'WS,22q11DS,BWS,CdLS,Down,KS,NS,PWS,RSTS1,WHS,Unaffected' --new_df_path $new_df_path --gender --skip_controls --skip_normal 

# --skip_age --gender

# ---------------------------------------------------------------------------- #
# ! make data into pytorch image dataset 
# ! can be done separately if we just change resolution 

datapath=/data/duongdb/

source_in=$datapath/ManyFaceConditions08172022/Align1024RmBgCenter/

upsample='1-4'

# '{"label1":[0,11],"label2":[11,16],"label3":[16,18]}'


for resolution in 1024 # 1024 256
do 

  csvjsonbasename=ManyCondition-Normal-Other-RmBg # ! NAME OF CSV INPUT AND JSON -SkipAge-SkipGender

  dest_folder=$datapath/ManyFaceConditions08172022/Res$resolution$csvjsonbasename'Up'$upsample

  img_csv=$datapath/ManyFaceConditions08172022/$csvjsonbasename.csv
  meta_fname=$datapath/ManyFaceConditions08172022/$csvjsonbasename.json

  cd /data/duongdb/stylegan3-FaceSyndromes
  python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname --upsample-label-dict '{"22q11DS":1, "BWS":4, "CdLS":4, "Down":4, "KS":4, "NS":4, "PWS":4, "RSTS1":4, "Unaffected":4, "WHS":4, "WS":1}'

  # '{"22q11DS":1, "BWS":4, "CdLS":4, "Down":4, "KS":4, "NS":4, "PWS":4, "RSTS1":4, "Unaffected":4, "WHS":4, "WS":1}'
  # '{"22q11DS":2, "BWS":10, "CdLS":10, "Down":10, "KS":10, "NS":10, "PWS":10, "RSTS1":10, "WHS":10, "WS":2}'
  # '{"22q11DS":4, "BWS":20, "CdLS":20, "Down":20, "KS":20, "NS":20, "PWS":20, "RSTS1":20, "WHS":20, "WS":4}'
  # python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname 

done 

cd $dest_folder


# ---------------------------------------------------------------------------- #
# ! make json from given csv 

datapath=/data/duongdb/ManyFaceConditions08172022/
codepath=$datadir/stylegan3-FaceSyndromes/FaceSyndromes/ManySyndromes # ! 
cd $codepath
experimentname=AlignPix255-NoExternal-Bg # -SkipAge-SkipGender
json_path=$datapath/$experimentname.json
csv_label=$datapath/TrimImg_255pix_align08172022_manual_auto_age_gender_race.csv
new_df_path=$datapath/$experimentname.csv
# keeps only @disease
python3 MakeLabelJson.py --json_path $json_path --csv_label $csv_label --disease 'WS,22q11DS,BWS,CdLS,Down,KS,NS,PWS,RSTS1,WHS,Unaffected' --new_df_path $new_df_path --skip_controls --skip_normal # --skip_age
cd $datapath

datapath=/data/duongdb/
source_in=$datapath/ManyFaceConditions08172022/TrimImg_align_255pix/
upsample='1-4'

for resolution in 256 # 1024 256
do 

  csvjsonbasename=$experimentname # ! NAME OF CSV INPUT AND JSON -SkipAge-SkipGender

  dest_folder=$datapath/ManyFaceConditions08172022/Res$resolution$csvjsonbasename'Up'$upsample

  img_csv=$datapath/ManyFaceConditions08172022/$csvjsonbasename.csv
  meta_fname=$datapath/ManyFaceConditions08172022/$csvjsonbasename.json

  cd /data/duongdb/stylegan3-FaceSyndromes
  python dataset_tool.py --source $source_in --dest $dest_folder --resolution=$resolution'x'$resolution --img-csv $img_csv --meta-fname $meta_fname --upsample-label-dict '{"22q11DS":1, "BWS":1, "CdLS":3, "Down":1, "KS":2, "NS":2, "PWS":4, "RSTS1":4, "Unaffected":3, "WHS":2, "WS":1}'

done 

cd $dest_folder



