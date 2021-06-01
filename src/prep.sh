

export RAW_PATH=/home/code-base/user_space/datasets/reddit-tifu/splits/
export TOKENIZED_PATH=/home/code-base/user_space/datasets/reddit-tifu/tokenized-all/
export JSON_PATH=/home/code-base/user_space/datasets/reddit-tifu/jsons/
export BERT_DATA_PATH=/home/code-base/user_space/datasets/reddit-tifu/bert-data/

#python preprocess.py -mode tokenize -raw_path $RAW_PATH -save_path $TOKENIZED_PATH
python preprocess.py -mode format_to_lines -raw_path $TOKENIZED_PATH -save_path $JSON_PATH -n_cpus 20 -use_bert_basic_tokenizer false
python preprocess.py -mode format_to_bert -raw_path $JSON_PATH -save_path $BERT_DATA_PATH  -lower -n_cpus 20 -log_file ../logs/preprocess.log



# extractive setting
python train.py -task ext -mode train -bert_data_path $BERT_DATA_PATH -ext_dropout 0.1 -model_path $MODEL_PATH -lr 2e-3 -visible_gpus 0,1 -report_every 50 -save_checkpoint_steps 2000 -batch_size 3000 -train_steps 50000 -accum_count 2 -log_file ../logs/ext_bert_reddit -use_interval true -warmup_steps 10000 -max_pos 1024
