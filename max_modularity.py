# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:19:47 2015

@author: andric
"""
import os
import time
import numpy as np
from collections import Counter
from scipy.stats import friedmanchisquare, wilcoxon
from itertools import combinations


class modularity_evaluation:

    def __init__(self, directory, subject, condition, density):
        print 'Initializing modularity evaluation -- %s' % time.ctime()
        self.subjid = subject
        print 'Subject: %s' % self.subjid
        self.cc = condition
        print 'Condition: %s' % self.cc
        self.dens = density
        print 'Density: %s' % self.dens
        self.dir = directory
        print 'Directory: %s' % self.dir

    def max_q(self):
        """
        Get the maximum modularity value
        :param directory: In each directory is 100 Qval files
        """
        print 'Getting max q value -- %s' % time.ctime()
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
        print 'Getting number of modules -- %s' % time.ctime()
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
        subj_dir = '%s/%s/modularity%s' % (os.environ['state'], ss[1], density)
        for cc in xrange(4):   # the four conditions
            me = modularity_evaluation(subj_dir, ss[1], cc+1, density)
            q_value_array[ss[0], cc], iter_array[ss[0], cc] = me.max_q()
            n_mods_array[ss[0], cc] = me.n_modules()

    q_out_report = []
    n_mod_out_report = []

    print 'Doing tests \nFriedman chi square... %s' % time.ctime()
    q_vals_chi, q_vals_p = friedmanchisquare(q_value_array[:, 0], q_value_array[:, 1], q_value_array[:, 2], q_value_array[:, 3])
    q_out_report.append('Friedman test result -- ChiSq: %s, p-val: %s' % (q_vals_chi, q_vals_p))
    n_mods_chi, n_mods_p = friedmanchisquare(n_mods_array[:, 0], n_mods_array[:, 1], n_mods_array[:, 2], n_mods_array[:, 3])
    n_mod_out_report.append('Friedman test result -- ChiSq: %s, p-val: %s' % (n_mods_chi, n_mods_p))

    combos = combinations(range(4), 2)   # every pair of conditions
    print 'Wilcox tests.. %s' % time.ctime()
    for co in combos:
        qstat, qp = wilcoxon(q_value_array[:, co[0]], q_value_array[:, co[1]])
        q_out_report.append('Wilcoxon on conditions %s and %s: %s, p-val %s' % (co[0]+1, co[1]+1, qstat, qp))
        nstat, nmods_p = wilcoxon(n_mods_array[:, co[0]], n_mods_array[:, co[1]])
        n_mod_out_report.append('Wilcoxon on conditions %s and %s: %s, p-val %s' % (co[0]+1, co[1]+1, nstat, nmods_p))

    return (q_value_array, n_mods_array, q_out_report, n_mod_out_report)


if __name__ == '__main__':

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']

    for density in ['5p', '8p', '12p', '15p']:
        qs_array, nmods_array, qs_rep, nmods_rep = network_evaluations(subj_list, density)
    
        outf = open('%s/max_q_values_density%s_report.txt' % (os.environ['interim_state'], density), 'w')
        outf.write('\n'.join(qs_rep))
        outf.close()
        outf = open('%s/max_q_n_mods_density%s_report.txt' % (os.environ['interim_state'], density), 'w')
        outf.write('\n'.join(nmods_rep))
        outf.close()
        np.savetxt('%s/max_q_values_density%s_array.txt' % (os.environ['interim_state'], density), qs_array, fmt='%.4f')
        np.savetxt('%s/max_q_n_mods_density%s_array.txt' % (os.environ['interim_state'], density), nmods_array, fmt='%i')
