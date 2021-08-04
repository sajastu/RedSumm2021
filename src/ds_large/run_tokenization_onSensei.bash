
#some configs
pip3 install spacy
python3 -m spacy download en_core_web_sm


id=m_0

# m0
file_id=1Xzr3ZUbWLTcxFPUdTAsKwsL_T0PHLSHk #my_machine

#pip install gdown
current=pwd
mkdir -p /home/code-base/mashine_split_lrg_reddit/
cd /home/code-base/mashine_split_lrg_reddit/
## fill_out id for $id
gdown --id $file_id -O /home/code-base/mashine_split_lrg_reddit/
#tar -xf /home/code-base/mashine_split_lrg_reddit/$id.tar
#
#cd $current
## java, do this manually
## conda install -c anaconda openjdk
#
#
## set up Stanford coreNlp

#wget -O stanford-corenlp-4.2.2.zip https://nlp.stanford.edu/software/stanford-corenlp-4.2.2.zip
#unzip stanford-corenlp-4.2.2.zip
#mkdir -p /home/code-base/toolkits/
#mv stanford-corenlp-4.2.2 /home/code-base/toolkits
#export CLASSPATH=/home/code-base/toolkits/stanford-corenlp-4.2.2/stanford-corenlp-4.2.2.jar
#source /root/.bashrc
#
#
## now preprocessing
#mkdir -p /home/code-base/lrg_split_s/$id/splits
#mkdir -p /home/code-base/lrg_split_s/$id/tokenized
#mkdir -p /home/code-base/lrg_split_s/$id/jsons
#mkdir -p /home/code-base/lrg_split_s/$id/bert-data

#DS_BASE_DIR=/home/code-base/lrg_split_s/$id/
#export RAW_PATH=$DS_BASE_DIR/splits/
#export TOKENIZED_PATH=$DS_BASE_DIR/tokenized/
#export JSON_PATH=$DS_BASE_DIR/jsons/
#export BERT_DATA_PATH=$DS_BASE_DIR/bert-data/
#cd ../
#
## PREPARING DATA
#python preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
#python preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 64 -use_bert_basic_tokenizer false
#python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 64 -log_file ../logs/preprocess.log

