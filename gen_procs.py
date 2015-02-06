#!~/anaconda/bin/python

import os
import shutil
from glob import glob

#subjects = ["ANGO", "MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO","ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN","CLFR"]
#subjects = ["MYTP","TRCO","PIGL","SNNW","LDMW","FLTM","EEPA","DNLN","CRFO"]
#subjects = ["ANMS","MRZM","MRVV","MRMK","MRMC","MRAG","MNGO","LRVN","CLFR"]
subjects = ['DNLN', 'CRFO', 'ANMS', 'MRMK', 'MRMC', 'MRAG', 'LRVN', 'CLFR']   # these subjects were hung on 31, James was trying to do DTI stuff, shit was clogged. 

def make_dirs(newdir):
    if os.path.exists(newdir):
        print newdir+' --> This already exists!'
    if not os.path.exists(newdir):
        print newdir+' is the new directory'
        os.makedirs(newdir)

def file_mover(file, destination):
    shutil.copy2(file, destination)

def generate_batchargs(arg1, arg2, arg3):
    """sample usage:
    $ python gen_procs.py >> ../submitdir/submit_1.corr_mats
    """
    print 'arguments    = /mnt/lnif-storage/urihas/MAstdstt/stcode/1.corr_mats.py %s %s %s \nqueue \n' % (arg1, arg2, arg3)


if __name__ == "__main__":

    td = 0.05   # thresh density
    for ss in subjects:
        for c in xrange(1,5):
            generate_batchargs(ss, c, td)

