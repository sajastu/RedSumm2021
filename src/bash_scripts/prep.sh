

export RAW_PATH=/home/code-base/user_space/datasets/reddit-tifu/raw/
export TOKENIZED_PATH=/home/code-base/user_space/datasets/reddit-tifu/tokenized/

python ../preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH

