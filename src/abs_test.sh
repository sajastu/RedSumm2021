
BERT_DATA_PATH=/home/code-base/user_space/datasets/reddit-tifu/bert-data/
MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-reddit-1024-BertAbs/


 python train.py -task abs -mode validate \
                -batch_size 3000 -test_batch_size 10 \
                -bert_data_path $BERT_DATA_PATH \
                -log_file ../logs/val_abs_bert_cnndm \
                -model_path $MODEL_PATH -sep_optim true \
                -use_interval true -visible_gpus 0,1,2,3 \
                -max_pos 1024 -max_length 128 \
                -alpha 0.95 -min_length 20 \
                -result_path ../logs/abs_bert_cnndm
