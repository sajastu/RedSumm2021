import gc
import glob
import json
import os
import random
import re
import shutil
import subprocess
from collections import Counter
from itertools import filterfalse
from os.path import join as pjoin

import torch
from multiprocess import Pool
from tqdm import tqdm

from others.logging import logger
from others.tokenization import BertTokenizer
# from pytorch_transformers import XLNetTokenizer

from others.utils import clean
from prepro.utils import _get_word_ngrams

import xml.etree.ElementTree as ET

format_to_linesnyt_remove_words = ["photo", "graph", "chart", "map", "table", "drawing"]


def recover_from_corenlp(s):
    s = re.sub(r' \'{\w}', '\'\g<1>', s)
    s = re.sub(r'\'\' {\w}', '\'\'\g<1>', s)


def load_json(p, lower):
    source = []
    tgt = []
    flag = False
    for sent in json.load(open(p))['sentences']:
        tokens = [t['word'] for t in sent['tokens']]
        if (lower):
            tokens = [t.lower() for t in tokens]
        if (tokens[0] == '@highlights'):
            flag = True
            tgt.append([])
            continue
        if (flag):
            tgt[-1].extend(tokens)
        else:
            source.append(tokens)

    source = [clean(' '.join(sent)).split() for sent in source]
    tgt = [clean(' '.join(sent)).split() for sent in tgt]
    return source, tgt, p.split('/')[-1]

def load_json_1(p, lower):
    source = []
    tgt = []
    # flag = False
    # for sent in json.load(open(p))['sentences']:
    #     tokens = [t['word'] for t in sent['tokens']]
    #     if (lower):
    #         tokens = [t.lower() for t in tokens]
    #     if (tokens[0] == '@highlights'):
    #         flag = True
    #         tgt.append([])
    #         continue
    #     if (flag):
    #         tgt[-1].extend(tokens)
    #     else:
    #         source.append(tokens)
    with open(p) as fR:
        for l in fR:
            doc = json.loads(l.strip())

            for sent in doc['src']:
                src_tokens = [t for t in sent]
                if (lower):
                    src_tokens = [t.lower() for t in src_tokens]
                source.append(src_tokens)

            for t_sent in doc['tgt']:
                tgt_tokens = [t for t in t_sent]
                if (lower):
                    tgt_tokens = [t.lower() for t in tgt_tokens]
                tgt.extend(tgt_tokens)

    source = [clean(' '.join(sent)).split() for sent in source]
    tgt = [clean(' '.join(sent)).split() for sent in tgt]
    id = p.split('/')[-1]
    return source, tgt, id


def load_xml(p):
    tree = ET.parse(p)
    root = tree.getroot()
    title, byline, abs, paras = [], [], [], []
    title_node = list(root.iter('hedline'))
    if (len(title_node) > 0):
        try:
            title = [p.text.lower().split() for p in list(title_node[0].iter('hl1'))][0]
        except:
            print(p)

    else:
        return None, None
    byline_node = list(root.iter('byline'))
    byline_node = [n for n in byline_node if n.attrib['class'] == 'normalized_byline']
    if (len(byline_node) > 0):
        byline = byline_node[0].text.lower().split()
    abs_node = list(root.iter('abstract'))
    if (len(abs_node) > 0):
        try:
            abs = [p.text.lower().split() for p in list(abs_node[0].iter('p'))][0]
        except:
            print(p)

    else:
        return None, None
    abs = ' '.join(abs).split(';')
    abs[-1] = abs[-1].replace('(m)', '')
    abs[-1] = abs[-1].replace('(s)', '')

    for ww in nyt_remove_words:
        abs[-1] = abs[-1].replace('(' + ww + ')', '')
    abs = [p.split() for p in abs]
    abs = [p for p in abs if len(p) > 2]

    for doc_node in root.iter('block'):
        att = doc_node.get('class')
        # if(att == 'abstract'):
        #     abs = [p.text for p in list(f.iter('p'))]
        if (att == 'full_text'):
            paras = [p.text.lower().split() for p in list(doc_node.iter('p'))]
            break
    if (len(paras) > 0):
        if (len(byline) > 0):
            paras = [title + ['[unused3]'] + byline + ['[unused4]']] + paras
        else:
            paras = [title + ['[unused3]']] + paras

        return paras, abs
    else:
        return None, None

