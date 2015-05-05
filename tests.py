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


def nmi_evaluation(ss, density):
    """
    Evaluate normalized mutual information
    Uses function in 'graph_evals.py'
    :param ss: Subject identifier
    :param density: corresponding graph density
    :returns : 6 values corresponding to pairwise number of
    conditions (4) at which NMI is tested
    """
    subj_dir = '%s/%s/modularity%s' % \
        (os.environ['state_rec'], ss, density)
    q_val, iter_max1 = ge.max_q(subj_dir, ss, 1, density)
    q_val, iter_max2 = ge.max_q(subj_dir, ss, 2, density)
    q_val, iter_max3 = ge.max_q(subj_dir, ss, 3, density)
    q_val, iter_max4 = ge.max_q(subj_dir, ss, 4, density)

    trees = []
    suffix = 'r0.5_linksthresh_proportion.out.maxlevel_tree'
    tname_1 = 'iter%d.%s.%d.%s_%s' % (iter_max1, ss, 1, density, suffix)
    input1 = os.path.join(subj_dir, tname_1)
    tree1 = np.loadtxt(input1, dtype=int)[:, 1]
    trees.append(tree1)
    tname_2 = 'iter%d.%s.%d.%s_%s' % (iter_max1, ss, 2, density, suffix)
    input2 = os.path.join(subj_dir, tname_2)
    tree2 = np.loadtxt(input2, dtype=int)[:, 1]
    trees.append(tree2)
    tname_3 = 'iter%d.%s.%d.%s_%s' % (iter_max1, ss, 3, density, suffix)
    input3 = os.path.join(subj_dir, tname_3)
    tree3 = np.loadtxt(input3, dtype=int)[:, 1]
    trees.append(tree3)
    tname_4 = 'iter%d.%s.%d.%s_%s' % (iter_max1, ss, 4, density, suffix)
    input4 = os.path.join(subj_dir, tname_4)
    tree4 = np.loadtxt(input4, dtype=int)[:, 1]
    trees.append(tree4)

    combos = [c for c in combinations(range(4), 2)]
    out = np.empty(len(combos))
    for i, co in enumerate(combos):
        out[i] = ge.normalized_MI(trees[co[0]], trees[co[1]])
    return out


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
            out_array[ss[0], cc[0]] = ge.q_nmod_corr(ss[1], cc[1], '5p', subj_dir)[0]

    return out_array


if __name__ == '__main__':

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW',
                 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS',
                 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']

    import pandas as pd
    from itertools import combinations
    condition_names = ['HighlyOrdered', 'SomewhatOrdered',
                       'Random', 'AlmostRandom']
    column_names = [cc for cc in combinations(condition_names, 2)]
    out_mat = np.empty(len(subj_list)*len(column_names))
    out_mat = out_mat.reshape(len(subj_list), len(column_names))
    for i, ss in enumerate(subj_list):
        out_mat[i, :] = nmi_evaluation(ss, '5p')

    nmi_out_frame = pd.DataFrame(out_mat,
                                 index=subj_list, columns=column_names)
    nmi_out_frame.to_csv('%s/state/nmi_evaluations.csv' % os.environ['t2'])
