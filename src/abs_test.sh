
MODEL_IDENTIFIER=presum-reddit-1024-bertExtAbs-base/

#BERT_DATA_PATH=/disk1/sajad/datasets/reddit/tldr-9+/bert-files/
BERT_DATA_PATH=/disk1/sajad/datasets/reddit/tldr-9+/tmp_files//tldr-9+/bert-data-0/
#MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-reddit-1024-BertAbs/
MODEL_PATH=/disk1/sajad/saved_models/bertabs-tldr9/
#MODEL_PATH=/disk1/sajad/saved_models/bertabs-tldrQ/

mkdir -p results/$MODEL_IDENTIFIER
python3 train.py -task abs -mode test \
                -batch_size 50000 -test_batch_size 1200 \
                -bert_data_path $BERT_DATA_PATH \
                -log_file ../logs/val_abs_bert_cnndm \
                -model_path $MODEL_PATH -sep_optim true \
                -use_interval true -visible_gpus 0,1 \
                -max_pos 1024 -max_length 128 -max_tgt_len 128 \
                -alpha 0.95 -min_length 50 \
                -result_path $MODEL_PATH/redditAbsNew.128 \
                -test_from $MODEL_PATH/model_step_1200000.pt