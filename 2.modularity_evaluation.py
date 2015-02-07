#!~/anaconda/bin/python

import sys
import os
from subprocess import call
from shlex import split


def get_modularity(el, to, ms):
    f = open(to, 'w')
    m = open(ms, 'w')
    cmdargs = split('/home/michaeljames.andric/Community_latest/community -l -1 '+el+'.bin')
    call(cmdargs, stdout=f, stderr=m)
    f.close()
    m.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write("You done fucked up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                        (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]

    basedir = '/mnt/lnif-storage/urihas/MAstdstt'
    edgelist = '%s/%s/graphs/%s.%s.dens_%s.edgelist' % (basedir, subjid, subjid, condition, thresh_density)
    for n in xrange(100):
        treeoutname = '%s/%s/trees/iter%s.%s.%s.dens_%s.tree' % (basedir, subjid, n, subjid, condition, thresh_density)
        modscorename = '%s/%s/Qvals/iter%s.%s.%s.dens_%s.Qval' % (basedir, subjid, n, subjid, condition, thresh_density)
        get_modularity(edgelist, treeoutname, modscorename)