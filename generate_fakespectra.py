import fake_spectra.spectra as fs
from fake_spectra.randspectra import RandSpectra

# snapshot number
snap = 31

# the directory the snapshot is in
snapdir = '/path/to/the/snapshot/'

# the directory to save the spectra file to
savedir = '/path/to/the/snapshot/SPECTRA_'+snap.zfill(3)

# the name of the resulting spectra file
savefile = 'fake-spectra.hdf5'

res = 1 # spectral resolution, we want it to be 1 km/s
        # this is much better than any observation would have
        # this doesn't have the correct spreading function for spectrograph resolution
        # use spec_utils.res_corr(tau, self.dvbin, self.spec_res) to correct for spectrograph resolution

ion = 1 #-1 for all hydrogen, 1 for neutral hydrogen

# if you want a set of randomly sampled sightlines use this function
# change the number of sightlines using the numlos argument
# thresh ensures you will get sightlines above the specified column density (cm-2)
# e.g. thresh = 10**20 will replace sightlines that don't have a column dnesity of at least 10**20 cm-2
rr = RandSpectra(snap, snapdir, thresh=0., res=res, savedir=savedir, savefile=savefile, numlos=5000)


# if you want spectra for specified sightlines use this function
# cofm is (N, 3) shape array with N being the number of sightlines you want and the 3 corresponding to x y z 
# axis is (N, 1) shape array with N being the number of sightlines and the 1 corresponding to 
# which axis your sightline runs along x y or z (1 2 or 3 respectively)
rr = fs.Spectra(snap, snapdir, res=res, savedir=savedir, savefile=savefile, cofm=cofm, axis=axis, reload_file=True, sf_neutral=False)
# sf_neutral - if True (the default) then gas on the star-forming equation of state is assumed to be neutral
# should only be true if used with a Springel-Hernquist star formation model in a version of Gadget/Arepo
# which incorrectly sets the neutral fraction in the star forming gas to less than unity

# grabs the column dnesities for sightlines
cds = rr.get_col_density("H",ion)

# grabs the optical depths for sightlines
taus = rr.get_tau("H", ion, 1215) # number is Lyman-alpha line in Angstroms
                                  # could change for other lines
# grabs the temperatures for sightlines
T = rr.get_temp("H", ion) 

rr.save_file() #Save spectra to file
