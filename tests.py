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

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    subj_list= ['ANGO']
    for ss in subj_list:
        out_dir = '%s/state/global_connectivity/' % os.environ['t2']
        input_dir = '%s/%s/corrTRIM_BLUR' % (os.environ['state_rec'], ss)
        for cc in xrange(1, 5):
            input_ts = 'cleanTS.%d.%s_graymask_dump' % (cc, ss)
            out_name = 'avg_corrZ_%d_%s' % (cc, ss)
            np.savetxt(os.path.join(out_dir, out_name), ge.avg_global_connectivity(os.path.join(input_dir, input_ts)), fmt='%.4f')
