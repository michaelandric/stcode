# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 12:32:00 2015

The idea is to do epi_reg for mean_epi to the T1 in the .anat dir (from fsl_anat).
Then can apply the coeff already done to move this to MNI space

@author: andric
"""

import os
import time
import shutil
from shlex import split
from subprocess import call
from subprocess import Popen
from subprocess import PIPE
from subprocess import STDOUT


def converttoNIFTI(brain):
    """
    convert AFNI file to NIFTI
    """
    print 'Doing converttoNIFTI for %s -- ' % brain+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_converttoNIFTI' % stdout_dir, 'w')
    cmdargs = split('3dAFNItoNIFTI %s' % brain)
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def epi_reg(ss, epi, wholet1, extrt1, out):
    """
    Register epi to t1
    """
    print 'Doing converttoNIFTI for %s -- ' % ss+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_epireg.txt' % stdout_dir, 'w')
    cmdargs = split('epi_reg --epi=%s --t1=%s --t1brain=%s --out=%s' % (epi, wholet1, extrt1, out))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFLIRT(ss, input, extrt1, out, premat):
    """
    Warp via linear transformation via fsl FLIRT
    """
    print 'doing applywarpFLIRT for %s -- ' % ss+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarpFLIRT.txt' % stdout_dir, 'w')
    cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s' % (input, extrt1, out, premat))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def applywarpFNIRT(ss, input, out, coeff):
    """
    Warp via nonlinear transformation via fsl FNIRT
    """
    print 'Doing applywarpFNIRT for %s -- ' % ss+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_applywarp.txt' % stdout_dir, 'w')
    decor = os.environ['decor']
    cmdargs = split('applywarp -i %s -r %s/groupstuff/MNI152_T1_2mm.nii.gz -o %s -w %s' % (input, decor, out, coeff))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
