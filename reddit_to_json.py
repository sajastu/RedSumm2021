import json

BASE_DIR = '/home/code-base/user_space/packages/datasets/reddit_tifu/'
# BASE_DIR = '/home/code-base/user_space/datasets/reddit-tifu/json-line/'

for set in ['train', 'val', 'test']:
    i = 0
    json_file = open(f'{BASE_DIR}/{set}.json', mode='a')
    srcs = []
    tgts = []

    with open(f'{BASE_DIR}/{set}.source') as fS, open(
            f'{BASE_DIR}/{set}.target') as fT:
        for s, t in zip(fS, fT):
            if len(s.strip()) > 0:
                src = s.replace('<n>', '').replace('\n', '').strip()
                tgt = t.replace('<n>', '').replace('\n', '').strip()

                if 'test' in set:
                    json.dump(
                        {'id': f'{set}-{i}', 'document': src, 'summary': tgt},
                        json_file)
                    json_file.write('\n')
                else:
                    json.dump(
                        {'document': src, 'summary': tgt},
                        json_file)
                    import pdb;

                    pdb.set_trace()
                    json_file.write('\n')

                i += 1