def _add_set_to_filemaes(base_dir):
    for set in ['test', 'validation', 'train']:
        for f in tqdm(glob.glob(pjoin(base_dir, set, "*")), total=len(glob.glob(pjoin(base_dir, set, "*")))):
            if not f.split('/')[-1].startswith(set):
                new_file_name = set + '-' + f.split('/')[-1]
                os.rename(f, base_dir + '/' + set + '/'+ new_file_name)

def bi_contains(lst, item):
    """ efficient `item in lst` for sorted lists """
    # if item is larger than the last its not in the list, but the bisect would
    # find `len(lst)` as the index to insert, so check that first. Else, if the
    # item is in the list then it has to be at index bisect_left(lst, item)
    return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)



def tokenize(args):
    from bisect import bisect_left
    def bi_contains(lst, item):
        """ efficient `item in lst` for sorted lists """
        # if item is larger than the last its not in the list, but the bisect would
        # find `len(lst)` as the index to insert, so check that first. Else, if the
        # item is in the list then it has to be at index bisect_left(lst, item)
        return (item <= lst[-1]) and (lst[bisect_left(lst, item)] == item)


    stories_dir = os.path.abspath(args.raw_path)
    tokenized_stories_dir = os.path.abspath(args.save_path)

    prev_tokenized = []
    for f in glob.glob(os.path.abspath(args.prev_tokenized) + '/*'):
        prev_tokenized.append(f.split('/')[-1].replace('.json', '').lower())

    print('Sorting')
    prev_tokenized = sorted(prev_tokenized)
    print('Sorting done...')
    print("Preparing to tokenize %s to %s..." % (stories_dir, tokenized_stories_dir))
    stories = os.listdir(stories_dir)
    # make IO list file
    print("Making list of files to tokenize...")
    c=0
    with open("mapping_for_corenlp.txt", "w") as f:
        for s in tqdm(stories, total=len(stories)):
            # if '-tldr_' in s.lower() and not bi_contains(prev_tokenized, s.lower()):
            #     if '-tldr_' in s.lower():
                f.write("%s\n" % (os.path.join(stories_dir, s)))
                c+=1


    print(f'Actuall tokeninzing: {c}')

    command = ['java', 'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators', 'tokenize,ssplit',
               '-ssplit.newlineIsSentenceBreak', 'always', '-filelist', 'mapping_for_corenlp.txt', '-outputFormat',
               'json', '-outputDirectory', tokenized_stories_dir]

    print("Tokenizing %i files in %s and saving in %s..." % (len(stories), stories_dir, tokenized_stories_dir))
    subprocess.call(command)
    print("Stanford CoreNLP Tokenizer has finished.")
    os.remove("mapping_for_corenlp.txt")

    # Check that the tokenized stories directory contains the same number of files as the original directory
    num_orig = len(os.listdir(stories_dir))
    num_tokenized = len(os.listdir(tokenized_stories_dir))
    if num_orig != num_tokenized:
        raise Exception(
            "The tokenized stories directory %s contains %i files, but it should contain the same number as %s (which has %i files). Was there an error during tokenization?" % (
                tokenized_stories_dir, num_tokenized, stories_dir, num_orig))
    print("Successfully finished tokenizing %s to %s.\n" % (stories_dir, tokenized_stories_dir))


