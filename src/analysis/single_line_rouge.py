import json

import pandas as pd

# from utils.rouge_score import evaluate_rouge
from analysis_utils.rouge_score import evaluate_rouge


def ensure_lines(arr_1,arr_2):
    pass



ext_summaries = {}
with open('../results/presum-reddit-1024-bertExt/bertExt_step8000.json') as F:
    for l in F:
        ent = json.loads(l.strip())
        ext_summaries[ent['id']] = [(ent['pred'], ent['gold'])]

all_summaries = {}
with open('../results/presum-reddit-1024-bertExtAbs-base/redditExtAbs.128.8000.gold') as F:
    for l in F:
        ent = json.loads(l.strip())
        id = ent['id']
        try:
            all_summaries[id] = {
                'src': ent['raw_src'],
                'pred_ext': ext_summaries[id][0],
                'pred_abs': ent['pred'],
                'gold': ent['gold'],
            }
        except:
            continue


rg_dict = {
    'raw_src':[],
    'pred_ext':[],
    'rg_l_ext':[],
    'pred_abs':[],
    'rg_l_abs': [],
    'gold':[],
}

for id, value in all_summaries.items():
    raw_src = value['src']
    pred_ext = value['pred_ext']
    pred_abs = value['pred_abs']
    gold = value['gold']

    rg_l_ext = evaluate_rouge([pred_ext], [gold])[-1]
    rg_l_abs = evaluate_rouge([pred_abs], [gold])[-1]

    rg_dict['raw_src'].append(raw_src)
    rg_dict['pred_ext'].append(pred_ext)
    rg_dict['rg_l_ext'].append(rg_l_ext)
    rg_dict['pred_abs'].append(pred_abs)
    rg_dict['rg_l_abs'].append(rg_l_abs)
    rg_dict['gold'].append(gold)

df = pd.DataFrame(rg_dict, columns= ['raw_src', 'pred_ext', 'rg_l_ext', 'pred_abs', 'rg_l_abs', 'gold'])
df.to_csv (r'../results/bertsum_ext_vs_abs.csv', index=False, header=True)
