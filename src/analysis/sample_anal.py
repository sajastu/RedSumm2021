
import pandas as pd
import random


df = pd.read_csv('../results/bertsum_ext_vs_abs.csv')

rg_dict_sample = {
    'raw_src':[],
    'pred_ext':[],
    'rg_l_ext':[],
    'pred_abs':[],
    'rg_l_abs': [],
    'gold':[],
    'rg_diff':[],
}

bin_size = len(df) // 100

i = 0
iter = 0
while i<len(df):
    start_idx = i
    end_idx = (iter*bin_size) + (i+bin_size)
    if end_idx > len(df):
        end_idx = len(df)

    rand_int = random.randint(start_idx, end_idx)
    rg_dict_sample['raw_src'].append(df.iloc[rand_int]['raw_src'].replace('[PAD]', ''))
    rg_dict_sample['pred_ext'].append(df.iloc[rand_int]['pred_ext'])
    rg_dict_sample['rg_l_ext'].append(df.iloc[rand_int]['rg_l_ext'])
    rg_dict_sample['pred_abs'].append(df.iloc[rand_int]['pred_abs'])
    rg_dict_sample['rg_l_abs'].append(df.iloc[rand_int]['rg_l_abs'])
    rg_dict_sample['gold'].append(df.iloc[rand_int]['gold'])
    rg_dict_sample['rg_diff'].append(df.iloc[rand_int]['RG-L-Diff'])
    i+= bin_size
    iter+=1


df = pd.DataFrame(rg_dict_sample, columns= ['raw_src', 'pred_ext', 'rg_l_ext', 'pred_abs', 'rg_l_abs', 'gold', 'rg_diff'])
df.to_csv (r'../results/bertsum_ext_vs_abs_sample.csv', index=False, header=True)
