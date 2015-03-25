# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 12:32:00 2015

The idea is to do epi_reg for mean_epi to the T1 in the .anat dir (from fsl_anat).
Then can apply the coeff already done to move this to MNI space

@author: andric
"""

import os
import time
from shlex import split
from subprocess import call, STDOUT


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
    print 'Doing epi_reg for %s -- ' % ss+time.ctime()
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
    cmdargs = split('applywarp -i %s -r %s -o %s --premat=%s --interp=nn' % (input, extrt1, out, premat))
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
    cmdargs = split('applywarp -i %s -r %s/data/standard/MNI152_T1_2mm.nii.gz -o %s -w %s --interp=nn' % (input, os.environ['FSLDIR'], out, coeff))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


if __name__ == "__main__":

    # subj_list = ['ANGO', 'CLFR', 'MYTP', 'TRCO', 'PIGL', 'SNNW']
    # subj_list = ['LDMW', 'FLTM', 'EEPA', 'DNLN']
    # subj_list = ['CRFO', 'ANMS', 'MRZM', 'MRVV', 'MRMK']
    subj_list = ['MRMC', 'MRAG', 'MNGO', 'LRVN']
    for ss in subj_list:
        for cc in xrange(1, 5):
            reg_dir = '%s/state/%s' % (os.environ['t2'], ss)
            os.chdir('%s/state/global_connectivity/%s_res' % (os.environ['t2'], ss))
            print os.getcwd()

            in_epi = 'avg_corrZ_%d_%s.ijk+orig' % (cc, ss)
            # converttoNIFTI(in_epi)

            # Section for FLIRT
            input_FL = 'avg_corrZ_%d_%s.ijk.nii.gz' % (cc, ss)
            extrt1 = '%s.SurfVol_Alnd_Exp.anat/T1_biascorr_brain.nii.gz' % ss
            premat = 'epi2anat_%s_meanepi.mat' % ss
            out_FL = 'avg_corrZ_%d_%s_highres_flirted_MNI2mm' % (cc, ss)
            applywarpFLIRT(ss, input_FL, os.path.join(reg_dir, extrt1), out_FL, os.path.join(reg_dir, premat))

            # Section for FNIRT
            input_FN = '%s.nii.gz' % out_FL
            coeff = '%s.SurfVol_Alnd_Exp.anat/T1_to_MNI_nonlin_coeff.nii.gz' % ss
            out_FN = 'avg_corrZ_%d_%s_highres_fnirted_MNI2mm' % (cc, ss)
            applywarpFNIRT(ss, input_FN, out_FN, os.path.join(reg_dir, coeff))
