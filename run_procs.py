# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import procedures as procs
import os
import sys
# import shutil
# from glob import glob


if __name__ == '__main__':

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    ss = sys.argv[1]
    mask = '%s/data/standard/MNI152_T1_2mm_brain_mask_dil1.nii.gz' % os.environ['FSLDIR']
    data_dir = '%s/state/global_connectivity/%s_res' % (os.environ['t2'], ss)
    for cc in xrange(1, 5):
        afni_data_pref = 'avg_corrZ_%d_%s_highres_fnirted_MNI2mm.nii.gz' % (cc, ss)
        outname_pref = 'avg_corrZ_%d_%s_highres_fnirted_MNI2mm.txt' % (cc, ss)
        procs.maskdump(mask, data_dir, os.path.join(data_dir, afni_data_pref), os.path.join(data_dir, outname_pref))
