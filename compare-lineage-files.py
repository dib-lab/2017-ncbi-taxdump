#! /usr/bin/env python
from __future__ import print_function
import sys
import argparse
from collections import Counter

want_taxonomy = ['superkingdom', 'phylum', 'order', 'class', 'family', 'genus', 'species']

def main():
    p = argparse.ArgumentParser()
    p.add_argument('file1')
    p.add_argument('file2')
    p.add_argument('column')
    p.add_argument('-m', '--min-in-file1', type=int, default=0)
    args = p.parse_args()

    try:
        column_idx = int(args.column)
    except ValueError:
        column_idx = want_taxonomy.index(args.column)

    a_cnt = Counter()

    print('loading', args.file1, file=sys.stderr)
    with open(args.file1) as fp:
        next(fp)
        
        for line in fp:
            col = line.strip()
            if len(col):
                col = col.split(';')
                col = col[column_idx]
                a_cnt[col] += 1

    a = set()
    for item, item_count in a_cnt.most_common():
        if item_count >= args.min_in_file1:
            a.add(item)
        else:
            break

    b = set()
    print('loading', args.file2, file=sys.stderr)
    with open(args.file2) as fp:
        next(fp)
        
        for line in fp:
            col = line.strip()
            if len(col):
                col = col.split(';')
                col = col[column_idx]
                b.add(col)

    print(len(a - b), len(b - a), len(a.intersection(b)))


if __name__ == '__main__':
    main()