def tokenize_spacy(args):

    def _mp_tokenize_stanford(param):
        param = stories_dir + '/' + param.split('-')[0] +'/'+ param
        command = ['java', 'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators', 'tokenize,ssplit',
                   '-ssplit.newlineIsSentenceBreak', 'always', '-file', f'{param}', '-outputFormat',
                   'json', '-outputDirectory', tokenized_stories_dir]
        subprocess.call(command)

    def sentencizer(text):
        sents = []
        doc = nlp(text)
        sent_lst = doc.sents
        for sent in sent_lst:
            sents.append(sent.text)
        return sents

    # def _tokenize(src_sents):
    #     src_tkns = []
    #     for sent in src_sents:
    #         src_sentences_tkns = tokenizer.tokenize_text([sent])
    #         ctr = 0
    #         for _ in src_sentences_tkns: ctr += 1
    #         src_sentences_tkns_tmp = []
    #         if ctr > 1:
    #             src_sentences_tkns = tokenizer.tokenize_text([sent])
    #             for sT in src_sentences_tkns:
    #                 for tkn in sT:
    #                     src_sentences_tkns_tmp.append(tkn.text)
    #             src_sentences_tkns = src_sentences_tkns_tmp
    #         else:
    #             src_sentences_tkns = tokenizer.tokenize_text([sent])
    #             for sT in src_sentences_tkns:
    #                 for tkn in sT:
    #                     src_sentences_tkns_tmp.append(tkn.text)
    #             src_sentences_tkns = src_sentences_tkns_tmp
    #
    #         sent_tkns = []
    #         for token in src_sentences_tkns:
    #             sent_tkns.append(token)
    #         src_tkns.append(sent_tkns)
    #
    #     return src_tkns

    def _mp_tokenize(param):
        param_abs = stories_dir + '/' + param.split('-')[0] +'/'+ param
        src_txt = ''
        tgt_txt = ''
        tgt_flag = False
        with open(param_abs) as fR:
            for l in fR:
                if len(l.strip())>0:
                    if not tgt_flag and '@highlights' not in l:
                        src_txt += l.strip()
                        src_txt += ' '
                    elif '@highlights' in l:
                        tgt_flag = True
                        continue

                    if tgt_flag:
                        tgt_txt += l.strip()
                        tgt_txt += ' '
        src = sentencizer(src_txt.strip())
        tgt = sentencizer(tgt_txt.strip())

    def _read_file(param):
        param_abs = stories_dir + '/' + param.split('-')[0] + '/' + param
        src_txt = ''
        tgt_txt = ''
        tgt_flag = False
        with open(param_abs) as fR:
            for l in fR:
                if len(l.strip()) > 0:
                    if not tgt_flag and '@highlights' not in l:
                        src_txt += l.strip()
                        src_txt += ' '
                    elif '@highlights' in l:
                        tgt_flag = True
                        continue

                    if tgt_flag:
                        tgt_txt += l.strip()
                        tgt_txt += ' '

        return src_txt.strip() + '\n@highlights.\n' + tgt_txt.strip() + '\n@file_id.\n' + param


    stories_dir = os.path.abspath(args.raw_path)
    # _add_set_to_filemaes(stories_dir)

    tokenized_stories_dir = os.path.abspath(args.save_path)
    print("Preparing to tokenize %s to %s..." % (stories_dir, tokenized_stories_dir))

    stories = []

    for set in ['train', 'validation', 'test']:
        stories.extend([(f_name, set) for f_name in os.listdir(os.path.abspath(args.raw_path + '/'))])
        # stories.extend(os.listdir(os.path.abspath(args.raw_path+ '/' + set + '/')))
    # make IO list file

    # prev_tokenized = [s.replace('.json', '') for s in os.listdir(args.save_path)]

    print("Making list of files to tokenize...")
    to_be_tokenized = []
    # with open("mapping_for_corenlp.txt", "w") as f:
    #     f.write("%s\n" % (os.path.join(stories_dir, s.split('-')[0], s)))

    # pool_read = Pool(60)

    # for res in tqdm(pool_read.imap_unordered(_mp_read, stories[:1000]), total=len(stories[:1000])):
    #     if res != False:
    #         to_be_tokenized.append(res)
    #
    # pool_read.close()
    # import pdb;pdb.set_trace()
    file_ids = []
    for s in tqdm(stories[:3000], total=len(stories[:3000])):
        # if s not in prev_tokenized:
        to_be_tokenized.append(_read_file(s))
        file_ids.append(s)
        # to_be_tokenized.append(os.path.join(stories_dir, s.split('-')[0], s))
    #             f.write("%s\n" % (os.path.join(stories_dir, s.split('-')[0], s)))

    # to_be_tokenized = list(filterfalse(to_be_tokenized.__contains__, prev_tokenized))
                # f.write("%s\n" % (os.path.join(stories_dir, s[1], s[0])))

    print("Tokenizing %i files in %s and saving in %s..." % (len(stories), stories_dir, tokenized_stories_dir))
    # pool = Pool(64)

    # do it for src

    for doc in tqdm(nlp.pipe(to_be_tokenized, batch_size=500, n_process=64)):
        src_tokens = []
        tgt_tokens = []
        tgt_flg = False
        id_flg = False
        for sent in doc.sents:
            tokens = [t.text.lower() for t in sent]


            if ('@highlights' in tokens[1]):
                tgt_flg = True
                tgt_tokens.append([])
                continue

            if ('@file_id' in tokens[1]):
                tgt_flg = False
                id_flg = True
                continue

            if (tgt_flg):
                tokens = [t for t in tokens if len(t.strip())>0]
                tgt_tokens[-1].extend(tokens)
            elif (id_flg):
                file_id = ''.join(tokens)
                break
            else:
                src_tokens.append(tokens)

        json.dump({'src': src_tokens, 'tgt': tgt_tokens}, open(tokenized_stories_dir + '/' + file_id.strip() + '.json', mode='w'))


    # for doc in nlp.pipe([dict['tgt'] for dict in to_be_tokenized], batch_size=50000, n_process=60):
    #     docs_tokens = []
    #     for sent in doc.sents:
    #         docs_tokens.append([tok.text.lower() for tok in sent])


    # for _ in tqdm(pool.imap_unordered(_mp_tokenize, to_be_tokenized), total=len(to_be_tokenized)):
    #     pass

    # command = ['java', 'edu.stanford.nlp.pipeline.StanfordCoreNLP', '-annotators', 'tokenize,ssplit',
    #            '-ssplit.newlineIsSentenceBreak', 'always', '-filelist', 'mapping_for_corenlp.txt', '-outputFormat',
    #            'json', '-outputDirectory', tokenized_stories_dir]
    # print("Tokenizing %i files in %s and saving in %s..." % (len(stories), stories_dir, tokenized_stories_dir))
    # subprocess.call(command)

    print("Stanford CoreNLP Tokenizer has finished.")
    # os.remove("mapping_for_corenlp.txt")

    # Check that the tokenized stories directory contains the same number of files as the original directory
    num_orig = 0
    for set in ['train', 'validation', 'test']:
        num_orig = len(os.listdir(os.path.abspath(args.raw_path + '/' + set)))
    # num_orig = len(stories)
    num_tokenized = len(os.listdir(tokenized_stories_dir))
    if num_orig != num_tokenized:
        raise Exception(
            "The tokenized stories directory %s contains %i files, but it should contain the same number as %s (which has %i files). Was there an error during tokenization?" % (
                tokenized_stories_dir, num_tokenized, stories_dir, num_orig))
    print("Successfully finished tokenizing %s to %s.\n" % (stories_dir, tokenized_stories_dir))


