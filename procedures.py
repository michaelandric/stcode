# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 12:28:34 2015

@author: andric
"""

import os
import time
import numpy as np
from shlex import split
from subprocess import call, STDOUT, Popen, PIPE


def gen_condor_submit_args(arg_list):
    """
    Generate condor_submit_file arguments
    """
    print 'arguments = %s \nqueue \n' % ' '.join(arg_list)


def undump(subjid, ijk_coords, datafilename, data_dir, master_file):
    """
    :param subjid: Subject identifier
    :param ijk_coords: IJK coordinates. GIVE FULL PATH
    :param datafilename: name of the data file that you want to undump
    :param data_dir: File where the data live
    :param master_file: The master file for AFNI voxel resolution. GIVE FULL PATH
    Writes AFNI format Undumped file
    """
    print 'Doing undump... \nFirst pasting ijk to data -- %s' % time.ctime()
    ijkfile = np.genfromtxt(ijk_coords)
    data = np.genfromtxt(os.path.join(data_dir, datafilename))
    data_ijk_outname = '%s.ijk' % os.path.join(data_dir, datafilename)
    np.savetxt(data_ijk_outname, np.column_stack([ijkfile, data]), fmt='%i %i %i %.4f')

    stdout_dir = 'stdout_files'
    if not os.path.exists(os.path.join(data_dir, stdout_dir)):
        os.makedirs(os.path.join(data_dir, stdout_dir))
    print 'Doing 3dUndump... %s' % time.ctime()
    f = open('%s/stdout_files/stdout_from_undump.txt' % data_dir, 'w')
    cmdargs = split('3dUndump -prefix %s -ijk -datum %s -master %s %s' % (data_ijk_outname, 'float', master_file, data_ijk_outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
    print 'Finished undump -- %s' % time.ctime()


def autotlrc(subjid, tlrc_brain, afni_data, data_dir):
    """
    :param subjid: Subject Identifier
    :param tlrc_brain: The brain in talairach space, GIVE FULL PATH
    :param afni_data: AFNI data in orig space that is going to talairach space
    :param data_dir: Where data live
    Writes out AFNI format file in group space
    """
    print 'Doing autotlrc  -- %s' % time.ctime()
    os.chdir(data_dir)   # @auto_tlrc requires you to be in current directory of data
    print os.getcwd()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('stdout_files/stdout_from_autotlrc.txt', 'w')
    cmdargs = split('@auto_tlrc -apar %s -input %s -rmode NN -dxyz 2' % (tlrc_brain, afni_data))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
    print 'Finished autotrlc -- %s' % time.ctime()


def nwarpapply(nwarp_algn_brain, affn_trans, afni_data, outpref, data_dir):
    """
    Doing 3dNwarpApply that derives from output of 3dQwarp
    """
    print 'Doing nwarpapply -- %s' % time.ctime()
    os.chdir(data_dir)
    print os.getcwd()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_nwarpapply.txt' % stdout_dir, 'w')
    cmdargs = split("3dNwarpApply -nwarp '%s %s' -source %s -master NWARP -ainterp NN -prefix %s" % (nwarp_algn_brain, affn_trans, afni_data, outpref))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
    print 'Finished NWARP -- %s' % time.ctime()


def maskdump(mask, afni_data, outname):
    """
    Dump AFNI image to text file.
    """
    print 'Doing maskdump -- %s' % time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    # f = open('%s/stdout_from_nwarpapply.txt' % stdout_dir, 'w')
    cmdargs = split('3dmaskdump -mask %s %s' % (mask, afni_data))
    serr = open('%s/stderr_from_maskdump.txt', 'w')
    dump_out = Popen(cmdargs, stdout=PIPE, stderr=PIPE).communicate()
    serr.write(dump_out[1])
    serr.close()
    f = open('%s' % outname)
    f.write(dump_out[0])
    f.close()
    print 'Finished maskdump -- %s' % time.ctime()


def vol2surf(hemi, parent, surfvol, pn, outname):
    """
    """
    print 'Doing maskdump -- %s' % time.ctime()
    os.chdir('/mnt/lnif-storage/urihas/uhproject/suma_tlrc')
    print os.getcwd()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_vol2surf.txt' % stdout_dir, 'w')
    cmdargs = split('3dVol2Surf -spec ./N27_%s_tlrc.spec \
                    -surf_A ./%s.smoothwm.tlrc.ply -surf_B ./%s.pial.tlrc.ply \
                    -sv %s -grid_parent %s \
                    -map_func max -f_steps 10 -f_index voxels \
                    -f_p1_fr -%s -f_pn_fr %s \
                    -outcols_NSD_format -oob_index -1 -oob_value 0.0 \
                    -out_1D %s' % (hemi, hemi, hemi, surfvol, parent, pn, pn, outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def afni2nifti(t1):
    """
    Wrapper to do AFNI program 3dAFNItoNIFTI
    """
    print 'AFNItoNIFTI... -- '+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_afnitonifti.txt' % stdout_dir, 'w')
    cmdargs = split('3dAFNItoNIFTI %s+orig.' % t1)
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
    print 'DONE... '+time.ctime()


def fslanat(t1pref):
    """
    Do fsl_anat.
    This creates whole directory of anatomy files in different config.
    """
    print 'Doing fslanat for %s -- ' % t1pref+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('stdout_files/stdout_from_fsl_anat.txt', 'w')
    fslargs = split('fsl_anat -i %s.nii.gz --weakbias' % t1pref)
    Popen(fslargs, stdout=f, stderr=STDOUT)
    f.close()


def avgepis(ss, epi_list, outpref):
    """
    Make average TS brain
    :param ss: Subject identifier
    :param epi_list: Include list of epis that you average over
    Writes to file a TS average brain
    """
    print 'Doing avgepis for %s -- ' % ss+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_avgepis.txt' % stdout_dir, 'w')
    cmdargs = split('3dMean -prefix %s %s' % (outpref, epi_list))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def mean_epi(ss, infile, outpref):
    """
    Average across TS mean brain to get one mean image.
    YOU SHOULD FIRST HAVE AN AVERAGE OF TS (MANY IMAGES) THAT YOU WANT TO MAKE MEAN (ONE IMAGE).
    This serves registration purposes.
    :param ss: Subject identifier
    Writes to file AFNI mean brain (one image)
    """
    print 'Doing mean_epi for %s -- ' % ss+time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s/stdout_from_mean_epi.txt' % stdout_dir, 'w')
    cmdargs = split('3dTstat -prefix %s -mean %s' % (outpref, infile))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def fwhm_est(input_data, outname, mask=None):
    """
    Estiamte FWHM of data
    Will return FWHM
    """
    print 'Doing fwhm_est -- %s' % time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('%s_fwhm_est_out.txt' % input_data, 'w')
    if mask is None:
        cmdargs = split('3dFWHMx -input %s -out %s' % (input_data, outname))
    else:
        cmdargs = split('3dFWHMx -mask %s -input %s -out %s' % (mask, input_data, outname))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()


def clustsim(fwhm, mask=None):
    """
    Find the size of clusters by chance
    """
    print 'Running clustsim -- %s' % time.ctime()
    stdout_dir = 'stdout_files'
    if not os.path.exists(stdout_dir):
        os.makedirs(stdout_dir)
    f = open('ClustSim_FWHM_%f_%f_%f_out.txt' % (fwhm[0], fwhm[1], fwhm[2]), 'w')
    if mask is None:
        cmdargs = split('3dClustSim -fwhmxyz %f %f %f' % (fwhm[0], fwhm[1], fwhm[2]))
    else:
        # cmdargs = split('3dClustSim -NN 123 -mask %s -fwhmxyz %f %f %f' % (mask, fwhm[0], fwhm[1], fwhm[2]))
        cmdargs = split('3dClustSim -NN 123 -mask %s -fwhmxyz %f %f %f' % (mask, fwhm[0], fwhm[1], fwhm[2]))
    call(cmdargs, stdout=f, stderr=STDOUT)
    f.close()
