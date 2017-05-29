#! /usr/bin/env python
from __future__ import print_function
import argparse
import gzip

def main():
    p = argparse.ArgumentParser()
    p.add_argument('acc_file')
    p.add_argument('acc2taxid_files', nargs='+')
    args = p.parse_args()

    with open(args.acc_file) as fp:
        acc_set = set([ x.strip().split('.')[0] for x in fp ])

    outfp = open(args.acc_file + '.taxid', 'w')

    m = 0
    for filename in args.acc2taxid_files:
        xopen = open
        if filename.endswith('.gz'):
            xopen = gzip.open

        with xopen(filename, 'r') as fp:
            next(fp)                #  skip headers
            for n, line in enumerate(fp):
                if n and n % 100000 == 0:
                    print('...', n, m, filename)

                try:
                    acc, _, taxid, _ = line.split()
                except ValueError:
                    print('ignoring line', (line,))
                    continue

                if acc in acc_set:
                    m += 1
                    outfp.write('{},{}\n'.format(acc, taxid))
                    acc_set.remove(acc)

    print('failed to find {} acc'.format(len(acc_set)))


if __name__ == '__main__':
    main()
