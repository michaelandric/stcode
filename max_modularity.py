# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:19:47 2015

@author: andric
"""
import os
import numpy as np
from collections import Counter
from scipy.stats import friedmanchisquare, wilcoxon
from itertools import combinations


class modularity_evaluation:

    def __init__(self, directory, subject, condition, density):
        self.ss = subject
        self.cc = condition
        self.dens = density
        self.dir = directory

    def max_q(self):
        """
        Get the maximum modularity value
        :param directory: In each directory is 100 Qval files
        """
        q_vals = np.zeros(100)
        for i in xrange(100):
            fname = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.Qval' % (i+1, self.subjid, self.cc, self.dens)
            q_vals[i] = np.genfromtxt(os.path.join(self.dir, fname))
        self.iter_max = q_vals.argmax()+1

        return (np.max(q_vals), self.iter_max)

    def n_modules(self):
        """
        Get the number of modules
        """
        n_mods = np.zeros(100)
        tname = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.maxlevel_tree' % (self.iter_max, self.subjid, self.cc, self.dens)
        tree = np.genfromtxt(os.path.join(self.dir, tname))
        cnts = np.array(Counter(tree[:, 1]).values())
        n_mods = len(cnts[np.where(cnts > 1)])

        return n_mods


def network_evaluations(subj_list, density):
    """
    Determine q values and number of modules at max modularity
    """
    q_value_array = np.zeros(len(subj_list*4)).reshape(len(subj_list), 4)
    n_mods_array = np.zeros(len(subj_list*4)).reshape(len(subj_list), 4)
    iter_array = np.zeros(len(subj_list*4)).reshape(len(subj_list), 4)

    for ss in enumerate(subj_list):
        subj_dir = '%s/%s/modularity%s' % (os.environ['state'], ss, density)
        for cc in xrange(4):   # the four conditions
            me = modularity_evaluation(subj_dir, ss, cc+1, density)
            q_value_array[ss[0], cc], iter_array[ss[0], cc] = me.max_q()
            n_mods_array[ss[0], cc] = me.n_modules()

    q_out_report = []
    n_mod_out_report = []

    q_vals_chi, q_vals_p = friedmanchisquare(q_value_array[:, 0], q_value_array[:, 1], q_value_array[:, 2], q_value_array[:, 3])
    q_out_report.append('Friedman test result -- ChiSq: %s, p-val: %s' % (q_vals_chi, q_vals_p))
    n_mods_chi, n_mods_p = friedmanchisquare(n_mods_array[:, 0], n_mods_array[:, 1], n_mods_array[:, 2], n_mods_array[:, 3])
    n_mod_out_report.append('Friedman test result -- ChiSq: %s, p-val: %s' % (n_mods_chi, n_mods_p))

    combos = combinations(range(1,5), 2)   # every pair of conditions
    for co in combos:
        qstat, qp = wilcoxon(q_value_array[:, co[0]], q_value_array[:, co[1]])
        q_out_report.append('Wilcoxon on conditions %s and %s: %s, p-val %s' % (co[0], co[1], qstat, qp))
        nstat, np = wilcoxon(n_mods_array[:, co[0]], n_mods_array[:, co[1]])
        n_mod_out_report.append('Wilcoxon on conditions %s and %s: %s, p-val %s' % (co[0], co[1], nstat, np))

    return (q_out_report, n_mod_out_report)


if __name__ == '__main__':

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    density = '5p'

    qs_rep, nmods_rep = network_evaluations(subj_list, density)

    outf = open('%s/q_values_density%s_report.txt' % (os.environ['interim_state'], density))
    outf.write('\n'.join(qs_rep))
    outf.close()
    outf = open('%s/n_mods_density%s_report.txt' % (os.environ['interim_state'], density))
    outf.write('\n'.join(nmods_rep))
    outf.close()
