import json

BASE_DIR = '/home/code-base/user_space/saved_models/bart/reddit-xsum-1024-tuned/checkpoint-58000/'

steps_score = {}

with open(BASE_DIR + 'trainer_state.json') as F:

    all_logs = json.load(F)


for a in all_logs['log_history']:
    if 'eval_rougeL' in a.keys():
        steps_score[a['step']] = a['eval_rougeL']
# import pdb;pdb.set_trace()

sorted = sorted(steps_score.items(), key=lambda item: item[1], reverse=True)

for s in sorted:
    print(s)
    print('\n')