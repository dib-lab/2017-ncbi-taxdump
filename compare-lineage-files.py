#! /usr/bin/env python
"""
Load two files with lineages on each line (e.g. kaiju output
processed by kaiju.py and sourmash output processed by
sourmash-csv-to-lineages.py) and compare at given taxonomic level.
"""
from __future__ import print_function
import sys
import argparse
from collections import Counter


def main():
    p = argparse.ArgumentParser()
    p.add_argument('file1')
    p.add_argument('file2')
    p.add_argument('column')
    p.add_argument('-m', '--min-in-file1', type=int, default=0)
    p.add_argument('-o', '--output-details', type=str)
    args = p.parse_args()

    # figure out which taxonomic resolution we want
    want_taxonomy = ['superkingdom', 'phylum', 'order', 'class', 'family',
                     'genus', 'species']
    try:
        column_idx = int(args.column)
    except ValueError:
        column_idx = want_taxonomy.index(args.column)

    tax_level = want_taxonomy[column_idx]
    print('comparing at tax level: {}'.format(tax_level),
          file=sys.stderr)

    # load file A, and count the number of times each term shows up
    # (potentially thresholding).
    a_cnt = Counter()

    print('loading', args.file1, file=sys.stderr)
    with open(args.file1) as fp:
        next(fp)
        
        for line in fp:
            col = line.strip()
            if len(col):
                col = col.split(';')
                if col[column_idx]:
                    col = col[:column_idx]
                    col = ';'.join(col)
                    a_cnt[col] += 1

    # threshold at a given count if desired (default is 0 threshold)
    a = set()
    for item, item_count in a_cnt.most_common():
        if item_count >= args.min_in_file1:
            a.add(item)
        else:
            break

    # load file B
    b = set()
    print('loading', args.file2, file=sys.stderr)
    with open(args.file2) as fp:
        next(fp)
        
        for line in fp:
            col = line.strip()
            if len(col):
                col = col.split(';')
                if col[column_idx]:
                    col = col[:column_idx]
                    col = ';'.join(col)
                    b.add(col)

    # show unique-to-a, unique-to-b, common, tax_level
    print(len(a - b), len(b - a), len(a.intersection(b)), tax_level)

    # output?
    if args.output_details:
        print('writing output details to {}.*'.format(args.output_details))
        with open(args.output_details + '.only_a', 'w') as fp:
            for name in a - b:
                fp.write("{}\n".format(name))

        with open(args.output_details + '.only_b', 'w') as fp:
            for name in b - a:
                fp.write("{}\n".format(name))

        with open(args.output_details + '.common', 'w') as fp:
            for name in b.intersection(a):
                fp.write("{}\n".format(name))


if __name__ == '__main__':
    main()
