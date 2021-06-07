
MODEL_IDENTIFIER=presum-reddit-1024-bertExtAbs-base/

BERT_DATA_PATH=/home/code-base/user_space/datasets/reddit-tifu/bert-data/
#MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-reddit-1024-BertAbs/
MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/$MODEL_IDENTIFIER

mkdir -p ../results/$MODEL_IDENTIFIER
python train.py -task abs -mode validate \
                -batch_size 1000 -test_batch_size 500 \
                -bert_data_path $BERT_DATA_PATH \
                -log_file ../logs/val_abs_bert_cnndm \
                -model_path $MODEL_PATH -sep_optim true \
                -use_interval true -visible_gpus 0,1,2 \
                -max_pos 1024 -max_length 128 -max_tgt_len 128 \
                -alpha 0.95 -min_length 50 \
                -result_path results/$MODEL_IDENTIFIER/redditExtAbs.128 \
                -test_all