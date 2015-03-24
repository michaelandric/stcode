# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import os
import sys
import procedures as procs


if __name__ == '__main__':

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    """for ss in subj_list:
        arglist = []
        arglist.append('run_procs.py')
        arglist.append(ss)
        procs.gen_condor_submit_args(arglist)"""
    ss = sys.argv[1]
    data_dir = '%s/state/global_connectivity' % os.environ['t2']
    for cc in xrange(1, 5):
        ijks = '%s/%s/masking/ijk_coords_graymattermask_%s' % (os.environ['state_rec'], ss, ss)
        dat = '%s/avg_corrZ_%d_%s' % (data_dir, cc, ss)
        mstr = '%s/%s/blur.%d.%s.steadystate.TRIM+orig' % (os.environ['state_rec'], ss, cc, ss)
        procs.undump(ss, ijks, dat, data_dir, mstr)
