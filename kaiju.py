#! /usr/bin/env python
"""
Convert kaiju detailed output to NCBI lineages using the NCBI taxdump.

The nodes_dmp and names_dmp files are from
ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz

Creates a lineage.gz file named by appending that to kaiju input file.
"""
from __future__ import print_function
import sys
import argparse
from taxdump.parse_taxdump import parse_names, parse_nodes, get_lineage
from pickle import dump
import os.path
import gzip


want_taxonomy = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']

def parse_kaiju(filename):
    with open(filename) as fp:
        for line in fp:
            if line[0] == 'C':            # skip unclassified / 'U'
                yield int(line.split()[2])   # get column 3


def main():
    p = argparse.ArgumentParser()
    p.add_argument('nodes_dmp')
    p.add_argument('names_dmp')
    p.add_argument('kaiju_out')
    args = p.parse_args()

    print('loading...', file=sys.stderr)
    names = parse_names(args.names_dmp)
    child_to_parent, node_to_info = parse_nodes(args.nodes_dmp)

    print('parsing kaiju file:', args.kaiju_out)

    n = 0
    x = []
    with gzip.open(os.path.basename(args.kaiju_out) + '.lineage.gz', 'w') as fp:
        for taxid in parse_kaiju(args.kaiju_out):
            lineage = get_lineage(names, child_to_parent, node_to_info, taxid)
            if lineage:
                z = []
                for t in want_taxonomy:
                     z.append(lineage.get(t, ''))

                fp.write(';'.join(z))
                fp.write('\n')

            n += 1

            if n % 100000 == 0:
                print('...', n)


if __name__ == '__main__':
    main()
