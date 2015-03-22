# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 19:30:32 2015

@author: andric
"""
import numpy as np


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
