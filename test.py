import json
import os
from multiprocessing import Pool, cpu_count

from tqdm import tqdm

def mp_read(param):
    with open(param) as fR:
        for l in tqdm(fR):
            try:
                ent = json.loads(l.strip())
                return ent['id']
            except:
                continue

json_file_w = open('/tmp/th22_splits_m2.txt', mode='w')

for m in ['m2']:
    id_files = []
    c=0
    for root, dirs, files in os.walk(f'/home/code-base/user_space/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/tldrQ/dataset-{m}/', topdown=False):
        for name in files:
            if '.json' in name:
                id_files.append(os.path.join(root, name))

    print('reading entire dataset...')
    pool = Pool(cpu_count())

    for out in tqdm(pool.imap_unordered(mp_read, id_files), total=len(id_files)):
        json_file_w.write(out)

    pool.close()
    pool.join()