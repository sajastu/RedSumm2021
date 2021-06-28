import json

BASE_DIR = '/home/code-base/user_space/packages/datasets/reddit_tifu/'
# BASE_DIR = '/home/code-base/user_space/datasets/reddit-tifu/json-line/'

for set in ['train', 'validation', 'test']:
    i = 0
    json_file = open(f'{BASE_DIR}/{set}.json', mode='w')
    instances = []

    with open(f'{BASE_DIR}/{set}.source') as fS, open(
            f'{BASE_DIR}/{set}.target') as fT:
        for s, t in zip(fS, fT):
            if len(s.strip()) > 0:
                src = s.replace('<n>', '').replace('\n', '').strip()
                tgt = t.replace('<n>', '').replace('\n', '').strip()

                if 'test' in set:
                    instances.append({'id': f'{set}-{i}', 'document': src, 'summary': tgt})
                else:
                    instances.append({'document': src, 'summary': tgt})
                i += 1

    for inst in instances:
        json.dump(inst, json_file)
        json_file.write('\n')
