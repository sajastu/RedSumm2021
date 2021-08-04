

DS_BASE_DIR=/trainman-mount/trainman-k8s-storage-06a4f11e-8e1a-4301-8f5d-8b8b9e41ce4d/large_tldr_dataset/

export RAW_PATH=/home/code-base/tldr_dataset/splits/
export TOKENIZED_PATH=$DS_BASE_DIR/tokenized-all/
export JSON_PATH=$DS_BASE_DIR/jsons/
export BERT_DATA_PATH=$DS_BASE_DIR/bert-data/
#export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-large-reddit-1024

# PREPARING DATA
python preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 60 -use_bert_basic_tokenizer false
python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 60 -log_file ../logs/preprocess.log



