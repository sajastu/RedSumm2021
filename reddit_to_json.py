import codecs
import json

# BASE_DIR = '/home/code-base/user_space/packages/datasets/reddit_tifu/'
BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'

for set in ['train', 'val', 'test']:
    i = 0
    json_file = codecs.open(f'{BASE_DIR}/{set}.json', "w", "utf-8")
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
        json.dump(inst, json_file,ensure_ascii=False)
        json_file.write(u'\n')

    json_file.close()