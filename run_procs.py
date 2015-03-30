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
    # input_pref = 'avg_corrZ_anova'
    # mask = '%s/data/standard/MNI152_T1_2mm.nii.gz' % os.environ['FSLDIR']
    # out_name = '%s_fwhm_est_out_p.05' % input_pref
    # procs.fwhm_est('%s+tlrc' % input_pref, out_name, mask)
    # fwhmvals = [5.50817, 5.91411, 5.89492]
    # fwhmvals = [9.16169, 10.2877, 10.193]
    # fwhmvals = [6, 6, 6]
    # for fwhmvals in [[5.50817, 5.91411, 5.89492], [9.16169, 10.2877, 10.193], [6, 6, 6]]:
    #    procs.clustsim(fwhmvals, mask)
    # procs.fdr('%s+tlrc' % input_pref, 'FDR_%s' % input_pref, mask)
    # parent_pref = 'Fvals_avg_corrZ_anova_Clust_mask'
    # parent_pref = 'neglin_tstat_avg_corrZ_anova_Clust_mask'
    # parent_pref = 'Fvals_mask_ClustVals_avg_corrZ_anova'
    parent_pref = 'neglin_mask_ClustVals_avg_corrZ_anova'
    pn = '1.0'
    # surfvol = 'TT_N27+tlrc'
    for hemi in ['lh', 'rh']:
        outname = '%s_%s_pn%s_MNI_N27.1D' % (parent_pref, hemi, pn)
        procs.vol2surf_mni(hemi, '%s+tlrc' % parent_pref, pn, outname)
        # procs.vol2surf(hemi, '%s+tlrc' % os.path.join(data_dir, parent_pref), surfvol, pn, outname)
