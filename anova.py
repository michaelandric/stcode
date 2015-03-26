# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:13:40 2015

@author: andric
"""

import os
import time
from shlex import split
from subprocess import call, STDOUT


def afni_anova(cond_list, ss_list):
    """
    Doing mixed effects (rand: subjects, fixed: conditions)
    """
    dsets = []
    ameans = []
    for i, cond_name in enumerate(cond_list):
        ameans.append('-amean %d %s_mean' % (i+1, cond_name))
        for j, ss in enumerate(ss_list):
            dset_dir = '%s/state/global_connectivity/%s_res' % (os.environ['t2'], ss)
            dset_pref = 'avg_corrZ_%d_%s_highres_fnirted_def_MNI2mm.nii.gz' % (i+1, ss)
            dsets.append("-dset %d %d '%s'" % (i+1, j+1, os.path.join(dset_dir, dset_pref)))

    ameans = ' '.join(ameans)
    dsets = ' '.join(dsets)
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('stdout_files/stdout_from_3dANOVA2.txt', 'w')
    cmdargs = split('3dANOVA2 -type 3 -alevels 4 -blevels %d \
                    %s -fa all_fstat %s \
                    -mask %s/data/standard/MNI152_T1_2mm_brain_mask_dil1.nii.gz \
                    -adiff 1 3 HighlyOrdervsRandom \
                    -acontr -0.75 -0.059 0.63 0.178 poslincorrect \
                    -acontr 0.42 -0.57 0.56 -0.41 Ushapecorrect \
                    -acontr -1 -1 1 1 stepupcorrect \
                    -bucket avg_corrZ_anova' % (len(ss_list), dsets, ameans, os.environ['FSLDIR']))
    call(cmdargs, stdout=f, stderr=STDOUT)


if __name__ == "__main__":

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    conditions = ['HighlyOrder', 'SomewhatOrder', 'Random', 'AlmostRandom']

    os.chdir('%s/state/global_connectivity/group' % os.environ['t2'])
    print 'Doing ANOVA -- %s' % time.ctime()
    print os.getcwd()
    afni_anova(conditions, subj_list)
