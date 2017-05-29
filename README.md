# 2017-ncbi-taxdump

Create a CSV containing taxonomic lineage for NCBI accession numbers.

Usage:
```
./sourmash-csv-to-lineages.py gather.csv gather-matches.sig genbank-genomes-accession+lineage-20170529.csv.gz > lineages.csv
```

where `gather.csv` comes from `sourmash gather -o` and `gather-matches.sig`
comes from `--save-matches`, e.g.

```
sourmash gather podar-reads.10k.sig fixed.sbt.json -o gather.csv --save-matches=gather-matches.sig
```

For some reason a few accessions do not have matches in our database; for those,
the `lineages.csv` will simply output empty taxid and lineage column entries.
