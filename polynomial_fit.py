# Marta Xiulan Aribó Herrera
# Autmun 2022/2023
# TFG
# Program to correct tilted spectra with a polynomial routine

#---------------------------------------------------------------------------
#                               LIBRARIES & FUNCTIONS
#---------------------------------------------------------------------------

import numpy as np
import matplotlib.pyplot as plt
import csv

plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Serif",
        "font.size":10
    })

def ReadFiles (CSV_file,energy,intensity):
    with open (CSV_file, newline = '') as file:
        reader = csv.reader(file, delimiter = ',')
        file.seek(0)
        next(reader, None)
        for fila in reader:
            energy.append(float(fila[0]))
            intensity.append(float(fila[1]))

def SaveFiles(energy,intensity,CSVTitle):
    with open (CSVTitle, 'w', newline = '') as CSV_file:
            write_csv = csv.writer(CSV_file, delimiter = ' ')
            write_csv.writerow(['Energy',"Intensity"])
            for j in range(0,len(intensity),1):
                write_csv.writerow([energy[j],intensity[j]])

def graph(x,y,x1,y1,GraphTitle,GraphFileTitle):
    
    plt.figure(figsize=(15,10))
    plt.plot(x,y,x1,y1,linewidth=1)

    plt.title(GraphTitle)
    plt.xlabel('Energy(eV)')
    plt.ylabel("Intensity")


    #plt.xticks([885,865,875,885])
     
    plt.savefig(GraphFileTitle + ".jpg",dpi=300)
    #plt.show()
    plt.close()

#---------------------------------------------------------------------------
#                         Body
#---------------------------------------------------------------------------


number_of_particles = 15

for particle in range(1,number_of_particles+1):

    intensity = list()
    energy = list()
    adjustment = list()
    CSV_file = "/Users/martaariboherrera/Desktop/TFG/Sample_2B/20220918_s15615_AbsorptionSpectrum_L2,3/particle_analysis/particle_analysis_sample_2B_1_LH/data_spectra/spectrum_particle_{}.csv".format(str(particle))
    ReadFiles(CSV_file,energy,intensity)

    #mask
    energy_not_masked = list()
    intensity_not_masked = list()

    for i in energy:
        if i < 850 :
            energy_not_masked.append(i)
            intensity_not_masked.append(intensity[energy.index(i)])
        if i >= 861 and i <= 868:
            energy_not_masked.append(i)
            intensity_not_masked.append(intensity[energy.index(i)])
        if i>876 :
            energy_not_masked.append(i)
            intensity_not_masked.append(intensity[energy.index(i)])

    #polynomial ajust
    pol_fit = np.polyfit(x=energy_not_masked, y=intensity_not_masked, deg=2)
    pol_deg_2 = np.poly1d(pol_fit) #polynomial object

    file = open("polynomial_ajust.txt", "a")
    file.write("Polynomial fit for the particle {} : {} \n ".format(str(particle),str(pol_deg_2)))


    #save files
    CSVTitle = "polynomial_fit_particle_"+str(particle)+ ".csv"
    SaveFiles(energy,intensity-pol_deg_2(energy),CSVTitle)

    #plot
    GraphTitle = "Original spectrum with the polynomial adjust for the particle {}".format(str(particle))
    GraphFileTitle = "polynomial_fit_particle_spectrum_{}".format(str(particle))
    graph(energy,intensity,energy_not_masked,pol_deg_2(energy_not_masked),GraphTitle,GraphFileTitle)

    GraphTitle = "Corrected spectrum for the particle {}".format(str(particle))
    GraphFileTitle = "corrected_spectrum_particle_{}".format(str(particle))
    graph(energy,intensity-pol_deg_2(energy),energy,intensity-pol_deg_2(energy),GraphTitle,GraphFileTitle)


file.close()

