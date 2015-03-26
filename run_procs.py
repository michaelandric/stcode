# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import procedures as procs
import os
# import sys
# import shutil
# from glob import glob


if __name__ == '__main__':

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    # ss = sys.argv[1]

    data_dir = '%s/state/global_connectivity/group' % os.environ['t2']
    os.chdir(data_dir)
    print os.getcwd()
    input_pref = 'avg_corrZ_def_anova'
    mask = '%s/data/standard/MNI152_T1_2mm.nii.gz' % os.environ['FSLDIR']
    out_name = '%s_fwhm_est_out' % input_pref
    # procs.fwhm_est('%s+tlrc' % input_pref, out_name, mask)
    # fwhmvals = [5.50817, 5.91411, 5.89492]
    # fwhmvals = [9.16169, 10.2877, 10.193]
    fwhmvals = [6, 6, 6]
    procs.clustsim(fwhmvals, mask)