def cal_rouge(evaluated_ngrams, reference_ngrams):
    reference_count = len(reference_ngrams)
    evaluated_count = len(evaluated_ngrams)

    overlapping_ngrams = evaluated_ngrams.intersection(reference_ngrams)
    overlapping_count = len(overlapping_ngrams)

    if evaluated_count == 0:
        precision = 0.0
    else:
        precision = overlapping_count / evaluated_count

    if reference_count == 0:
        recall = 0.0
    else:
        recall = overlapping_count / reference_count

    f1_score = 2.0 * ((precision * recall) / (precision + recall + 1e-8))
    return {"f": f1_score, "p": precision, "r": recall}


def greedy_selection(doc_sent_list, abstract_sent_list, summary_size):
    def _rouge_clean(s):
        return re.sub(r'[^a-zA-Z0-9 ]', '', s)

    max_rouge = 0.0
    abstract = sum(abstract_sent_list, [])
    abstract = _rouge_clean(' '.join(abstract)).split()
    sents = [_rouge_clean(' '.join(s)).split() for s in doc_sent_list]
    evaluated_1grams = [_get_word_ngrams(1, [sent]) for sent in sents]
    reference_1grams = _get_word_ngrams(1, [abstract])
    evaluated_2grams = [_get_word_ngrams(2, [sent]) for sent in sents]
    reference_2grams = _get_word_ngrams(2, [abstract])

    selected = []
    for s in range(summary_size):
        cur_max_rouge = max_rouge
        cur_id = -1
        for i in range(len(sents)):
            if (i in selected):
                continue
            c = selected + [i]
            candidates_1 = [evaluated_1grams[idx] for idx in c]
            candidates_1 = set.union(*map(set, candidates_1))
            candidates_2 = [evaluated_2grams[idx] for idx in c]
            candidates_2 = set.union(*map(set, candidates_2))
            rouge_1 = cal_rouge(candidates_1, reference_1grams)['f']
            rouge_2 = cal_rouge(candidates_2, reference_2grams)['f']
            rouge_score = rouge_1 + rouge_2
            if rouge_score > cur_max_rouge:
                cur_max_rouge = rouge_score
                cur_id = i
        if (cur_id == -1):
            return selected
        selected.append(cur_id)
        max_rouge = cur_max_rouge

    return sorted(selected)


