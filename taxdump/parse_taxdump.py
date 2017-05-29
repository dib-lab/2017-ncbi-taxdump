#! /usr/bin/env python
import sys
import argparse

def parse_nodes(filename):
    child_to_parent = dict()
    node_to_info = dict()

    with open(filename) as fp:
        for n, line in enumerate(fp):
            x = line.split('\t|\t')

            node_id, parent_node_id, rank, embl, div_id, div_flag, gencode, mgc_inherit, mgc_flag, mgc_id, hidden_flag, subtree_flag, comments = x

            node_id = int(node_id)
            parent_node_id = int(parent_node_id)

            child_to_parent[node_id] = parent_node_id
            node_to_info[node_id] = rank, embl, div_id, div_flag, comments

    return child_to_parent, node_to_info


def parse_names(filename):
    taxid_to_names = dict()
    with open(filename) as fp:
        for n, line in enumerate(fp):
            line = line.rstrip('\t|\n')
            x = line.split('\t|\t')

            taxid, name, uniqname, name_class = x
            taxid = int(taxid)

            if name_class == 'scientific name':
                taxid_to_names[taxid] = (name, uniqname, name_class)

    return taxid_to_names


want_taxonomy = ['superkingdom', 'phylum', 'order', 'class', 'family', 'genus', 'species']

def get_lineage(names, child_to_parent, node_to_info, taxid):
    taxid = int(taxid)

    d = {}

    lineage = []
    while taxid != 1:
        if taxid not in node_to_info:
            print('cannot find taxid {}; quitting.'.format(taxid))
            break
        rank = node_to_info[taxid][0]
        if rank in want_taxonomy:
            d[rank] = names[taxid][0]
        taxid = child_to_parent[taxid]

    return d


def main():
    p = argparse.ArgumentParser()
    p.add_argument('nodes_dmp')
    p.add_argument('names_dmp')
    args = p.parse_args()

    names = parse_names(args.names_dmp)
    child_to_parent, node_to_info = parse_nodes(args.nodes_dmp)

    lineage = get_lineage(names, child_to_parent, node_to_info, 407976)
    print(lineage)


if __name__ == '__main__':
    main()
