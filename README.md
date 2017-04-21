# BAO_correlation

  Input files are put into data_south/, data_north/, random_south/, and random_north/. Input files are converted from spherical coordinates to cartesian and weighted based off of the input files in Spherical-to-Cartesian.py. They are then correlated to each other using the function on the NERSC server, which is called using the sgc.ini and sgc.sl scripts. The sgc.ini file can be generated using print_sgc.py. Before correlating, must first create and set up destination folder using mkResultFile.sh, which is in the calculation folder.
  After correlated data is put into calculation/result under the names result_{south/north}_{file number}-{norm/DD/DR/RR}.dat. The correlation function is then calculated from this data set in cal_cor.py. The legendre polynomials are calculated in the xi2dTOxiLegendre_Cmu_spline.py. Then each file is plotted individually in the plot_corr.py. To run a range of files, use run.sh. To plot the average of all the files run many_plot_corr.py (WARNING: must run all the files individually before all at once)


FILE
INPUT ARGUMENT
INPUT FILE
OUTPUT

Spherical-to-Cartesian.py (Can use the python module 2.7-anaconda or 3.4-anaconda on NERSC Edison)
'data_north' or 'data_south' or 'random_south' or 'random_north'//which folder to read from
{argument1}/cmass_dr11_{north/south/north_randoms/south_randoms (does automatically from arugment)}_ir{4000+file_number}.v11.1.release.txt
{4000+file_number}_{data_north/data_south/random_north/random_south (does automatically from arugment)}.xyzw 

print_sgc.py (Can use the python module 2.7-anaconda or 3.4-anaconda on NERSC Edison)
N/A (file range is hardcoded)
N/A
sgc.ini (results in sgc.ini file that will run using the data from my NERSC account and only south)

mkResultFile.sh
N/A
N/A
returns a set up result folder ready to go with the folder name as 'result' and the files as result_south_{file number}-{norm/DD/DR/RR}.dat

cal_cor.py (Use the python module 2.7-anaconda)
{file_number}
result/result_south_{file number}-{norm/DD/DR/RR}.dat
xi2d/xi2d-{file_number}.txt

xi2dTOxiLegendre_Cmu_spline.py (Use the python module 2.7-anaconda)
{path to correlation function location}
xi2d/xi2d-{file_number}.txt
xi2d/xi2d-{file_number}.txt_L02s (returns xi2d/xi2d-{file_number}.txt_L021s if monopole)

plot_corr.py(Use the python module 2.7-anaconda)
{file_number}
xi2d/xi2d-{file_number}.txt_L02s
plots/corr_R_{file_number}.png

run.sh
N/A (range of files is hard coded)
result/result_south_{file number}-{norm/DD/DR/RR}.dat
plots/corr_R_{file_number}.png

many_plot_corr.py (Can use the python module 2.7-anaconda or 3.4-anaconda on NERSC Edison)
{start file_number} {end file_number} (inclusive)
xi2d/xi2d-{file_number}.txt_L02s (file_number iterates through start and end inclusive)
corr_{start file_number}-{end file_number}.png avg_corr_fun.txt (avg_corr_fun.txt prints the values plotted)

  
TODO:
  *Add southern or northern hemisphere argument in cal_cor.py
  *Add file number range argument to Spherical-to-Cartesian.py
  *Add file number range argument to print_sgc.py
  *Change print_sgc.py to use files from folder and not from my NERSC account location
  *Add file number range argument to mkResultFile.sh
  *Expand mkResultFile.sh for north as well as south
  *Expand print_sgc.py to handle north and south
