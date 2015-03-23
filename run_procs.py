# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import os
import sys
import procedures as procs


if __name__ == '__main__':

    subj_list = ['CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN']
    # subj_list = ['CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MNGO', 'LRVN']
    # subj_list = ['ANGO']
    """for ss in subj_list:
        arglist = []
        arglist.append('run_procs.py')
        arglist.append(ss)
        procs.gen_condor_submit_args(arglist)"""
    # ss = sys.argv[1]
    for ss in subj_list:
        # For undump:
        ijks = '%s/%s/masking/ijk_coords_graymattermask_%s' % (os.environ['state_rec'], ss, ss)
        snsc_data = 'snsc_%s.txt' % ss
        data_dir = '%s/state/snsc_results' % os.environ['t2']
        mstr = '%s/%s/blur.1.%s.steadystate.TRIM+orig' % (os.environ['state_rec'], ss, ss)
        procs.undump(ss, ijks, snsc_data, data_dir, mstr)

        # for autotlrc
        tlrc_brain = '%s/%s/corrTRIM_BLUR/%stlrc+tlrc' % (os.environ['state_rec'], ss, ss)
        afni_dat = '%s.ijk+orig' % snsc_data
        procs.autotlrc(ss, tlrc_brain, afni_dat, data_dir)
