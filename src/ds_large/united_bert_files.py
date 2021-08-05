import glob
import os
import sys


def rename(store_dir):
    file_count = {'train':0, 'validation':0, 'test':0}
    files_abs_dir = []
    for root, dirs, files in os.walk(store_dir, topdown=False):
        for name in files:
            # print(os.path.join(root, name))
            file_count[name.split('.')[0]] += 1
            files_abs_dir.append(os.path.join(root, name))

    # renaming files
    for f in files_abs_dir:
        if 'train' in f:
            os.rename(f, '/'.join(f.split('/')[:-1]) + f'/train.{file_count["train"]-1}.pt')
        elif 'validation' in f:
            os.rename(f, '/'.join(f.split('/')[:-1]) + f'/validation.{file_count["validation"] - 1}.pt')
        elif 'test' in f:
            os.rename(f, '/'.join(f.split('/')[:-1]) + f'/test.{file_count["test"] - 1}.pt')

    # now mv'ing...


if __name__ == '__main__':
    store_dir = sys.argv[1]
    rename(store_dir)