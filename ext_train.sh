# extractive setting



export BERT_DATA_PATH=/home/code-base/user_space/trainman-k8s-storage-5ddccee4-32ad-4e32-ba2d-1d06b71f80b0/datasets/tldrQ/bert-files/
export MODEL_PATH=/home/code-base/user_space/trainman-k8s-storage-5ddccee4-32ad-4e32-ba2d-1d06b71f80b0/saved_models/bertsum/bertExt-tldrQ/
mkdir -p logs

python src/train.py -task ext -mode train \
                          -bert_data_path $BERT_DATA_PATH -ext_dropout 0.1 -model_path $MODEL_PATH \
                          -lr 2e-3 -visible_gpus 0,1,2,3,4,5,6,7 -report_every 100 -save_checkpoint_steps 25000 \
                          -batch_size 15000 -test_batch_size 15000 -train_steps 1000000 -accum_count 2 \
                          -log_file logs/ext_bert_reddit.log -use_interval true -warmup_steps 20000 -max_pos 512 \
                          -train_from $MODEL_PATH/model_step_25000.pt
#0,1,2,3,4,5,6,7