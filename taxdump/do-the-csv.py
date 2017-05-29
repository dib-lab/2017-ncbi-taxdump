#! /usr/bin/env python
from __future__ import print_function
import sys
import argparse
import csv

from parse_taxdump import parse_names, parse_nodes, get_lineage


want_taxonomy = ['superkingdom', 'phylum', 'class', 'order', 'family', 'genus', 'species']
def main():
    p = argparse.ArgumentParser()
    p.add_argument('nodes_dmp')
    p.add_argument('names_dmp')
    p.add_argument('acc_taxid_csv')
    args = p.parse_args()

    names = parse_names(args.names_dmp)
    child_to_parent, node_to_info = parse_nodes(args.nodes_dmp)

    r = csv.reader(open(args.acc_taxid_csv))
    for row in r:
        acc, taxid = row
        taxid = int(taxid)

        x = get_lineage(names, child_to_parent, node_to_info, taxid)
        z = []
        for t in want_taxonomy:
            z.append(x.get(t, ''))

        print('{},{},{}'.format(acc, taxid, ';'.join(z)))


if __name__ == '__main__':
    main()