def hashhex(s):
    """Returns a heximal formated SHA1 hash of the input string."""
    h = hashlib.sha1()
    h.update(s.encode('utf-8'))
    return h.hexdigest()


class BertData():
    def __init__(self, args):
        self.args = args
        self.tokenizer = BertTokenizer.from_pretrained('bert-base-uncased', do_lower_case=True)

        self.sep_token = '[SEP]'
        self.cls_token = '[CLS]'
        self.pad_token = '[PAD]'
        self.tgt_bos = '[unused0]'
        self.tgt_eos = '[unused1]'
        self.tgt_sent_split = '[unused2]'
        self.sep_vid = self.tokenizer.vocab[self.sep_token]
        self.cls_vid = self.tokenizer.vocab[self.cls_token]
        self.pad_vid = self.tokenizer.vocab[self.pad_token]

    def preprocess(self, src, tgt, sent_labels, use_bert_basic_tokenizer=False, is_test=False):

        if ((not is_test) and len(src) == 0):
            return None

        original_src_txt = [' '.join(s) for s in src]

        idxs = [i for i, s in enumerate(src) if (len(s) > self.args.min_src_ntokens_per_sent)]

        _sent_labels = [0] * len(src)
        for l in sent_labels:
            _sent_labels[l] = 1

        src = [src[i][:self.args.max_src_ntokens_per_sent] for i in idxs]
        sent_labels = [_sent_labels[i] for i in idxs]
        src = src[:self.args.max_src_nsents]
        sent_labels = sent_labels[:self.args.max_src_nsents]

        if ((not is_test) and len(src) < self.args.min_src_nsents):
            return None

        src_txt = [' '.join(sent) for sent in src]
        text = ' {} {} '.format(self.sep_token, self.cls_token).join(src_txt)

        src_subtokens = self.tokenizer.tokenize(text)

        src_subtokens = [self.cls_token] + src_subtokens + [self.sep_token]
        src_subtoken_idxs = self.tokenizer.convert_tokens_to_ids(src_subtokens)
        _segs = [-1] + [i for i, t in enumerate(src_subtoken_idxs) if t == self.sep_vid]
        segs = [_segs[i] - _segs[i - 1] for i in range(1, len(_segs))]
        segments_ids = []
        for i, s in enumerate(segs):
            if (i % 2 == 0):
                segments_ids += s * [0]
            else:
                segments_ids += s * [1]
        cls_ids = [i for i, t in enumerate(src_subtoken_idxs) if t == self.cls_vid]
        sent_labels = sent_labels[:len(cls_ids)]

        tgt_subtokens_str = '[unused0] ' + ' [unused2] '.join(
            [' '.join(self.tokenizer.tokenize(' '.join(tt), use_bert_basic_tokenizer=use_bert_basic_tokenizer)) for tt
             in tgt]) + ' [unused1]'
        tgt_subtoken = tgt_subtokens_str.split()[:self.args.max_tgt_ntokens]
        if ((not is_test) and len(tgt_subtoken) < self.args.min_tgt_ntokens):
            return None

        tgt_subtoken_idxs = self.tokenizer.convert_tokens_to_ids(tgt_subtoken)

        tgt_txt = '<q>'.join([' '.join(tt) for tt in tgt])
        src_txt = [original_src_txt[i] for i in idxs]

        return src_subtoken_idxs, sent_labels, tgt_subtoken_idxs, segments_ids, cls_ids, src_txt, tgt_txt


