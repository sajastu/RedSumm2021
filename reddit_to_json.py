import json

# BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'
BASE_DIR = '/home/code-base/user_space/datasets/reddit-tifu/json-line/'

for set in ['train', 'validation', 'test']:
    i = 0
    json_file = open(f'{BASE_DIR}/{set}.json', mode='a')
    srcs = []
    tgts = []

    with open(f'{BASE_DIR}/{set}.source') as fS, open(
            f'{BASE_DIR}/{set}.target') as fT:
        for s, t in zip(fS, fT):
            if len(s.strip()) > 0:
                json.dump(
                    {'id': f'{set}-{i}', 'text': s.replace('\n', ' ').strip(), 'summary': t.replace('\n', ' ').strip()},
                    json_file)
                json_file.write('\n')
