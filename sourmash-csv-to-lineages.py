#! /usr/bin/env python
"""
Take a sourmash output CSV containing md5sums ('search' and 'gather'),
a collection of associated signatures, and a file containing accession
-> lineage information, and create a new CSV file with md5sum, accession,
taxid, and a lineage string.
"""
from __future__ import print_function
import sourmash_lib.signature
import csv
import argparse
import gzip
import sys


def main():
    p = argparse.ArgumentParser()
    p.add_argument('sourmash_csv')
    p.add_argument('matched_sigs')
    p.add_argument('genbank_csv')
    p.add_argument('--extra-info')
    args = p.parse_args()

    xopen = open
    if args.genbank_csv.endswith('.gz'):
        xopen = gzip.open

    # load the genbank CSV (accession -> lineage)
    with xopen(args.genbank_csv, 'rt') as fp:
        accessions = {}
        for row in csv.DictReader(fp, fieldnames=['acc', 'taxid', 'lineage']):
            acc = row['acc']
            accessions[acc] = row

    #
    extra_info = {}
    if args.extra_info:
        with open(args.extra_info) as fp:
            r = csv.reader(fp)
            for row in r:
                name = row[0]
                taxid = int(row[1])
                lineage = row[2]
                extra_info[name] = (taxid, lineage)

    # load the signatures (-> md5)
    with open(args.matched_sigs) as fp:
        md5sums = {}
        md5sums_name = {}
        
        siglist = list(sourmash_lib.signature.load_signatures(fp))
        for sig in siglist:
            md5 = sig.md5sum()
            acc = sig.name().split(' ')[0]   # first part of sequence name
            acc = acc.split('.')[0]          # get acc w/o version

            # @CTB hack hack split off NZ from accession
            if acc.startswith('NZ_'):
                acc = acc[3:]

            #print('md5 {} has accession {}'.format(md5[:8], acc), file=sys.stderr)
            md5sums[md5] = acc
            md5sums_name[md5] = sig.name()

    if not siglist:
        print('no signatures!? quitting.', file=sys.stderr)
        sys.exit(-1)

    with open(args.sourmash_csv) as fp:

        w = csv.writer(sys.stdout)
        w.writerow(['md5', 'acc', 'taxid', 'lineage'])
        for row in csv.DictReader(fp):
            md5 = row['md5']
            acc = md5sums.get(md5, '')
            
            lineage = ''
            taxid = ''
            if acc:
                info = accessions.get(acc)
                if info:
                    lineage = info['lineage']
                    taxid = info['taxid']

            if not lineage and not taxid:
                # try in backup file
                name = md5sums_name[md5]
                taxid, lineage = extra_info.get(name, ('', ''))

            w.writerow([md5, acc, taxid, lineage])
            

if __name__ == '__main__':
    main()
