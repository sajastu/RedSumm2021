
#################  CONFIGS  #############################
id=m_0
DS_BASE_DIR=/home/code-base/lrg_split_machines/
mkdir -p $DS_BASE_DIR

### file ids to be downloaded
## m0
#file_id=1Xzr3ZUbWLTcxFPUdTAsKwsL_T0PHLSHk # my_machine
#
## m1
#file_id=18cSS5U1CxyvlaTGeKupZaRXg8Ud9RLuL #Franck -bart

## m2
#file_id=1oRbSyy-aZ3aJ2eVW3KLZLbBfuaCuIm6v # Franck's first

## m3
file_id=1EeK3jfCbO-8r1_BBJWy-k7v_O0uB8IzO #

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
#echo "Uncompressing $id.tar"
#tar -xf $DS_BASE_DIR/$id.tar


################### Set up Stanford coreNlp #############################

#if ! [ -f stanford-corenlp-4.2.2.zip ]
#then
#  wget -O stanford-corenlp-4.2.2.zip https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip
#fi
#
#unzip stanford-corenlp-4.2.2.zip
#rm stanford-corenlp-4.2.2.zip
#
#if [ -d /home/code-base/toolkits/stanford-corenlp-4.2.2/ ]
#then
#  rm -rf /home/code-base/toolkits/stanford-corenlp-4.2.2/
#fi
#
#mkdir -p /home/code-base/toolkits/
#mv stanford-corenlp-4.2.2 /home/code-base/toolkits
export CLASSPATH=/home/code-base/toolkits/stanford-corenlp-4.2.2/stanford-corenlp-4.2.2.jar



##################### Now preprocessing

mkdir -p /tmp/RedSumm2021/src/logs/
mkdir -p $DS_BASE_DIR/tokenized
mkdir -p $DS_BASE_DIR/jsons
mkdir -p $DS_BASE_DIR/bert-data


#export RAW_PATH=/home/code-base/tldr_dataset/machine_splits/$id
export RAW_PATH=$DS_BASE_DIR/$id/
export TOKENIZED_PATH=$DS_BASE_DIR/tokenized/
export JSON_PATH=$DS_BASE_DIR/jsons/
export BERT_DATA_PATH=$DS_BASE_DIR/bert-data/

### PREPARING DATA
python /tmp/RedSumm2021/src/preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python /tmp/RedSumm2021/src/preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 64 -use_bert_basic_tokenizer false
python /tmp/RedSumm2021/src/preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 64 -log_file ../logs/preprocess.log


echo "Compressing bert-files"
tar -cf $id_bertfiles.tar $BERT_DATA_PATH

