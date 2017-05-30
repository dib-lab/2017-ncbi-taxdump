# 2017-ncbi-taxdump

Files for all of the below exist on the MSU HPC under
`/mnt/research/ged/ctb/tax`.

# Extract taxonomic lineage information for a set of NCBI accession numbers

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

-----

## Kaiju foo

To extract a lineage file from Kaiju output, do:

```
./kaiju.py taxdump/nodes.dmp taxdump/names.dmp mircea_kaijudb-e/kaijudb_e_SRR606249.pe.qc.fq.gz.abundtrim.out
```

This will produce a `*.lineage` file in the cwd directory.

-----

## Comparing lineage files

To construct a lineage file from the output of `sourmash-csv-to-lineages.py`,
do e.g. `cut -d, -f4 gather.csv > gather.lineage`.

Then run:

`./compare-lineage-files.py kaijudb_e_SRR606249.pe.qc.fq.gz.abundtrim.out.lineage gather.lineage $column`

where column is one of `(superkingdom phylum order class family genus species)`.

The output will be `only_A only_B both_AB`.

To run it for all of 'em at once, do:

``` 
for col in superkingdom phylum order class family genus species;
do
echo $col $(./compare-lineage-files.py kaijudb_e_SRR606249.pe.qc.fq.gz.abundtrim.out.lineage gather.lineage $col);
done
