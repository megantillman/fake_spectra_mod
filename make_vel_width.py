#!/usr/bin env python
# -*- coding: utf-8 -*-
"""Make some plots of the velocity widths from the cosmo runs"""

import matplotlib
matplotlib.use('PDF')

import matplotlib.pyplot as plt

import plot_spectra as ps
import vel_data
import os.path as path
import numpy as np
from save_figure import save_figure

base="/home/spb/scratch/Cosmo/"
outdir = base + "plots/"
print "Plots at: ",outdir
zrange = {54:(7,3.5), 60:None, 68:(2.5,0)}
colors = {0:"red", 2:"blue", 3:"green"}
lss = {0:"--",2:"-",3:"-."}

def plot_vel_width_sim(sim, snap, color="red", ff=True, HI_cut = None):
    """Load a simulation and plot its velocity width"""
    halo = "Cosmo"+str(sim)+"_V6"
    if ff:
        halo+="_512"
    #Load from a save file only
    hspec = ps.PlottingSpectra(snap, base+halo, None, None)
    hspec.plot_vel_width("Si", 2, color=color, HI_cut = HI_cut)

def plot_sep_frac(sim, snap):
    """Plot fraction of lines from separated halos"""
    halo = "Cosmo"+str(sim)+"_V6_512"
    #Load from a save file only
    hspec = ps.PlottingSpectra(snap, base+halo, None, None)
    hspec.plot_sep_frac()

def plot_rel_vel_width(sim1, sim2, snap, color="black"):
    """Load and make a plot of the difference between two simulations"""
    halo1 = "Cosmo"+str(sim1)+"_V6"
    halo2 = "Cosmo"+str(sim2)+"_V6"
    hspec1 = ps.PlottingSpectra(snap, base+halo1)
    (vbin, vels1) = hspec1.vel_width_hist("Si", 2)
    hspec1 = ps.PlottingSpectra(snap, base+halo2)
    (vbin, vels2) = hspec1.vel_width_hist("Si", 2)
    mm = np.min((np.size(vels2), np.size(vels1)))
    plt.semilogx(vbin[:mm], vels2[:mm]/vels1[:mm], color=color)

def plot_spectrum(sim, snap, num):
    """Plot a spectrum"""
    halo = "Cosmo"+str(sim)+"_V6_512"
    #Load from a save file only
    hspec = ps.PlottingSpectra(snap, base+halo, None, None)
    tau = hspec.get_observer_tau("Si", 2, num)
    hspec.plot_spectrum(tau)
    plt.xlim(1000,1500)

    save_figure(path.join(outdir,"cosmo"+str(sim)+"_Si_spectrum"))
    plt.clf()
    vels = hspec.vel_width(hspec.get_observer_tau("Si",2))
    ind = np.where(vels == np.max(vels[hspec.get_filt("Si",2)]))[0][0]
    tau2 = hspec.get_observer_tau("Si",2,ind)
    hspec.plot_spectrum(tau2)
    save_figure(path.join(outdir,"cosmo"+str(sim)+"_maxv_Si_spectrum"))
    plt.clf()


def plot_spectrum_density_velocity(sim, snap, num):
    """Plot a spectrum"""
    halo = "Cosmo"+str(sim)+"_V6_512"
    #Load from a save file only
    hspec = ps.PlottingSpectra(snap, base+halo)
    hspec.plot_spectrum_density_velocity("Si",2, num)
    save_figure(path.join(outdir,"cosmo"+str(sim)+"_tdv_Si_spectrum"))
    plt.clf()

def plot_metallicity(sim, snap, ff=True):
    """Plot a spectrum"""
    halo = "Cosmo"+str(sim)+"_V6"
    out = "cosmo"+str(sim)+"_metallicity_z"+str(snap)
    if ff:
        halo+="_512"
        out+="_512"
    #Load from a save file only
    hspec = ps.PlottingSpectra(snap, base+halo, None, None)
    hspec.plot_metallicity()
    vel_data.plot_alpha_metal_data(zrange[snap])
    save_figure(path.join(outdir,out))
    plt.clf()
    out = "cosmo"+str(sim)+"_correlation_z"+str(snap)
    if ff:
        out+="_512"
    hspec.plot_Z_vs_vel_width()
    vel_data.plot_prochaska_2008_correlation()
    save_figure(path.join(outdir,out))
    plt.clf()
    (redshift, met, vels) = vel_data.load_data()
    print "KS test is : ",hspec.kstest(10**met, vels)

