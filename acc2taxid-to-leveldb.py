#! /usr/bin/env python
import leveldb
import argparse

def main():
    p = argparse.ArgumentParser()
    p.add_argument('acc2taxid_file')
    p.add_argument('dbout')
    args = p.parse_args()

    db = leveldb.LevelDB(args.dbout)

    with open(args.acc2taxid_file, 'rb') as fp:
        batch = leveldb.WriteBatch()

        next(fp)                #  skip headers
        for n, line in enumerate(fp):
            if n and n % 100000 == 0:
                print('...', n)
                db.Write(batch)
            acc, _, taxid, _ = line.split()
            taxid = int(taxid)
            batch.Put(bytes(acc), taxid.to_bytes(4, byteorder='big'))

        db.Write(batch, sync=True)

if __name__ == '__main__':
    main()
