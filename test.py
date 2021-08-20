import json

from tqdm import tqdm

json_file_w = open('th22_splits.json', mode='w')

splits = {
    'test': [],
    'validation': [],
    'train': []
}

for set in ["test", "validation", "train"]:
    set_ids = []
    with open(f'/home/code-base/user_space/trainman-k8s-storage-c91414be-d3d1-431d-a2c8-1d040368c6e8/tldrQ/{set}.json') as fR:
        for l in tqdm(fR):
            set_ids.append(json.loads(l.strip())['id'])

    splits[set] = set_ids


json.dump(splits, json_file_w)
