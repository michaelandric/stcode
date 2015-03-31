# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 12:54:56 2015

@author: andric
"""

import os
import numpy as np
import pandas as pd


def get_clust_info(subj_list, conditions, maskname, method='mean'):
    """
    Having already subj data and Clust_mask to text files
    Get information about the clusters
    :param subj_list: List of subjects to collect data on
    :param conditions: This is a list type!
    :param maskname: The cluster mask, gives info what cluster is at what voxel
    :param method: "mean" by default, can also do "median"
    :returns : numpy array including cols for subj, condition, cluster num, values
    """
    print 'Getting cluster info \nDoing %s' % method
    mask = np.genfromtxt(maskname)   # has ijk + data, so 4 columns total
    mask = mask[:, 3]   # has ijk + data, so 4 columns total
    clusters = np.unique(mask)[np.unique(mask) != 0]
    vals = []
    for ss in subj_list:
        print 'Getting subject: %s' % ss
        subj_dir = '%s/state/global_connectivity/%s_res/' % (os.environ['t2'], ss)
        for cc in conditions:
            dat_pref = 'avg_corrZ_%d_%s_highres_fnirted_MNI2mm.txt' % (cc, ss)
            subj_dat = np.genfromtxt(os.path.join(subj_dir, dat_pref))
            subj_dat = subj_dat[:, 3]
            for cl in clusters:
                if method is 'mean':
                    vals.append(np.mean(subj_dat[np.where(mask == cl)]))
                elif method is 'median':
                    vals.append(np.median(subj_dat[np.where(mask == cl)]))
    subj_vec = subj_list*(len(clusters)*len(conditions))
    cond_vec = np.tile(np.repeat(conditions, len(clusters)), len(subj_list))
    clust_vec = np.tile(np.tile(clusters, len(conditions)), len(subj_list))

    return np.column_stack([subj_vec, cond_vec, clust_vec, vals])


if __name__ == "__main__":

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    os.chdir('%s/state/global_connectivity/group' % os.environ['t2'])
    print os.getcwd()
    conditions = range(1, 5)
    clust_mask = 'neglin_tstat_avg_corrZ_anova_Clust_mask+tlrc.txt'
    out = pd.DataFrame(get_clust_info(subj_list, conditions, clust_mask))
    out.to_csv('neglin_tstat_avg_corrZ_anova_Clust_mask+tlrc.cluster_info.csv')
