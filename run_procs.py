# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import os
import sys
import procedures as procs


if __name__ == '__main__':

    # subj_list = ['CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    """for ss in subj_list:
        arglist = []
        arglist.append('run_procs.py')
        arglist.append(ss)
        procs.gen_condor_submit_args(arglist)"""
    data_dir = '%s/state/snsc_results' % os.environ['t2']
    ijks = '%s/groupstats/ijk_coords_TTavg152T1' % os.environ['state_rec']
    dat = '%s/snsc_group_median.txt' % data_dir
    mstr = '%s/groupstats/automask_d1_TTavg152T1+tlrc' % os.environ['state_rec']
    procs.undump('preserved', ijks, dat, data_dir, mstr)
    """for h in ['lh', 'rh']:
        parent_vol = 'snsc_group_median.txt.ijk+tlrc'
        pn = '2.0'
        outname = 'snsc_group_median.txt.ijk_tlrc_%s_%s.1D' % (h, pn)
        procs.vol2surf(h, parent_vol, 'TT_N27+tlrc', '2.0', outname)"""
