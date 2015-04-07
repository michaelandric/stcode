# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 00:01:17 2015

@author: andric
"""

import os
import numpy as np
import graph_evals as ge


def snsc_evaluation(ss, outdir, density):
    """
    Get Single Node Set Consistency (SNSC) value
    """
    subj_dir = '%s/%s/modularity%s' % (os.environ['state_rec'], ss, density)
    q_val, iter_max1 = ge.max_q(subj_dir, ss, 1, density)
    q_val, iter_max3 = ge.max_q(subj_dir, ss, 3, density)
    tname_1 = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.maxlevel_tree' % (iter_max1, ss, 1, density)
    input1 = os.path.join(subj_dir, tname_1)
    tname_3 = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.maxlevel_tree' % (iter_max3, ss, 3, density)
    input2 = os.path.join(subj_dir, tname_3)

    if ss == 'MRAG':
        return ge.snsc_MRAG(input1, input2)
    else:
        return ge.snsc(input1, input2)


def table_q_nmod_corr(subj_list):
    """
    Make table subjects by conditions
    of correlation between Q value and number modules (> 1 voxel)
    """
    conditions = np.arange(1, 5)
    out_array = np.zeros(len(subj_list)*len(conditions)).reshape(len(subj_list), len(conditions))
    for ss in enumerate(subj_list):
        subj_dir = '%s/%s/modularity%s' % (os.environ['state_rec'], ss[1], '5p')
        for cc in enumerate(conditions):
            out_array[ss[0], cc[0]] = ge.q_nmod_corr(ss[1], cc[1], '5p', subj_dir)

    return out_array


if __name__ == '__main__':

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']

    import pandas as pd
    condition_names = ['HighlyOrdered', 'SomewhatOrdered', 'Random', 'AlmostRandom']
    q_nmod_corr_out = pd.DataFrame(table_q_nmod_corr(subj_list), index=subj_list, columns=condition_names)
    q_nmod_corr_out.to_csv('%s/state/q_nmod_corr.csv' % os.environ['t2'])
