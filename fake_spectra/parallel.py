import fake_spectra
#print("fake_spectra imported")
from fake_spectra.randspectra import RandSpectra
#print("haloassigned_spectra imported")
from fake_spectra.plot_spectra import PlottingSpectra
#print("PlottingSpectra imported")
from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

numlos = 1000
ndla = 1000

### the array to store added column density in



if rank ==0 :
    
    found = 0

    while (found < 1000) :

        col_den_added = np.empty(shape=(numlos,))

        ### Recieve col_den from all other ranks and add them together
        comm.Reduce(np.empty(numlos, dtype='d'), col_den_added, op = MPI.SUM, root = 0)
        
        ### indices which should be replaced
        ind = np.where(col_den_added > 10**20.3)
        size_ind = np.size(ind)
        found += size_ind
        ### Here, Broadcast not_DLA_indices to each rank to be regenrated


        comm.bcast(size_ind, root=0)
        comm.Bcast(ind, root = 0)




    ### Save Final Data

    rr.savefile()



if rank ==1 :
    
    #num_DLA = 0# just for first iteration  of the while below
    rank_str = str(rank)
    rr = RandSpectra(34, "/rhome/mqezl001/bigdata/TNG/TNG100-1/output/snapdir_034/0/", MPI, comm,  thresh = 0.0, kernel='tophot',ndla = 1000, numlos=1000,savedir="/rhome/mqezl001/bigdata/TNG/TNG100-1/postprocessing/randspectra/Snap_034/parallel", savefile="spectra_34.0.hdf5")

    #### Calculate spectra for 100 hdf5 files
    rr.get_tau("H",1,1215)
    #Lyman-beta
    rr.get_tau("H",1,1025)
    rr.get_col_density("H",1)
    rr.get_col_density("H",-1)
    

    """
    while(num_DLA < 1000) :
    
        H1_DLA = np.empty_like()
        rr.replace_not_DLA(ndla, thresh, elem=elem, ion=ion, DLA_indices)

        #### Calculate spectra for 100 hdf5 files
        tau_1215 = rr.get_tau("H", 1,1215)
        tau_1025 = rr.get_tau("H", 1, 1025)
        col_den_total = rr.get_col_density("H",1)
        col_den_HI = rr.get_col_density('H', -1)
        cdsum = np.sum(col_den_HI, axis=1)


        ### Send col_den to root rank
        comm_Reduce(cdsum, col_den_added, op=MPI.SUM, root=0)
        

        ### Here, get not_DLA_indices and if there are still some non_DLA, regenerate spectra for those indices            
        ### Recieve not_DLA_indices from manager rank
        num_DLA = comm.bcast(root=0)
        ind = np.empty(num_DLA, dtype='d')
        comm.Bcast(ind, root=0)
            
    """

if rank ==2 :
    
    #num_DLA = 0# just for first iteration  of the while below
    rank_str = str(rank)
    rr = RandSpectra(34, "/rhome/mqezl001/bigdata/TNG/TNG100-1/output/snapdir_034/1/", MPI, comm,  thresh = 0.0, kernel='tophot',ndla = 1000, numlos=1000,savedir="/rhome/mqezl001/bigdata/TNG/TNG100-1/postprocessing/randspectra/Snap_034/parallel", savefile="spectra_34.0.hdf5")

    #### Calculate spectra for 100 hdf5 files
    rr.get_tau("H",1,1215)
    #Lyman-beta
    rr.get_tau("H",1,1025)
    rr.get_col_density("H",1)
    rr.get_col_density("H",-1)
        
if rank ==3 :
    
    #num_DLA = 0# just for first iteration  of the while below
    rank_str = str(rank)
    rr = RandSpectra(34, "/rhome/mqezl001/bigdata/TNG/TNG100-1/output/snapdir_034/2/", MPI, comm,  thresh = 0.0, kernel='tophot',ndla = 1000, numlos=1000,savedir="/rhome/mqezl001/bigdata/TNG/TNG100-1/postprocessing/randspectra/Snap_034/parallel", savefile="spectra_34.0.hdf5")

    #### Calculate spectra for 100 hdf5 files
    rr.get_tau("H",1,1215)
    #Lyman-beta
    rr.get_tau("H",1,1025)
    rr.get_col_density("H",1)
    rr.get_col_density("H",-1)



if rank ==4 :
    
    #num_DLA = 0# just for first iteration  of the while below
    rank_str = str(rank)
    rr = RandSpectra(34, "/rhome/mqezl001/bigdata/TNG/TNG100-1/output/snapdir_034/3/", MPI, comm,  thresh = 0.0, kernel='tophot',ndla = 1000, numlos=1000,savedir="/rhome/mqezl001/bigdata/TNG/TNG100-1/postprocessing/randspectra/Snap_034/parallel", savefile="spectra_34.0.hdf5")

    #### Calculate spectra for 100 hdf5 files
    rr.get_tau("H",1,1215)
    #Lyman-beta
    rr.get_tau("H",1,1025)
    rr.get_col_density("H",1)
    rr.get_col_density("H",-1)

if rank ==5 :
    
    #num_DLA = 0# just for first iteration  of the while below
    rank_str = str(rank)
    rr = RandSpectra(34, "/rhome/mqezl001/bigdata/TNG/TNG100-1/output/snapdir_034/4/", MPI, comm,  thresh = 0.0, kernel='tophot',ndla = 1000, numlos=1000,savedir="/rhome/mqezl001/bigdata/TNG/TNG100-1/postprocessing/randspectra/Snap_034/parallel", savefile="spectra_34.0.hdf5")

    #### Calculate spectra for 100 hdf5 files
    rr.get_tau("H",1,1215)
    #Lyman-beta
    rr.get_tau("H",1,1025)
    rr.get_col_density("H",1)
    rr.get_col_density("H",-1)


