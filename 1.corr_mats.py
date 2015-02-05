#!~/anaconda/bin/python

import pandas as pd
import numpy as np
import networkx as nx
import datetime
import sys
import os
from shlex import split
from subprocess import call
from subprocess import STDOUT


class GRAPHS:

    def __init__(self, subjid, condition, thresh_density):
        self.ss = subjid
        self.cc = condition
        self.dens = thresh_density
        self.tformat = "%a %b %d %H:%M:%S %Y"
        print 'Initializing. -- '+datetime.datetime.today().strftime(self.tformat)

    def make_graph(self, outname):
        print 'Now making graph -- '+datetime.datetime.today().strftime(self.tformat)
        ts = np.loadtxt('blur.%s.%s.steadystate.TRIM_graymask_dump' % (self.cc, self.ss))
        ts = pd.DataFrame(ts).T
        print 'Time series loaded \nStarting correlation -- '+datetime.datetime.today().strftime(self.tformat)
        corrmat = ts.corr()
        print 'Correlation matrix done. -- '+datetime.datetime.today().strftime(self.tformat)
        corrmatUT = np.triu(corrmat)
        np.fill_diagonal(corrmatUT, 0)
        print 'Starting sort. -- '+datetime.datetime.today().strftime(self.tformat)
        corrsrtd = np.sort(corrmatUT[corrmatUT !=0], kind='mergesort')
        print 'Sort done. \nThresholding... -- '+datetime.datetime.today().strftime(self.tformat)
        threshd = corrsrtd[int(len(corrsrtd)*(1-self.dens)):]
        print 'Thresholding done. \nNow getting edge indices -- '+datetime.datetime.today().strftime(self.tformat)
        ix = np.in1d(corrmatUT.ravel(), threshd).reshape(corrmatUT.shape)
        inds = zip(np.where(ix)[0], np.where(ix)[1])
        G = nx.Graph()
        print 'Graph initialized. \nAdding edges -- '+datetime.datetime.today().strftime(self.tformat)
        for ii in inds:
            G.add_edge(ii[0], ii[1])
        print 'Graph complete. \nWriting it to file -- '+datetime.datetime.today().strftime(self.tformat)
        nx.write_edgelist(G, outname, data=False)
        print 'Graph edgelist written out. \nDONE. -- '+datetime.datetime.today().strftime(self.tformat)

    def convert_graph(self, graph):
        '''This is to convert graph from text to binary file for community detection'''
        f = open('stdout_files/stdout_from_convert.txt', 'w')
        print 'Converting edgelist to binary for community detection -- '+datetime.datetime.today().strftime(self.tformat)
        cmdargs = split('community_convert -i '+graph+'  -o '+graph+'.bin')
        call(cmdargs, stdout=f, stderr=STDOUT)
        print 'Conversion done. -- '+datetime.datetime.today().strftime(self.tformat)
        f.close()


if __name__ == "__main__":
    if len(sys.argv) < 4:
        sys.stderr.write("You done fucked up! \n"
                         "Usage: %s <SUBJECT ID> <CONDITION ID> <THRESH DENSITY> \n" %
                        (os.path.basename(sys.argv[0]),))

    subjid = sys.argv[1]
    condition = sys.argv[2]
    thresh_density = sys.argv[3]

    os.chdir('/mnt/lnif-storage/urihas/MAstdstt/%s' % subjid)
    print os.getcwd()
    graph_outname = '/mnt/lnif-storage/urihas/MAstdstt/%s/graphs/%s.%s.dens_%s.edgelist' % (subjid, subjid, condition, thresh_density)
    GR = GRAPHS(subjid, condition, thresh_density)
    GR.make_graph(graph_outname)
    GR.convert_graph(graph_outname)
