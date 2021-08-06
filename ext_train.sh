# extractive setting



export BERT_DATA_PATH=/home/code-base/large_reddit_bertfiles/
export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/bertExt-reddit-1024/

mkdir -p logs

python train.py -task ext -mode train \
                          -bert_data_path $BERT_DATA_PATH -ext_dropout 0.1 -model_path $MODEL_PATH \
                          -lr 2e-3 -visible_gpus 0,1,2,3,4,5,6,7 -report_every 50 -save_checkpoint_steps 1000 \
                          -batch_size 34000 -train_steps 1000000 -accum_count 2 \
                          -log_file logs/ext_bert_reddit.log -use_interval true -warmup_steps 20000 -max_pos 1024
