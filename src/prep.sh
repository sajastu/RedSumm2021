

export RAW_PATH=/home/code-base/tldr_dataset/splits/
export TOKENIZED_PATH=/home/code-base/large_tldr_bert/tokenized-all-new/
export JSON_PATH=/home/code-base/large_tldr_bert/jsons/
export BERT_DATA_PATH=/home/code-base/large_tldr_bert/bert-data/
#export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-large-reddit-1024

# PREPARING DATA
python preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 60 -use_bert_basic_tokenizer false
python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 60 -log_file ../logs/preprocess.log



