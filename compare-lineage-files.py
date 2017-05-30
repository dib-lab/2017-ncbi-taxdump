#! /usr/bin/env python
from __future__ import print_function
import argparse


def main():
    p = argparse.ArgumentParser()
    p.add_argument('file1')
    p.add_argument('file2')
    p.add_argument('column', type=int)
    args = p.parse_args()

    a = set()

    with open(args.file1) as fp:
        next(fp)
        
        for line in fp:
            col = line.strip()
            if len(col):
                col = col.split(';')
                col = col[args.column]
                a.add(col)

    b = set()
    with open(args.file2) as fp:
        next(fp)
        
        for line in fp:
            col = line.strip()
            if len(col):
                col = col.split(';')
                col = col[args.column]
                b.add(col)

    print(len(a - b), len(b - a), len(a.intersection(b)))


if __name__ == '__main__':
    main()
