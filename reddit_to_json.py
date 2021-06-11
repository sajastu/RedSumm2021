import json

for set in ['train', 'validation', 'test']:
    i = 0
    json_file = open(f'/home/code-base/user_space/datasets/reddit-tifu/splits-pegasus/reddit_tifu/{set}.json', mode='a')
    with open(f'/home/code-base/user_space/datasets/reddit-tifu/splits-pegasus/reddit_tifu/{set}.source') as fS, open(
            f'/home/code-base/user_space/datasets/reddit-tifu/splits-pegasus/reddit_tifu/{set}.target') as fT:
        for s, t in zip(fS, fT):
            json.dump({'id': f'{set}-{i}', 'text': s.strip(), 'summary': t.strip()}, json_file)
            json_file.write('\n')
