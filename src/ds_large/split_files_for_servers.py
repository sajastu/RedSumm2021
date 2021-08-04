import glob
import os
import shutil

import numpy as np

all_tldr = []

for set in ["test", "validation", "train"]:
    for f in glob.glob(f'/home/code-base/tldr_dataset/splits/{set}/*'):
        all_tldr.append(f)

# split to sensei, considreing 5 machines.

bin_count = 5
bin_size = len(all_tldr) // 5
fromm = 0

m_0 = all_tldr[fromm:bin_size]
fromm = bin_size

m_1 = all_tldr[fromm:2*bin_size]
fromm = 2*bin_size

m_2 = all_tldr[fromm:3*bin_size]
fromm = 3*bin_size

m_3 = all_tldr[fromm:4*bin_size]
fromm = 4*bin_size

m_4 = all_tldr[fromm:]
fromm = bin_size

for key, files in {"m_0": m_0, "m_1": m_1, "m_2": m_2, "m_3": m_3, "m_4": m_4}.items():
    if not os.path.exists(f'/home/code-base/tldr_dataset/machine_splits/{key}'):
        os.makedirs(f'/home/code-base/tldr_dataset/machine_splits/{key}')

    for f in files:
        shutil.move(f, f'/home/code-base/tldr_dataset/machine_splits/{key}')