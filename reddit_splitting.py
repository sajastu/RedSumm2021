
# import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf

import tensorflow_datasets as tfds
from tqdm import tqdm

split_patterns = {
    "train": "train[:80%]",
    "validation": "train[80%:90%]",
    "test": "train[90%:]"
}

for split in split_patterns.keys():
    split_list = []
    ds, info = tfds.load(
            "reddit_tifu/long",
            split=split_patterns[split],
            shuffle_files=False,
            with_info=True)

    for ex in ds:
        src = ex['documents'].numpy().decode("utf-8")
        tldr = ex['tldr'].numpy().decode("utf-8")
        split_list.append({'src': src, 'tldr': tldr})

    counter = 0
    print('writing to directory %s...' % f'raw_data/{split}')
    for doc in tqdm(split_list, total=len(split_list)):
        counter+=1
        with open(f'raw_data/{split}/{split}-{counter}.instance', mode='w') as f:
            f.write(doc['src'])
            f.write('\n')
            f.write('\n')
            f.write('@highlights')
            f.write('\n')
            f.write(doc['tldr'])



