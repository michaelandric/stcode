# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import os
import sys
import procedures as procs
import shutil
from glob import glob


if __name__ == '__main__':

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW']
    subj_list = ['LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS']
    # subj_list = ['MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    # ss = sys.argv[1]
    for ss in subj_list:
        anat_dir = '%s/state/%s' % (os.environ['t2'], ss)
        os.chdir(anat_dir)
        print os.getcwd()
        procs.fslanat('%s.SurfVol_Alnd_Exp' % ss)
