# Marta Xiulan Aribó Herrera
# Autumn 2022/2023
# TFG
# Program to normalize and plot XLMD
#---------------------------------------------------------------------------
#                               LIBRARIES & FUNCTIONS
#---------------------------------------------------------------------------

import csv
import matplotlib.pyplot as plt
import numpy as np
import scienceplots

plt.style.use('science')

def Graph(x,y,GraphTitle,GraphFileTitle):
    plt.plot(x,y,linewidth=1)

    plt.title(GraphTitle)
    plt.xlabel('Photon Energy(eV)')
    plt.ylabel("Normalized Absorption (U.A)")
     
    plt.savefig(GraphFileTitle+".jpg",dpi=300)
    plt.close()


def ReadingFiles_And_Normalization(CSVFile,energy,intensity,NormalizedIntensity):
    with open (CSVFile, newline = '') as file:
        reader = csv.reader(file, delimiter = ' ')
        file.seek(0)
        next(reader, None)
        for fila in reader:
            energy.append(float(fila[0]))
            intensity.append(float(fila[1]))

    index= 185
    print(energy[index])
    
    for i in range (0, len(intensity)):
        NormalizedIntensity.append((intensity[i]-min(intensity))/(intensity[index]-min(intensity)))


def WritingFiles(energy,NormalizedIntensity,CSVTitle):
    with open (CSVTitle, 'w', newline = '') as csvfile:
            write_csv = csv.writer(csvfile, delimiter = ' ')
            write_csv.writerow(['Energy',"Normalized Heaviside Sample Signal"])
            for j in range(0,len(NormalizedIntensity),1):
                write_csv.writerow([energy[j],NormalizedIntensity[j]])

#---------------------------------------------------------------------------
#                         Body
#---------------------------------------------------------------------------

number_of_particles = 48
size = "S"

for particle in range(1,number_of_particles+1,1):

#reading and normalization of horizontal polarised light
    CSVFile_LH = "./spectra_particles_2A_5_LH_S/spectrum_particle_{}{}.csv".format(size,particle) 
    energy_LH = list()
    intensity_LH = list() 
    NormalizedIntensity_LH = list()
    ReadingFiles_And_Normalization(CSVFile_LH,energy_LH,intensity_LH,NormalizedIntensity_LH)

#reading and normalization of vertical polarised light
    CSVFile_LV = "./spectra_particles_2A_6_LV_S/spectrum_particle_{}{}.csv".format(size,particle)
    energy_LV = list()
    intensity_LV = list()
    NormalizedIntensity_LV = list()
    ReadingFiles_And_Normalization(CSVFile_LV,energy_LV,intensity_LV,NormalizedIntensity_LV)

#saving normalized data of horizontal polarised light
    LH = "LH"
    GraphTitle = "Normalized heaviside spectrum of the particle {}{} {}".format(size,particle,LH)
    GraphFileTitle = "normalized_heaviside_spectrum_particle_{}{}_{}".format(size,particle,LH)
    CSVTitle =  "normalized_heaviside_spectrum_particle_{}{}_{}.csv".format(size,particle,LH)
    Graph(energy_LH,NormalizedIntensity_LH,GraphTitle,GraphFileTitle)
    WritingFiles(energy_LH,NormalizedIntensity_LH,CSVTitle)

#saving normalized data of vertical polarised light
    LV = "LV"
    GraphTitle = "Normalized heaviside spectrum of the particle {}{} {}".format(size,particle,LV)
    GraphFileTitle = "normalized_heaviside_spectrum_particle_{}{}_{}".format(size,particle,LV)
    CSVTitle =  "normalized_heaviside_spectrum_particle_{}{}_{}.csv".format(size,particle,LV)
    Graph(energy_LV,NormalizedIntensity_LV,GraphTitle,GraphFileTitle)
    WritingFiles(energy_LV,NormalizedIntensity_LV,CSVTitle)

#XLMD computed via difference
    DifferenceIntensity = list()

    for j in range(0,len(NormalizedIntensity_LH)):
        DifferenceIntensity.append(+NormalizedIntensity_LH[j]-NormalizedIntensity_LV[j])

#XLMD computed via division
    QuotientIntensity = list()
    for j in range (0,len(NormalizedIntensity_LH)):
        QuotientIntensity.append((intensity_LV[j])/(intensity_LH[j]))

#Generating graphs
    VH = "VH"
    GraphTitle = "XMLD spectra difference of the particle {}{}".format(size,particle)
    GraphFileTitle = "XMLD_spectra_difference_particle_{}{}".format(size,particle)
    Graph(energy_LH,DifferenceIntensity,GraphTitle,GraphFileTitle)

    VH = "VH"
    GraphTitle = "XMLD spectra quotient of the particle {}{}".format(size,particle)
    GraphFileTitle = "XMLD_spectra_quotient_particle_{}{}".format(size,particle)
    Graph(energy_LV,QuotientIntensity,GraphTitle,GraphFileTitle)



