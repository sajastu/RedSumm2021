import json

BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'

for set in ['train', 'val', 'test']:
    i = 0
    json_file = open(f'{BASE_DIR}/{set}.json', mode='a')
    with open(f'{BASE_DIR}/{set}.source') as fS, open(
            f'{BASE_DIR}/{set}.target') as fT:
        for s, t in zip(fS, fT):
            json.dump(
                {'id': f'{set}-{i}', 'text': s.replace('\n', ' ').strip(), 'summary': t.replace('\n', ' ').strip()},
                json_file)
            json_file.write('\n')
