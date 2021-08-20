# import json
# import os
# from multiprocessing import Pool, cpu_count
#
# from tqdm import tqdm
#
# def mp_read(param):
#     ids= []
#     with open(param) as fR:
#         for l in tqdm(fR):
#             try:
#                 ent = json.loads(l.strip())
#                 ids.append(ent['id'])
#             except:
#                 continue
#     return ids
#
# json_file_w = open('/tmp/th22_splits_m2.txt', mode='w')
#
# for m in ['m2']:
#     id_files = []
#     c=0
#     for root, dirs, files in os.walk(f'/home/code-base/user_space/trainman-k8s-storage-349d2c46-5192-4e7b-8567-ada9d1d9b2de/tldrQ/dataset-{m}/', topdown=False):
#         for name in files:
#             if '.json' in name:
#                 id_files.append(os.path.join(root, name))
#
#     print('reading entire dataset...')
#     pool = Pool(cpu_count())
#     all_ids = []
#     for out in tqdm(pool.imap_unordered(mp_read, id_files), total=len(id_files)):
#         all_ids.extend(out)
#
#
#     pool.close()
#     pool.join()
#
#     for id in all_ids:
#         json_file_w.write(id)
#         json_file_w.write('\n')




import glob
import json
import os
from bisect import bisect_left
from multiprocessing import cpu_count, Pool
import torch
from tqdm import tqdm

with open('/tmp/th22_splits.json') as fR:
    splits = json.load(fR)

splits['test'] = sorted(splits['test'])
splits['validation'] = sorted(splits['validation'])
splits['train'] = sorted(splits['train'])

def bi_contains(lst, item):
    """ efficient `item in lst` for sorted lists """
    # if item is larger than the last its not in the list, but the bisect would
    # find `len(lst)` as the index to insert, so check that first. Else, if the
    # item is in the list then it has to be at index bisect_left(lst, item)
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)


def _mp_read(file):
    dataset = torch.load(file)
    out = []

    for d in dataset:

        for split, files in splits.items():
            if bi_contains(files, d['id']):
                out.append((d, split))

    return out




bert_dir = '/home/code-base/lrg_split_machines/bert-data-m_2/'
bert_write = '/home/code-base/lrg_split_machines/bert-data-m_2-tldrQ/'

if not os.path.exists(bert_write):
    os.makedirs(bert_write)

files = []
for f in glob.glob(bert_dir + '*.pt'):
    files.append(f)

pool = Pool(cpu_count())

train, validation, test = [], [], []
train_c, validation_c, test_c = 0, 0, 0
for outs in tqdm(pool.imap_unordered(_mp_read, files), total=len(files)):
    for o in outs:
        eval('o[1]').append(o[0])

to_be_written = []
for d in tqdm(train):
    to_be_written.append(d)
    train_c+=1
    if train_c%50000==0:
        torch.save(to_be_written, bert_write + 'train.' + str(train_c / 50000) + '.pt')
        to_be_written = []

for d in tqdm(validation):
    to_be_written.append(d)
    validation_c+=1
    if train_c%50000==0:
        torch.save(to_be_written, bert_write + 'train.' + str(validation_c / 50000) + '.pt')
        to_be_written = []

for d in tqdm(test):
    to_be_written.append(d)
    test_c+=1
    if train_c%50000==0:
        torch.save(to_be_written, bert_write + 'train.' + str(test_c / 50000) + '.pt')
        to_be_written = []










