#! /usr/bin/env python
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

    # load the signatures (-> md5)
    with open(args.matched_sigs) as fp:
        md5sums = {}
        
        siglist = list(sourmash_lib.signature.load_signatures(fp))
        for sig in siglist:
            md5 = sig.md5sum()
            acc = sig.name().split(' ')[0]   # first part of sequence name
            acc = acc.split('.')[0]          # get acc w/o version

            print('md5 {} has accession {}'.format(md5[:8], acc), file=sys.stderr)
            md5sums[md5] = acc

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

            w.writerow([md5, acc, taxid, lineage])
            

if __name__ == '__main__':
    main()
