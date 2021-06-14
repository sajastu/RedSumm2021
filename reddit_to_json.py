import json

BASE_DIR = '/home/code-base/user_space/packages/summarization_datasets/datasets/'

for set in ['train']:
    i = 0
    json_file = open(f'{BASE_DIR}/{set}.json', mode='a')
    srcs = []
    tgts = []

    with open(f'{BASE_DIR}/{set}.source') as fS:
        for l in fS:
            if len(l.strip()) > 0:
                i+=1
                l = l.replace('\n', ' ').strip()

        #         if '\n' in l:
        #             print('n')
        #             import pdb;pdb.set_trace()
        #         if '\r' in l:
        #             print('r')
        #             import pdb;pdb.set_trace()
        #         srcs.append(l)
        #
        # with open(f'{BASE_DIR}/{set}.source') as fS:
        #     for j, l in enumerate(fS):
        #         srcs[j] == ''.
        #
        # import pdb;pdb.set_trace()

        with open(f'{BASE_DIR}/{set}.source') as fS, open(
                f'{BASE_DIR}/{set}.target') as fT:
            for s, t in zip(fS, fT):
                # srcs.append(s.replace('\n', ' ').strip())
                # tgts.append(t.replace('\n', ' ').strip())
        #
        #     import pdb;pdb.set_trace()
                if len(s.strip()) > 0:

                    json.dump(
                        {'id': f'{set}-{i}', 'text': s.replace('\n', ' ').strip(), 'summary': t.replace('\n', ' ').strip()},
                        json_file)
                    json_file.write('\n')
