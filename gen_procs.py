#!~/anaconda/bin/python

import os
import shutil
from glob import glob

subjects = ["ANGO", "MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN","CLFR"]

def make_dirs(newdir):
    if os.path.exists(newdir):
        print newdir+' --> This already exists!'
    if not os.path.exists(newdir):
        print newdir+' is the new directory'
        os.makedirs(newdir)

def file_mover(file, destination):
    shutil.copy2(file, destination)

def generate_batchargs(args):
    import makeargs as mm
    print mm.makeargs(args)


if __name__ == "__main__":

    for ss in subjects:
        nd = '/mnt/lnif-storage/urihas/MAstdstt/%s/graphs' % ss
        make_dirs(nd)
        nd = '/mnt/lnif-storage/urihas/MAstdstt/%s/stdout_files' % ss
        make_dirs(nd)
