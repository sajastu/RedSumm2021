

##################  Configs

export STORE_DIR=/home/code-base/large_reddit_bertfiles/
mkdir -p $STORE_DIR

# m0
https://drive.google.com/open?id=17t1ADPuRdiyDUdTULDtRj59vpviVgAOO

# m1

# m2

# m3

# m4


################## first Download bertFiles [m0, ..., m4]
perl gdown.pl/gdown.pl  $STORE_DIR/m0-bertFiles.tar
perl gdown.pl/gdown.pl  $STORE_DIR/m1-bertFiles.tar
perl gdown.pl/gdown.pl  $STORE_DIR/m3-bertFiles.tar
perl gdown.pl/gdown.pl  $STORE_DIR/m4-bertFiles.tar


################## Uncompressing bertfiles, should note that it should not interfere names

tar -xf $STORE_DIR/m0-bertFiles.tar
tar -xf $STORE_DIR/m1-bertFiles.tar
tar -xf $STORE_DIR/m2-bertFiles.tar
tar -xf $STORE_DIR/m3-bertFiles.tar

#python united_bert_files.py $STORE_DIR