
export BERT_DATA_PATH=/disk1/sajad/datasets/social/tldrQ/bert-files/
export MODEL_PATH=/disk1/sajad/sci-trained-models/presum/BertAbs-reddit-1024-tldrQ/
mkdir -p logs

python src/train.py -task abs -mode train \
                -bert_data_path $BERT_DATA_PATH -dec_dropout 0.2  -model_path $MODEL_PATH \
                -sep_optim true -lr_bert 0.002 -lr_dec 0.1 -save_checkpoint_steps 25000 \
                -batch_size 250 -test_batch_size 160 -train_steps 1000000 -report_every 100 -accum_count 1 \
                -use_bert_emb true -use_interval true -warmup_steps_bert 15000 \
                -warmup_steps_dec 30000 -max_pos 512 -visible_gpus 0,1,2,3,4,5,6,7  \
                -log_file logs/abs_bert_reddit
#                -train_from /home/code-base/user_space/saved_models/bertsum/BertAbs-reddit-1024/model_step_600000.pt