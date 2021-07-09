# extractive setting



export BERT_DATA_PATH=/home/code-base/user_space/datasets/reddit-tifu/bert-data/
#export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-reddit-1024-cnnFinetuned
export MODEL_PATH=/home/code-base/user_space/saved_models/bertsum/presum-reddit-512-bertExt-base-test/


python train.py -task ext -mode train \
                          -bert_data_path $BERT_DATA_PATH -ext_dropout 0.1 -model_path $MODEL_PATH \
                          -lr 2e-3 -visible_gpus 0 -report_every 50 -save_checkpoint_steps 1000 \
                          -batch_size 1500 -train_steps 100000 -accum_count 2 \
                          -log_file ../logs/ext_bert_reddit -use_interval true -warmup_steps 10000 -max_pos 512
