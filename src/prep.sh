

export RAW_PATH=/home/code-base/user_space/datasets/reddit-tifu/splits/
export TOKENIZED_PATH=/home/code-base/user_space/datasets/reddit-tifu/tokenized-all/
export JSON_PATH=/home/code-base/user_space/datasets/reddit-tifu/jsons/
export BERT_DATA_PATH=/home/code-base/user_space/datasets/reddit-tifu/bert-data/
export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-reddit-1024

# PREPARING DATA
#python preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
#python preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 20 -use_bert_basic_tokenizer false
#python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 20 -log_file ../logs/preprocess.log



