import json

pred_file = '/home/code-base/user_space/saved_models/pegasus1/generated_predictions.txt'

BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'

test_file = f'{BASE_DIR}/test.json'

preds = []
with open(pred_file) as fP:
    for l in fP:
        preds.append(l.strip())


json_with_pred_file = open('/home/code-base/user_space/saved_models/pegasus1/full_pred.json', mode='a')

with open(test_file) as fJ:
    for j, l in enumerate(fJ):
        ent = json.loads(l.strip())
        ent['pred'] = preds[j]
        json.dump(ent, json_with_pred_file)
        json_with_pred_file.write('\n')
