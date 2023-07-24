
import os,sys,re,pickle

mapping = {
  # '8,15,160,15,16T0.6':'YoungChildGirlUnaff22q_unaff',
  # '8,15,1610,15,16T0.6':'YoungChildGirlUnaffWS_unaff',
  # '8,15,161,15,16T0.6': 'YoungChildGirlUnaffBWS_unaff',
  # '8,15,162,15,16T0.6': 'YoungChildGirlUnaffCdLS_unaff',
  # '8,15,163,15,16T0.6': 'YoungChildGirlUnaffDown_unaff',
  '8,15,164,15,16T0.6': 'YoungChildGirlUnaffKS_unaffSetting0.6',
  '8,15,165,15,16T0.6': 'YoungChildGirlUnaffNS_unaffSetting0.6',
  # '8,15,166,15,16T0.6': 'YoungChildGirlUnaffPWS_unaff',
  # '8,15,167,15,16T0.6': 'YoungChildGirlUnaffRSTS1_unaff',
  # '8,15,169,15,16T0.6': 'YoungChildGirlUnaffWHS_unaff',
  # '8,15,170,15,17T0.6':'YoungChildBoyUnaff22q_unaff',
  # '8,15,1710,15,17T0.6':'YoungChildBoyUnaffWS_unaff',
  # '8,15,171,15,17T0.6': 'YoungChildBoyUnaffBWS_unaff',
  # '8,15,172,15,17T0.6': 'YoungChildBoyUnaffCdLS_unaff',
  # '8,15,173,15,17T0.6': 'YoungChildBoyUnaffDown_unaff',
  '8,15,174,15,17T0.6': 'YoungChildBoyUnaffKS_unaffSetting0.6',
  '8,15,175,15,17T0.6': 'YoungChildBoyUnaffNS_unaffSetting0.6',
  # '8,15,176,15,17T0.6': 'YoungChildBoyUnaffPWS_unaff',
  # '8,15,177,15,17T0.6': 'YoungChildBoyUnaffRSTS1_unaff',
  # '8,15,179,15,17T0.6': 'YoungChildBoyUnaffWHS_unaff',
}

# maindir = '/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/Res256AlignPix0-NoExternalUp1-4/00001-stylegan2-Res256AlignPix0-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001209.pklInterpolate'

maindir = '/data/duongdb/ManyFaceConditions08172022/Stylegan3Model/Res256AlignPix255-NoExternalUp1-4/00000-stylegan2-Res256AlignPix255-NoExternalUp1-4-gpus4-batch64-gamma0.2048-multilabel/network-snapshot-001330.pklInterpolate'

file_list = [ i for i in os.listdir (maindir) if i.endswith('0.6') ] 
for f in file_list : 
  if f in mapping: 
    os.system( 'mv ' + os.path.join(maindir,f) + ' ' + os.path.join(maindir,mapping[f]) )


#






