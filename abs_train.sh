
export BERT_DATA_PATH=/home/code-base/user_space/trainman-k8s-storage-9f2785bf-6c50-4c4a-867d-d14eaac0b2bf/bert-data/
export MODEL_PATH=/home/code-base/user_space/trainman-k8s-storage-9f2785bf-6c50-4c4a-867d-d14eaac0b2bf/saved_models/bertsum/BertAbs-reddit-1024-tldrQ/
mkdir -p logs

python src/train.py -task abs -mode train \
                -bert_data_path $BERT_DATA_PATH -dec_dropout 0.2  -model_path $MODEL_PATH \
                -sep_optim true -lr_bert 0.002 -lr_dec 0.1 -save_checkpoint_steps 25000 \
                -batch_size 30 -test_batch_size 200 -train_steps 1500000 -report_every 100 -accum_count 1 \
                -use_bert_emb true -use_interval true -warmup_steps_bert 20000 \
                -warmup_steps_dec 10000 -max_pos 1024 -visible_gpus 0,1,2,3,4,5,6,7  \
                -log_file logs/abs_bert_reddit
#                -train_from /home/code-base/user_space/saved_models/bertsum/BertAbs-reddit-1024/model_step_600000.pt