# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:28:08 2015

@author: andric
"""

import os
import sys
import procedures as procs
import shutil
from glob import glob


if __name__ == '__main__':

    subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW', 'LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW']
    # subj_list = ['LDMW', 'FLTM', 'EEPA', 'DNLN', 'CRFO', 'ANMS']
    # subj_list = ['MRZM', 'MRVV', 'MRMK', 'MRMC', 'MRAG', 'MNGO', 'LRVN']
    # ss = sys.argv[1]
    for ss in subj_list:
        epis = []
        for cc in xrange(1, 5):
            epis.append('%s/%s/blur.%d.%s.steadystate.TRIM+orig.' % (os.environ['state_rec'], ss, cc, ss))
        epilist = ' '.join(epis)
        os.chdir('%s/state/%s' % (os.environ['t2'], ss))
        print os.getcwd()
        outprefix = '%s_avgepi' % ss
        procs.avgepis(ss, epilist, outprefix)
