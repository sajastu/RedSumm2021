
#################  CONFIGS  #############################
export id=m_1

mkdir -p /tmp/RedSumm2021/src/logs/
mkdir -p $DS_BASE_DIR/tokenized
mkdir -p $DS_BASE_DIR/jsons
mkdir -p $DS_BASE_DIR/bert-data

export DS_BASE_DIR=/home/code-base/lrg_split_machines/
#export RAW_PATH=/home/code-base/tldr_dataset/machine_splits/$id
export RAW_PATH=$DS_BASE_DIR/$id/
export TOKENIZED_PATH=$DS_BASE_DIR/tokenized/
export JSON_PATH=$DS_BASE_DIR/jsons/
export BERT_DATA_PATH=$DS_BASE_DIR/bert-data-$id/

mkdir -p $DS_BASE_DIR

### file ids to be downloaded
## m0
#file_id=1Xzr3ZUbWLTcxFPUdTAsKwsL_T0PHLSHk # my_machine, finished
#
## m1
#file_id=18cSS5U1CxyvlaTGeKupZaRXg8Ud9RLuL #Franck -bart problematic!

## m2
#file_id=1oRbSyy-aZ3aJ2eVW3KLZLbBfuaCuIm6v # Franck's first, tokenizing finished

## m3
#file_id=1EeK3jfCbO-8r1_BBJWy-k7v_O0uB8IzO # Franck's first, tokenization [finished]

## m4
#file_id=1GUoZGWuzIVQlefwUxW1Tc-KOaEfL5s84 # Nicole's



################ download from Google drive  #############################

#if python -c 'import pkgutil; exit(not pkgutil.find_loader("gdown"))'; then
#    echo 'gdown found'
#else
#    echo 'gdown not found... installing'
#    pip install gdown
#fi
#
#if ! [ -f $DS_BASE_DIR/$file_id.tar ]
#then
#  gdown --id $file_id -O $DS_BASE_DIR/$file_id.tar
#fi
#
#
#if ! [ -d $DS_BASE_DIR/$id/ ]
#then
#  echo "Uncompressing $id.tar"
#  tar -xf $DS_BASE_DIR/$id.tar
#fi
#
#################### Set up Stanford coreNlp #############################
#
#if ! [ -f stanford-corenlp-4.2.2.zip ]
#then
##  wget -O stanford-corenlp-4.2.2.zip https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip
#  perl /home/code-base/lrg_split_machines/gdown.pl/gdown.pl https://drive.google.com/file/d/1mH34x7LF9RSYe6CSHP_lywbRBr2mon2B/edit stanford-corenlp-4.2.2.zip
#  cd $cur_dir
#fi
#
#if ! [ -d stanford-corenlp-4.2.2/ ]
#then
#  unzip stanford-corenlp-4.2.2.zip
#else
#  if [ -d /home/code-base/toolkits/stanford-corenlp-4.2.2/ ]
#  then
#    rm -rf /home/code-base/toolkits/stanford-corenlp-4.2.2/
#    mkdir -p /home/code-base/toolkits/
#    mv stanford-corenlp-4.2.2 /home/code-base/toolkits
#  fi
#fi
#
#
#

# don't comment
export CLASSPATH=/home/code-base/toolkits/stanford-corenlp-4.2.2/stanford-corenlp-4.2.2.jar



##################### Now preprocessing


#
#

#
#### PREPARING DATA
python /tmp/RedSumm2021/src/preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python /tmp/RedSumm2021/src/preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 64 -use_bert_basic_tokenizer false
python /tmp/RedSumm2021/src/preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 64 -log_file ../logs/preprocess.log

cd $DS_BASE_DIR
echo "Compressing bert-files at $BERT_DATA_PATH"
tar -cf $id-bertfiles.tar bert-data-$id/

gupload $DS_BASE_DIR/$id-bertfiles.tar

