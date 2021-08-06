

##################  Configs

export STORE_DIR=/home/code-base/large_reddit_bertfiles/
mkdir -p $STORE_DIR

# m0
URL_m0=https://drive.google.com/file/d/17t1ADPuRdiyDUdTULDtRj59vpviVgAOO/edit

# m1
URL_m1=https://drive.google.com/file/d/19tenZFat7Sj1_gLaHg1iKf7_Ng_L2Jmj/edit

# m2
URL_m2=https://drive.google.com/file/d/12GhzLqRxBzciBbbSOkv2XzaChzGBT3r2/edit

# m3
URL_m3=https://drive.google.com/file/d/1u5IDMSV8uc34o0bx9B9FjkQOUf7K-RjD/edit

# m4
URL_m4=https://drive.google.com/file/d/1MZEqFf0_77TDzdWE3PgFnKOzjSeeGXl-/edit

################## first Download bertFiles [m0, ..., m4]
#perl gdown/gdownload.pl  $URL_m0 m0-bertFiles.tar
#perl gdown/gdownload.pl  $URL_m1 m1-bertFiles.tar
perl gdown/gdownload.pl  $URL_m2 m2-bertFiles.tar
perl gdown/gdownload.pl  $URL_m3 m3-bertFiles.tar
#perl gdown/gdownload.pl  $URL_m4 m4-bertFiles.tar

################## Uncompressing bertfiles, should note that it should not interfere names

#tar -xf m0-bertFiles.tar --directory $STORE_DIR/
#rm m0-bertFiles.tar

#tar -xf m1-bertFiles.tar --directory $STORE_DIR/
#rm m1-bertFiles.tar

tar -xf m2-bertFiles.tar --directory $STORE_DIR/
rm m2-bertFiles.tar

tar -xf m3-bertFiles.tar --directory $STORE_DIR/
rm m3-bertFiles.tar

#tar -xf m4-bertFiles.tar --directory $STORE_DIR/
#rm m4-bertFiles.tar

#perl gdown/gdownload.pl $URL_m3 m3-bertFiles.tar && tar -xf m3-bertFiles.tar --directory /home/code-base/large_reddit_bertfiles/
#perl gdown/gdownload.pl https://drive.google.com/file/d/1-PuqDptfdrCQAXSetJkKK-Oj8cj27Ri3/edit m3-bertFiles.tar