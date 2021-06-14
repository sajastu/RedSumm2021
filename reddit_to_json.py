import json

BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'

for set in ['val', 'test']:
    i = 0
    # json_file = open(f'{BASE_DIR}/{set}.json', mode='a')
    srcs = []
    tgts = []

    with open(f'{BASE_DIR}/{set}.source') as fS:
        for l in fS:
            i+=1
            if '\n' in l:
                print('n')
                import pdb;pdb.set_trace()
            if '\r' in l:
                print('r')
                import pdb;pdb.set_trace()
            s = l.replace('\n', ' ').strip()
            srcs.append(s)

    import pdb;pdb.set_trace()

    # with open(f'{BASE_DIR}/{set}.source') as fS, open(
    #         f'{BASE_DIR}/{set}.target') as fT:
    #     for s, t in zip(fS, fT):
    #         srcs.append(s.replace('\n', ' ').strip())
    #         tgts.append(t.replace('\n', ' ').strip())
    #
    #     import pdb;pdb.set_trace()
            # json.dump(
            #     {'id': f'{set}-{i}', 'text': s.replace('\n', ' ').strip(), 'summary': t.replace('\n', ' ').strip()},
            #     json_file)
            # json_file.write('\n')
