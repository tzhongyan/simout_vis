import parser
import pandas as pd

def five_digit(i):
    i = str(i)
    while len(i) < 5:
        i = '0' + i
    return i

def merge(type_='ge', n=100, file_path='simout/simout/'):
    dd = []
    for i in range(1, n+1):
        fname = 'sim' + type_ + five_digit(i) + '.nml'
        print('Reading file: ' + fname)
        path = file_path + fname
        dd.append(parser.read_nml(path))
    
    # initiate df
    col_300 = ['KHAT', 'S', 'ZI', 'EPH', 'C', 'I', 'Y', 'RF1', 'SIGDLOGC1', 'ADJ']
    col_300_000 = ['KPAN', 'VPAN', 'DPAN', 'EPIPAN']

    sm = pd.DataFrame(columns=col_300)
    bm = pd.DataFrame(columns=col_300_000)

    i=1
    # append from read data
    for dat in dd:
        print('Merging row ' + five_digit(i))
        i = i+1
        sm = sm.append(pd.DataFrame({x:dat[x] for x in col_300}, columns=col_300), ignore_index=True)
        bm = bm.append(pd.DataFrame({x:dat[x] for x in col_300_000}, columns=col_300_000), ignore_index=True)

    return sm, bm