# Marta Xiulan Aribó Herrera
# Autmun 2022/2023
# TFG
# Program to plot intensities as a function of energy from Image J specific csv files.

#---------------------------------------------------------------------------
#                               LIBRARIES & FUNCTIONS
#---------------------------------------------------------------------------

import csv
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use('science')

def graph(x,y,GraphTitle,GraphFileTitle):
    
    plt.figure(figsize=(15,10))
    plt.plot(x,y,linewidth=1)

    plt.title(GraphTitle)
    plt.xlabel('Energy(eV)')
    plt.ylabel("Intensity")

    plt.savefig(GraphFileTitle + ".jpg",dpi=300)
    plt.close()

#---------------------------------------------------------------------------
#                         Body
#---------------------------------------------------------------------------

CSV_Sample= 'spectra_results_L.csv'

CSV_Energy= 'AbsortionSpectrum_15591_01.csv'

number_of_particles = 8

size = "L"

constant = 0

# Energy file -------------------------------------------------------
with open (CSV_Energy, newline = '') as file0:
    reader = csv. reader(file0, delimiter = ',')
    next(reader, None)

    energy = list()

    file0.seek(0)
    next(reader, None)

    for fila in reader:
        energy.append(float(fila[0]))


# Particle file -----------------------------------------------------
with open (CSV_Sample, newline = '') as file:
    reader = csv.reader(file, delimiter = ",")
    
    for j in reader:
        length = len(j)

    file.seek(0)
    next(reader, None)# Para saber la longitud de las filas

    particle = 0 #Contador de partículas

    for i in range(1, length, 2):

        particle = particle + 1

        intensity_without_background = list() 
        intensity_with_background = list()
        intensity_of_background =list()

        norm_intensity_without_background = list() 
        norm_intensity_with_background = list()
        norm_intensity_of_background =list()

        for fila in reader:
            intensity_without_background.append((float(fila[i])-float(fila[i+1])+constant))
            intensity_with_background.append(float(fila[i]))
            intensity_of_background.append(float(fila[i+1]))

        for j in range(0,len(intensity_of_background)):
            norm_intensity_without_background.append(float(intensity_without_background[j]/intensity_without_background[0]))
            norm_intensity_with_background.append(float(intensity_with_background[j]/intensity_with_background[0]))
            norm_intensity_of_background.append(float(intensity_of_background[j]/intensity_of_background[0]))

        csv_file_name = "spectrum_particle_{}{}.csv".format(size,particle)
        with open (csv_file_name, 'w', newline = '') as csvfile:
            write_csv = csv.writer(csvfile, delimiter = ' ')
            write_csv.writerow(['energy (eV)','intensity'])
            for j in range(0,len(norm_intensity_of_background)):
                write_csv.writerow([energy[j],norm_intensity_without_background[j]])

        GraphTitle = "Spectrum of the particle {}{} without background signal ".format(size,particle)
        GraphFileTitle = "spectrum_particle_without_background_{}{}".format(size,particle)
        graph(energy,norm_intensity_without_background,GraphTitle,GraphFileTitle)

        GraphTitle = "Spectrum of the particle {}{} with background signal ".format(size,particle)
        GraphFileTitle = "spectrum_particle_with_background_{}{}".format(size,particle)
        graph(energy,norm_intensity_with_background,GraphTitle,GraphFileTitle)

        GraphTitle = "Spectrum of the particle {}{} of the background signal ".format(size,particle)
        GraphFileTitle = "spectrum_particle_of_background_{}{}".format(size,particle)
        graph(energy,norm_intensity_of_background,GraphTitle,GraphFileTitle)

        file.seek(0) #Se va a la primera fila para leer
        next(file) #Se salta el header


#---------------------------------------------------------------------------
