
export BERT_DATA_PATH=/home/code-base/large_reddit_bertfiles/
export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/BertAbs-reddit-1024
mkdir -p logs

python src/train.py -task abs -mode train \
                -bert_data_path $BERT_DATA_PATH -dec_dropout 0.2  -model_path $MODEL_PATH \
                -sep_optim true -lr_bert 0.002 -lr_dec 0.1 -save_checkpoint_steps 100 \
                -batch_size 40 -test_batch_size 90 -train_steps 1500000 -report_every 100 -accum_count 1 \
                -use_bert_emb true -use_interval true -warmup_steps_bert 20000 \
                -warmup_steps_dec 10000 -max_pos 1024 -visible_gpus 0,1,2,3,4,5,6,7  \
                -log_file logs/abs_bert_reddit