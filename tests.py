# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:01:17 2015

@author: andric
"""

import os
import numpy as np
import graph_evals as ge


def snsc_evaluation(subj_list, density):
    """
    Get Single Node Set Consistency (SNSC) value
    """
    q_value_array = np.zeros(len(subj_list*4)).reshape(len(subj_list), 4)

    for ss in enumerate(subj_list):
        subj_dir = '%s/%s/modularity%s' % (os.environ['state_rec'], ss[1], density)
        q_val, iter_max1 = ge.max_q(subj_dir, ss[1], 1, density)
        q_val, iter_max3 = ge.max_q(subj_dir, ss[1], 3, density)
        tname_1 = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.maxlevel_tree' % (iter_max1, subjid, 1, density)
        cond1_in = os.path.join(subj_dir, tname_1)
        tname_3 = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.maxlevel_tree' % (iter_max3, subjid, 3, density)
        cond3_in = os.path.join(subj_dir, tname_3)
        outname = '%s' % WHAT IS THE OUT NAME
        np.savetxt(os.path.join(subj_dir, outname), ge.snsc(tname_1, tname_3), fmt='%.4f')


if __name__ == '__main__':

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']

    snsc_evaluation(subj_list, '5p')
