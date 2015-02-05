#!~/anaconda/bin/python

import os
import shutil
from glob import glob

subjects = ["ANGO", "MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN","CLFR"]

def make_dirs(ss, newdir):
    if not os.path.exists(newdir):
        os.makedirs(newdir)

def file_mover(file, destination):
    shutil.copy2(file, destination)

def generate_batchargs(args):
    import makeargs as mm
    print mm.makeargs(args)


if __name__ == "__main__":

    for ss in subjects:
        nd = '/mnt/lnif-storage/urihas/MAstdstt/%s' % ss
        make_dirs(ss, nd)
        filelist = glob('/mnt/lnif-storage/urihas/MAstdstt/TS_files/*%s*' % ss)
        for f in filelist:
            file_mover(f, nd)
