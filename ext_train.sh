# extractive setting



export BERT_DATA_PATH=/disk1/sajad/datasets/social/tldrQ/bert-files/
export MODEL_PATH=/disk1/sajad/sci-trained-models/presum/bertExt-reddit-512-tldrQ/
mkdir -p logs

python src/train.py -task ext -mode train \
                          -bert_data_path $BERT_DATA_PATH -ext_dropout 0.1 -model_path $MODEL_PATH \
                          -lr 2e-3 -visible_gpus 0,1 -report_every 100 -save_checkpoint_steps 25000 \
                          -batch_size 5100 -test_batch_size 8000 -train_steps 1000000 -accum_count 2 \
                          -log_file logs/ext_bert_reddit.log -use_interval true -warmup_steps 20000 -max_pos 512
#                          -train_from /home/code-base/user_space/saved_models/bertsum/bertExt-reddit-1024/model_step_150000.pt
#0,1,2,3,4,5,6,7