def format_to_bert(args):
    if (args.dataset != ''):
        datasets = [args.dataset]
    else:
        datasets = ['train', 'validation', 'test']

    for corpus_type in datasets:
        a_lst = []
        for json_f in glob.glob(pjoin(args.raw_path, '*' + corpus_type + '.*.json')):
            real_name = json_f.split('/')[-1]
            a_lst.append((corpus_type, json_f, args, pjoin(args.save_path, real_name.replace('json', 'bert.pt'))))
            _format_to_bert(a_lst[-1])
        # print(a_lst)
        pool = Pool(args.n_cpus)
        for d in pool.imap(_format_to_bert, a_lst):
            pass

        pool.close()
        pool.join()


def _format_to_bert(params):
    corpus_type, json_file, args, save_file = params
    is_test = corpus_type == 'test'
    if (os.path.exists(save_file)):
        logger.info('Ignore %s' % save_file)
        return

    bert = BertData(args)

    logger.info('Processing %s' % json_file)
    jobs = json.load(open(json_file))

    datasets = []
    for d in jobs:
        source, tgt, id = d['src'], d['tgt'], d['id']
        # import pdb;pdb.set_trace()

        sent_labels = greedy_selection(source[:args.max_src_nsents], tgt, 3)
        if (args.lower):
            source = [' '.join(s).lower().split() for s in source]
            tgt = [' '.join(s).lower().split() for s in tgt]
        b_data = bert.preprocess(source, tgt, sent_labels, use_bert_basic_tokenizer=args.use_bert_basic_tokenizer,
                                 is_test=is_test)
        # b_data = bert.preprocess(source, tgt, sent_labels, use_bert_basic_tokenizer=args.use_bert_basic_tokenizer)

        if (b_data is None):
            continue
        src_subtoken_idxs, sent_labels, tgt_subtoken_idxs, segments_ids, cls_ids, src_txt, tgt_txt = b_data
        b_data_dict = {"src": src_subtoken_idxs, "tgt": tgt_subtoken_idxs,
                       "src_sent_labels": sent_labels, "segs": segments_ids, 'clss': cls_ids,
                       'src_txt': src_txt, "tgt_txt": tgt_txt, 'id': id}
        datasets.append(b_data_dict)
    logger.info('Processed instances %d' % len(datasets))
    logger.info('Saving to %s' % save_file)
    torch.save(datasets, save_file)
    datasets = []
    gc.collect()

def move_subset(args):
    # read split ids

    if not os.path.exists(args.save_path):
        os.makedirs(args.save_path)

    with open('/tmp/th22_splits.json') as fR:
        splits = json.load(fR)

    for split, files in splits.items():
        for f in tqdm(files, total=len(files), desc=f'{split}'):
            try:
                # import pdb;pdb.set_trace()

                shutil.copy(args.raw_path + f, args.save_path)
                os.rename(args.save_path + f, args.save_path + split + '-' + '-'.join(f.split('-')[1:]))
            except:
                continue



