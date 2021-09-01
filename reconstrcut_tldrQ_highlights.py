import json

highlited_file = '/disk1/sajad/datasets/reddit/tldr-9+/highlights-test/'
with open('/disk1/sajad/datasets/reddit/tldr-9+/test.json') as fR:
    for l in fR:
        ent = json.loads(l.strip())
        src = ent['document'].replace('</s><s> ', '')
        summary = ent['summary']

        to_be_written = f'{src.strip()}\n@highlights\n{summary.strip()}'

        with open(highlited_file + ent['id'].replace('.json', ''), mode='w') as fW:
            fW.write(to_be_written)