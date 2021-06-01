

export RAW_PATH=/home/code-base/user_space/datasets/reddit-tifu/splits/
export TOKENIZED_PATH=/home/code-base/user_space/datasets/reddit-tifu/tokenized-all/
export JSON_PATH=/home/code-base/user_space/datasets/reddit-tifu/jsons/

#python ../preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python ../preprocess.py -mode format_to_lines -raw_path $RAW_PATH -save_path $JSON_PATH -n_cpus 20 -use_bert_basic_tokenizer false -map_path MAP_PATH