def format_to_lines(args):
    corpus_mapping = {}
    # for corpus_type in ['valid', 'test', 'train']:
    #     temp = []
    #     for line in open(pjoin(args.map_path, 'mapping_' + corpus_type + '.txt')):
    #         temp.append(hashhex(line.strip()))
    #     corpus_mapping[corpus_type] = {key.strip(): 1 for key in temp}

    train_files, validation_files, test_files = [], [], []
    #
    for f in glob.glob(pjoin(args.raw_path + '/*.json')):
        real_name = f.split('/')[-1]
    #
    #     splits = {}
    #     with open('th22_splits.json') as fR:
    #         splits = json.load(fR)
    #
    #     splits['test'] = sorted(splits['test'])
    #     splits['validation'] = sorted(splits['validation'])
    #     splits['train'] = sorted(splits['train'])
    #
    #     if bi_contains(splits['test'], real_name):
    #         corpus_type='test'
    #     elif bi_contains(splits['validation'], real_name):
    #         corpus_type='validation'
    #     else:
    #         corpus_type='train'
    #
        corpus_type = real_name.split('-')[0]

        eval(f'{corpus_type}_files').append(f)
        # real_name = f.split('/')[-1].split('.')[0]
        # if (real_name in corpus_mapping['valid']):
        #     validation_files.append(f)
        # elif (real_name in corpus_mapping['test']):
        #     test_files.append(f)
        # elif (real_name in corpus_mapping['train']):
        #     train_files.append(f)
    # else:
    #     train_files.append(f)

    corpora = {'train': train_files, 'validation': validation_files, 'test': test_files}
    for corpus_type in ['train', 'validation', 'test']:
        a_lst = [(f, args) for f in corpora[corpus_type]]
        pool = Pool(args.n_cpus)
        dataset = []
        p_ct = 0
        for d in tqdm(pool.imap_unordered(_format_to_lines, a_lst), total=len(a_lst)):
            if d is not None:
                dataset.append(d)
                if (len(dataset) > args.shard_size):
                    pt_file = "{:s}{:s}.{:d}.json".format(args.save_path, corpus_type, p_ct)
                    with open(pt_file, 'w') as save:
                        # save.write('\n'.join(dataset))
                        save.write(json.dumps(dataset))
                        p_ct += 1
                        dataset = []

        pool.close()
        pool.join()
        if (len(dataset) > 0):
            pt_file = "{:s}{:s}.{:d}.json".format(args.save_path, corpus_type, p_ct)
            with open(pt_file, 'w') as save:
                # save.write('\n'.join(dataset))
                save.write(json.dumps(dataset))
                p_ct += 1
                dataset = []


def _format_to_lines(params):
    f, args = params
    # print(f)
    try:
        source, tgt, id = load_json(f, args.lower)
    except:
        with open('not_parsed_tokenized.txt', mode='a') as aF:
            aF.write(f)
            aF.write('\n')
        return None

    return {'src': source, 'tgt': tgt, 'id':id}


def format_xsum_to_lines(args):
    if (args.dataset != ''):
        datasets = [args.dataset]
    else:
        datasets = ['train', 'test', 'valid']

    corpus_mapping = json.load(open(pjoin(args.raw_path, 'XSum-TRAINING-DEV-TEST-SPLIT-90-5-5.json')))

    for corpus_type in datasets:
        mapped_fnames = corpus_mapping[corpus_type]
        root_src = pjoin(args.raw_path, 'restbody')
        root_tgt = pjoin(args.raw_path, 'firstsentence')
        # realnames = [fname.split('.')[0] for fname in os.listdir(root_src)]
        realnames = mapped_fnames

        a_lst = [(root_src, root_tgt, n) for n in realnames]
        pool = Pool(args.n_cpus)
        dataset = []
        p_ct = 0
        for d in pool.imap_unordered(_format_xsum_to_lines, a_lst):
            if (d is None):
                continue
            dataset.append(d)
            if (len(dataset) > args.shard_size):
                pt_file = "{:s}.{:s}.{:d}.json".format(args.save_path, corpus_type, p_ct)
                with open(pt_file, 'w') as save:
                    save.write(json.dumps(dataset))
                    p_ct += 1
                    dataset = []

        pool.close()
        pool.join()
        if (len(dataset) > 0):
            pt_file = "{:s}.{:s}.{:d}.json".format(args.save_path, corpus_type, p_ct)
            with open(pt_file, 'w') as save:
                save.write(json.dumps(dataset))
                p_ct += 1
                dataset = []


def _format_xsum_to_lines(params):
    src_path, root_tgt, name = params
    f_src = pjoin(src_path, name + '.restbody')
    f_tgt = pjoin(root_tgt, name + '.fs')
    if (os.path.exists(f_src) and os.path.exists(f_tgt)):
        print(name)
        source = []
        for sent in open(f_src):
            source.append(sent.split())
        tgt = []
        for sent in open(f_tgt):
            tgt.append(sent.split())
        return {'src': source, 'tgt': tgt}
    return None


