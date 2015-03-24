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

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    """for ss in subj_list:
        arglist = []
        arglist.append('run_procs.py')
        arglist.append(ss)
        procs.gen_condor_submit_args(arglist)"""
    ss = sys.argv[1]
    data_dir = '%s/state/global_connectivity/%s_res' % (os.environ['t2'], ss)
    for cc in xrange(1, 5):
        tlrc_brain = '%s/%s/corrTRIM_BLUR/%stlrc+tlrc' % (os.environ['state_rec'], ss, ss)
        afni_dat = 'avg_corrZ_%d_%s.ijk+orig' % (cc, ss)
        procs.autotlrc(ss, tlrc_brain, afni_dat, data_dir)