
#some configs
#pip3 install spacy
#python3 -m spacy download en_core_web_sm


#
## m0
#file_id=1Xzr3ZUbWLTcxFPUdTAsKwsL_T0PHLSHk #my_machine
#
## m1
#file_id=18cSS5U1CxyvlaTGeKupZaRXg8Ud9RLuL #Franck -bart

## m2
file_id=1oRbSyy-aZ3aJ2eVW3KLZLbBfuaCuIm6v #my_machine

## m3
##file_id=1Xzr3ZUbWLTcxFPUdTAsKwsL_T0PHLSHk #my_machine

## m4
##file_id=1Xzr3ZUbWLTcxFPUdTAsKwsL_T0PHLSHk #my_machine

##

id=m_2

DS_BASE_DIR=/home/code-base/lrg_split_s/
#mkdir -p $DS_BASE_DIR


pip install gdown
current=pwd
cd $DS_BASE_DIR
gdown --id $file_id -O $DS_BASE_DIR/
#
echo "uncompressing"
tar -xf $id.tar
cd $current

##
### java, do this manually
### conda install -c anaconda openjdk
##
##
### set up Stanford coreNlp
#

wget -O stanford-corenlp-4.2.2.zip https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip
unzip stanford-corenlp-4.2.2.zip
mkdir -p /home/code-base/toolkits/
mv stanford-corenlp-4.2.2 /home/code-base/toolkits
export CLASSPATH=/home/code-base/toolkits/stanford-corenlp-4.2.2/stanford-corenlp-4.2.2.jar
#source /root/.bashrc


### now preprocessing

mkdir -p /tmp/RedSumm2021/src/logs/

#mkdir -p $DS_BASE_DIR/splits
mkdir -p $DS_BASE_DIR/tokenized
mkdir -p $DS_BASE_DIR/jsons
mkdir -p $DS_BASE_DIR/bert-data
#

export RAW_PATH=$DS_BASE_DIR/$id/
export TOKENIZED_PATH=$DS_BASE_DIR/tokenized/
export JSON_PATH=$DS_BASE_DIR/jsons/
export BERT_DATA_PATH=$DS_BASE_DIR/bert-data/

# PREPARING DATA
python /tmp/RedSumm2021/src/preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python /tmp/RedSumm2021/src/preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 64 -use_bert_basic_tokenizer false
python /tmp/RedSumm2021/src/preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 64 -log_file ../logs/preprocess.log


echo "Compressing bert-files"
tar -cf $id_bertfiles.tar $BERT_DATA_PATH

