


python3 train.py -task abs \
                -mode oracle \
                -test_batch_size 10000 \
                -bert_data_path /disk1/sajad/datasets/social/tldrQ/bert-data-0/ \
                -log_file ../logs/val_ext \
                -model_path /disk1/sajad/sci-trained-models/presum/bertExt-reddit-512-tldrQ/ \
                -sep_optim true \
                -use_interval true \
                -visible_gpus 0 \
                -max_pos 512 \
                -max_length 128 \
                -alpha 0.95 \
                -min_length 5 \
                -finetune_bert False \
                -result_path /disk1/sajad/sci-trained-models/presum/bertExt-reddit-512-tldrQ/bertExt.1 \
                -test_from /disk1/sajad/sci-trained-models/presum/bertExt-reddit-512-tldrQ/model_step_500000.pt \