def plot_vel_widths_sims(snap):
    """Plot some velocity width data at a particular redshift"""
    #Load sims
    hspec0 = ps.PlottingSpectra(snap, base+"Cosmo0_V6_512")
    hspec2 = ps.PlottingSpectra(snap, base+"Cosmo2_V6_512")
    hspec3 = ps.PlottingSpectra(snap, base+"Cosmo3_V6_512")
    #Make abs. plot
    hspec0.plot_vel_width("Si", 2, color=colors[0], ls=lss[0])
    hspec2.plot_vel_width("Si", 2, color=colors[2], ls=lss[2])
    hspec3.plot_vel_width("Si", 2, color=colors[3], ls=lss[3])
    if snap == 60:
        vel_data.plot_prochaska_2008_data(zrange[snap], 9)
    else:
        vel_data.plot_prochaska_2008_data(zrange[snap])
    save_figure(path.join(outdir,"cosmo_feedback_z"+str(snap)))
    plt.clf()
    #Make rel plot
    (vbin, vels0) = hspec0.vel_width_hist("Si", 2)
    (vbin, vels2) = hspec2.vel_width_hist("Si", 2)
    (vbin, vels3) = hspec3.vel_width_hist("Si", 2)
    mm = np.min((np.size(vels3), np.size(vels2),np.size(vels0)))
    plt.semilogx(vbin[:mm], vels0[:mm]/vels2[:mm], color=colors[0],ls=lss[0])
    plt.semilogx(vbin[:mm], vels3[:mm]/vels2[:mm], color=colors[3],ls=lss[3])
    plt.xlim(10, 1000)
    save_figure(path.join(outdir,"cosmo_rel_vel_z"+str(snap)))
    plt.clf()

def plot_vel_widths_res(snap):
    """Plot some velocity width data at a particular redshift"""
    #Load sims
    hspec0 = ps.PlottingSpectra(snap, base+"Cosmo0_V6")
    hspec512 = ps.PlottingSpectra(snap, base+"Cosmo0_V6_512")
    #Make abs. plot
    hspec0.plot_vel_width("Si", 2, color="blue", ls="--")
    hspec512.plot_vel_width("Si", 2, color="red", ls="-")
    vel_data.plot_prochaska_2008_data(zrange[snap])
    save_figure(path.join(outdir,"cosmo_feedback_res_z"+str(snap)))
    plt.clf()
    #Make rel plot
    (vbin, vels0) = hspec0.vel_width_hist("Si", 2)
    (vbin, vels2) = hspec512.vel_width_hist("Si", 2)
    mm = np.min((np.size(vels2),np.size(vels0)))
    plt.semilogx(vbin[:mm], vels0[:mm]/vels2[:mm], color="blue",ls="-")
    plt.xlim(10, 1000)
    save_figure(path.join(outdir,"cosmo_rel_vel_res_z"+str(snap)))
    plt.clf()

def plot_vel_redshift_evo(sim):
    """Plot the evolution with redshift of a simulation"""
    halo = "Cosmo"+str(sim)+"_V6_512"
    hspec0 = ps.PlottingSpectra(54, base+halo)
    (vbin, vels4) = hspec0.vel_width_hist("Si", 2)
    hspec0 = ps.PlottingSpectra(60, base+halo)
    (vbin, vels3) = hspec0.vel_width_hist("Si", 2)
    hspec0 = ps.PlottingSpectra(68, base+halo)
    (vbin, vels2) = hspec0.vel_width_hist("Si", 2)
    mm = np.min((np.size(vels2), np.size(vels3),np.size(vels4)))
    #Normalised by z=3
    plt.semilogx(vbin[:mm], vels3[:mm]/vels2[:mm], color="black",ls="--")
    plt.semilogx(vbin[:mm], vels4[:mm]/vels2[:mm], color="grey",ls="-")
    plt.xlim(10, 1000)
    plt.ylim(0,2)
    save_figure(path.join(outdir,"cosmo_"+str(sim)+"_zz_evol"))
    plt.clf()

if __name__ == "__main__":
#     colors=["blue", "purple", "orange", "red"]

#     for ss in (0,2,3):
#         print "Metallicity Simulation",ss
#         for zz in (54,60,68):
#             plot_metallicity(ss, zz,True)
#
#     for ss in (0,2,3):
#         plot_spectrum_density_velocity(ss,60, 15)
#         plot_spectrum(ss,60, 457)
#       plot_spectrum(2,60, 272)

    for ss in (0,2,3):
        plot_sep_frac(ss,60)
    save_figure(path.join(outdir,"cosmo_sep_frac_z3"))
    plt.clf()

#     for zz in (54, 60, 68):
#         plot_vel_widths_sims(zz)
#         plot_vel_widths_res(zz)


#     for ss in (0,2,3):
#         plot_vel_redshift_evo(ss)
