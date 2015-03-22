# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 23:18:06 2015

@author: andric
"""

import time
import os
import numpy as np
from collections import Counter


def max_q(directory, subjid, cc, dens):
    """
    Get the maximum modularity value
    :param subjid: Subject identifier
    ;param cc: condition number
    :param dens: density identifer
    :param directory: the directory where the iterations are
    :return : max q valu, iteration with max q value
    """
    print 'Getting max q value -- %s' % time.ctime()
    q_vals = np.zeros(100)
    for i in xrange(100):
        fname = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.Qval' % (i+1, subjid, cc, dens)
        q_vals[i] = np.genfromtxt(os.path.join(directory, fname))
    iter_max = q_vals.argmax()+1

    return (np.max(q_vals), iter_max)


def n_modules(subjid, cc, dens, iter_max, directory):
    """
    Get the number of modules
    :param subjid: Subject identifier
    ;param cc: condition number
    :param dens: density identifer
    :param directory: the directory where the iterations are
    :return : number of modules
    """
    print 'Getting number of modules -- %s' % time.ctime()
    n_mods = np.zeros(100)
    tname = 'iter%d.%s.%d.%s_r0.5_linksthresh_proportion.out.maxlevel_tree' % (iter_max, subjid, cc, dens)
    tree = np.genfromtxt(os.path.join(directory, tname))
    cnts = np.array(Counter(tree[:, 1]).values())
    n_mods = len(cnts[np.where(cnts > 1)])

    return n_mods


def snsc(input1, input2):
    """
    Get Single Node Set Consistency (SNSC) between two partitions
    Each input is a separate file, result of tree output from modularity function
    """
    input1 = np.genfromtxt(input1)
    input2 = np.genfromtxt(input2)
    coms1 = input1[:, input1.shape[1]-1]
    coms2 = input2[:, input2.shape[1]-1]
    mod_dict1 = {}
    mod_dict2 = {}
    for i in np.unique(coms1):
        mod_dict1[i] = [v for v, c in enumerate(coms1) if c == i]
    for i in np.unique(coms2):
        mod_dict2[i] = [v for v, c in enumerate(coms2) if c == i]

    preservation = np.zeros(len(coms2))
    """Return 777 if the community includes less than 20 voxels """
    for i in xrange(len(coms2)):
        if len(mod_dict2[coms2[i]]) < 20 or len(mod_dict1[coms1[i]]) < 20:
            preservation[i] = 777
        else:
            inter = len(set(mod_dict2[coms2[i]]).intersection(set(mod_dict1[coms1[i]])))
            preservation[i] = inter / float(len(mod_dict2[coms2[i]]))

    return preservation


def dummyvar(cis, return_sparse=False):
    '''
    This is an efficient implementation of matlab's "dummyvar" command
    using sparse matrices.
    input: partitions, NxM array-like containing M partitions of N nodes
        into <=N distinct communities
    output: dummyvar, an NxR matrix containing R column variables (indicator
        variables) with N entries, where R is the total number of communities
        summed across each of the M partitions.
        i.e.
        r = sum((max(len(unique(partitions[i]))) for i in range(m)))
    '''
    # num_rows is not affected by partition indexes
    n = np.size(cis, axis=0)
    m = np.size(cis, axis=1)
    r = np.sum((np.max(len(np.unique(cis[:, i])))) for i in range(m))
    nnz = np.prod(cis.shape)

    ix = np.argsort(cis, axis=0)
    # s_cis=np.sort(cis,axis=0)
    # FIXME use the sorted indices to sort by row efficiently
    s_cis = cis[ix][:, xrange(m), xrange(m)]

    mask = np.hstack((((True,),)*m,(s_cis[:-1,:]!=s_cis[1:,:]).T))
    indptr, = np.where(mask.flat)
    indptr = np.append(indptr, nnz)

    import scipy.sparse as sp
    dv = sp.csc_matrix((np.repeat((1, ), nnz), ix.T.flat, indptr), shape=(n, r))
    return dv.toarray()


def agreement(ci, buffsz=None):
    """
    Takes as input a set of vertex partitions CI of
    dimensions [vertex x partition]. Each column in CI contains the
    assignments of each vertex to a class/community/module. This function
    aggregates the partitions in CI into a square [vertex x vertex]
    agreement matrix D, whose elements indicate the number of times any two
    vertices were assigned to the same class.

    In the case that the number of nodes and partitions in CI is large
    (greater than ~1000 nodes or greater than ~1000 partitions), the script
    can be made faster by computing D in pieces. The optional input BUFFSZ
    determines the size of each piece. Trial and error has found that
    BUFFSZ ~ 150 works well.

    Inputs,     CI,     set of (possibly) degenerate partitions
                BUFFSZ, optional second argument to set buffer size

    Outputs:    D,      agreement matrix
    """
    m, n = ci.shape

    if buffsz is None:
        buffsz = 1000

    if n <= buffsz:
        ind = dummyvar(ci)
        D = np.dot(ind, ind.T)
    else:
        a = np.arange(0, n, buffsz)
        b = np.arange(buffsz, n, buffsz)
        if len(a) != len(b):
            b = np.append(b, m)
        D = np.zeros((m, m))
        for i, j in zip(a, b):
            y = ci[:, i:j+1]
            ind = dummyvar(y)
            D += np.dot(ind, ind.T)

    np.fill_diagonal(D, 0)
    return D
