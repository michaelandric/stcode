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

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    for ss in subj_list:
        new_dir = '%s/state/%s' (os.environ['t2'], ss)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        for f in glob('%s/%s/masking/%s.SurfVol_Alnd_Exp+orig*' % (os.environ['state_rec'], ss, ss)):
            shutil.copy2(f, new_dir)
