# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import os
import procedures as procs


if __name__ == '__main__':

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MNGO', 'LRVN']
    subj_list = ['ANGO']
    for ss in subj_list:
        ijks = '%s/%s/masking/ijk_coords_graymattermask_%s' % (os.environ['state_rec'], ss, ss)
        snsc_data = 'snsc_%s' % ss
        data_dir = '%s/state/snsc_results' % os.environ['t2']
        mstr = '%s/%s/blur.1.%s.steadystate.TRIM+orig' % (os.environ['state_rec'], ss, ss)
        procs.undump(ss, ijks, snsc_data, data_dir, mstr)
        tlrc_brain = '%s/%s/corrTRIM_BLUR/%stlrc+tlrc' % (os.environ['state_rec'], ss, ss)
        # procs.autotlrc(subjid, tlrc_brain, afni_data, data_dir)
