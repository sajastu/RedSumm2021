import json

MODEL_BASE_DIR = '/home/code-base/user_space/saved_models/bart/reddit-xsum-1024-tuned/'
pred_file = MODEL_BASE_DIR + '/generated_predictions.txt'

# DS_BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'
DS_BASE_DIR = '/home/code-base/user_space/packages/datasets/reddit_tifu/'

test_file = f'{DS_BASE_DIR}/test.json'

preds = []
with open(pred_file) as fP:
    for l in fP:
        preds.append(l.strip())


json_with_pred_file = open(MODEL_BASE_DIR + '/full_pred.json', mode='a')

with open(test_file) as fJ:
    for j, l in enumerate(fJ):
        ent = json.loads(l.strip())
        ent['pred'] = preds[j]
        json.dump(ent, json_with_pred_file)
        json_with_pred_file.write('\n')
