import json

import pandas as pd
import random

from utils.rouge_score import evaluate_rouge

df = pd.read_csv('../results/bertsum_ext_vs_abs.csv')

rg_dict_sample = {
    'id':[],
    'src':[],
    'gold':[],
    'pred_pegasus':[],
    'rg1': [],
    'rg2':[],
    'rgL':[],
}

preds = []
with open('/home/code-base/user_space/saved_models/pegasus1/full_pred.json', mode='r') as f:
    for l in f:
        preds.append(json.loads(l.strip()))

bin_size = len(preds) // 100

i = 0
iter = 0
while i<len(preds):
    start_idx = i
    end_idx = (iter*bin_size) + (i+bin_size)
    if end_idx > len(df):
        end_idx = len(df)

    rand_int = random.randint(start_idx, end_idx)

    rg_dict_sample['id'].append(preds[rand_int]['id'].replace('[PAD]', ''))
    rg_dict_sample['src'].append(preds[rand_int]['text'])
    rg_dict_sample['gold'].append(preds[rand_int]['summary'])
    rg_dict_sample['pred_pegasus'].append(preds[rand_int]['pred'])
    rg_dict_sample['rg1'].append(evaluate_rouge([preds[rand_int]['pred']], [preds[rand_int]['summary']])[0])
    rg_dict_sample['rg2'].append(evaluate_rouge([preds[rand_int]['pred']], [preds[rand_int]['summary']])[1])
    rg_dict_sample['rgL'].append(evaluate_rouge([preds[rand_int]['pred']], [preds[rand_int]['summary']])[2])
    i+= bin_size
    iter+=1


df = pd.DataFrame(rg_dict_sample, columns= ['id', 'src', 'rg_l_ext', 'gold', 'pred_pegasus', 'rg1', 'rg2', 'rgL'])
df.to_csv(r'pegasus_sample.csv', index=False, header=True)
