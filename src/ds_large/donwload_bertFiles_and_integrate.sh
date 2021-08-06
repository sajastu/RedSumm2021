

##################  Configs

export STORE_DIR=/home/code-base/large_reddit_bertfiles/
mkdir -p $STORE_DIR

# m0
URL_m0=https://drive.google.com/file/d/17t1ADPuRdiyDUdTULDtRj59vpviVgAOO/edit

# m1
URL_m1=https://drive.google.com/file/d/19tenZFat7Sj1_gLaHg1iKf7_Ng_L2Jmj/edit

# m2, m3
URL_m3=https://drive.google.com/file/d/1-PuqDptfdrCQAXSetJkKK-Oj8cj27Ri3/edit

# m4
URL_m4=https://drive.google.com/file/d/1MZEqFf0_77TDzdWE3PgFnKOzjSeeGXl-/edit

################## first Download bertFiles [m0, ..., m4]
curr=pwd
cd $STORE_DIR
perl /tmp/RedSumm2021/src/ds_large/gdown/gdownload.pl  $URL_m0 m0-bertFiles.tar
perl /tmp/RedSumm2021/src/ds_large/gdown/gdownload.pl  $URL_m1 m1-bertFiles.tar
perl /tmp/RedSumm2021/src/ds_large/gdown/gdownload.pl  $URL_m3 m3-bertFiles.tar
perl /tmp/RedSumm2021/src/ds_large/gdown/gdownload.pl  $URL_m4 m4-bertFiles.tar


################## Uncompressing bertfiles, should note that it should not interfere names

tar -xf $STORE_DIR/m0-bertFiles.tar --directory $STORE_DIR/
tar -xf $STORE_DIR/m1-bertFiles.tar --directory $STORE_DIR/
tar -xf $STORE_DIR/m2-bertFiles.tar --directory $STORE_DIR/
tar -xf $STORE_DIR/m3-bertFiles.tar --directory $STORE_DIR/