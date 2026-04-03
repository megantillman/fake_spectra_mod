from fake_spectra.spectra import Spectra
from fake_spectra.plot_spectra import PlottingSpectra
    
# we need the snapshot in order to generate temps
# path to the snapshot
snapdir = '/path/to/the/simulation/'
# name of the spectral file you want temps for
savefile = 'Lya-spectra.hdf5'

res = 1 # km/s, this is also the default
ion = 1 # -1 for all hydrogen, 1 for neutral hydrogen

snap = 145

# fake spectra looks for the spectral file in SPECTRA_XXX folders where XXX is the snapnumber
savedir = '/path/to/your/file/SPECTRA_'+snap 

# opening the file with the spectra module
spec = Spectra(int(snap), snapdir, cofm=None, axis=None, savedir=savedir, savefile=savefile)

# actually calculating the temperatures
print('\t Getting temps...')
T = spec.get_temp("H", ion)

# save spectra to file
spec.save_file() 

# the old file with be renamed to <savefile>.backup
print('\t Done.')


# Now we have the temps saved in the spectra file so at any point we can open the file are retrieve the values
# opening the spectra file
rs = PlottingSpectra(num=snap, base='path/to/your/SPECTRA_XXX/directories', savefile=savefile, label='Spectra')

# reload the temps for use
T = rs.get_temp("H", ion) 


