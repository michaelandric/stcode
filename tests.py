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


if __name__ == '__main__':

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MNGO', 'LRVN']
    subj_list = ['TRCO']
    outdir = os.environ['t2']+'/state/snsc_results/'
    for ss in subj_list:
        snsc_res = snsc_evaluation(ss, outdir, '5p')
        outpref = 'snsc_%s.txt' % ss
        np.savetxt(os.path.join(outdir, outpref), snsc_res, fmt='%.4f')

    # MRAG is special, shy 1 voxel
    # mrag_res = snsc_evaluation('MRAG', outdir, '5p')
    # outpref = 'snsc_MRAG.txt'
    # np.savetxt(os.path.join(outdir, outpref), snsc_res, fmt='%.4f')
