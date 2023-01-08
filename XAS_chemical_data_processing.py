# Marta Xiulan Aribó Herrera
# Autmun 2022/2023
# TFG
# Program to compare and plot the weighted sum of the standard spectra and those of the samples
#---------------------------------------------------------------------------
#                               LIBRARIES & FUNCTIONS
#---------------------------------------------------------------------------

import csv
import numpy as np
import matplotlib.pyplot as plt

import scienceplots

plt.style.use('science')
def ReadingFiles(fileCSVStandard,fileCSVSample,NiStandard,NiOStandard,Energy_sample,Energy_standard,IntensitySample):

    with open (fileCSVStandard, newline = '') as file0: #file con los estandares de Ni y NiO
        reader = csv.reader(file0, delimiter = ' ')
        file0.seek(0)
        next(reader, None)
        for fila in reader:
            NiStandard.append(float(fila[1])*2)
            NiOStandard.append(float(fila[2])*2)
            Energy_standard.append(float(fila[0]))

    with open (fileCSVSample, newline = '') as file1: #file muestra
        reader = csv.reader(file1, delimiter = ' ')
        file1.seek(0)
        next(reader, None)
        for fila in reader:
            Energy_sample.append(float(fila[0]))
            IntensitySample.append(float(fila[1]))
        
def weight_function(weight_Ni,weight_NiO,Energy,NiStandard,NiOStandard,WeightedIntensity):
    for i in range(0,len(Energy)):
        WeightedIntensity.append((weight_Ni/100*NiStandard[i]+weight_NiO/100*NiOStandard[i]))

def Graph(x,y1,y2,GraphTitle, GraphFileTitle):
    

    plt.plot(x,y1,'b',label = "Weighted Intensity",linewidth=1)
    plt.plot(x,y2,'g',label = "Sample Intensity", linewidth=1)


    plt.title(GraphTitle)
    plt.xlabel('Energía(eV)')
    plt.ylabel("Intensidad")
    plt.legend()
     
    plt.savefig(GraphFileTitle+".jpg",dpi=300)
    #plt.show()
    plt.close()

def Graph_energy_shifted(x1,y1,x2,y2,GraphTitle,GraphFileTitle,):
        

    index_y1 = y1.index(max(y1)) #standard
    index_y2 = y2.index(max(y2)) #sample
    index_y3 = y1.index(max(y1[100:len(y1)])) 
    index_y4 = y2.index(max(y2[100:len(y2)]))
    index_y5 = y1.index(max(y1[153:len(y1)])) 
    index_y6 = y2.index(max(y2[163:len(y2)]))


    energy_intensity_max_1 = x1[index_y1]
    energy_intensity_max_2 = x2[index_y2]
    energy_shift = energy_intensity_max_1-energy_intensity_max_2

    plt.plot(np.array(x1),np.array(y1), linewidth=1, label= 'NiO standard')
    plt.plot(np.array(x2)+energy_shift,np.array(y2), linewidth=1, label = 'Sample')

    e1 = np.linspace(energy_intensity_max_1,energy_intensity_max_1,205)
    e2 = np.linspace(energy_intensity_max_2+energy_shift,energy_intensity_max_2+energy_shift,205)
    e3 = np.linspace(x2[index_y3],x2[index_y3],205)
    e4 = np.linspace(x1[index_y4],x1[index_y4],205)
    e5 = np.linspace(x2[index_y5],x2[index_y5],205)
    e6 = np.linspace(x1[index_y6],x1[index_y6],205)

    plt.plot(e1,y1, linewidth = 1, label = f"Maximum A standard: ({max(y1), energy_intensity_max_1})")
    plt.plot(e2,y2, linewidth = 1, label = f"Maximum A' sample: ({max(y2), energy_intensity_max_2})")
    plt.plot(e3,y2, linewidth = 1, label = f"Maximum C standard: ({max(y1[100:len(y1)]),x1[index_y3]})")
    plt.plot(e4+energy_shift,y1, linewidth = 1, label = f"Maximum C' sample: ({max(y2[100:len(y2)]), x2[index_y4]})")
    plt.plot(e5,y1, linewidth = 1, label = f"Maximum D standard: ({max(y1[153:len(y1)]), x1[index_y5]})")
    plt.plot(e6+energy_shift,y1, linewidth = 1, label = f"Maximum D' sample: ({max(y2[163:len(y2)]), x2[index_y6]})")


    AC_ =max(y1)/max(y1[100:len(y1)])
    AC= max(y2)/max(y2[100:len(y2)])
    CD_=max(y1[100:len(y1)])/max(y1[156:len(y1)])
    CD=max(y2[100:len(y2)])/max(y2[156:len(y2)])
    A_C= energy_intensity_max_2-x2[index_y4]    
    print(A_C)
    plt.title(GraphTitle+ "with a shift of {} eV and A/C ={}, A'/C'={}, C/D={},C'/D'={} a-c={}".format(energy_shift,AC_,AC,CD_,CD,A_C))
    plt.xlabel('Energy(eV)')
    plt.ylabel("Intensity")
    plt.legend()
     
    plt.savefig(GraphFileTitle +".jpg",dpi=300)
    plt.show()
    plt.close()

#---------------------------------------------------------------------------
#                         Body
#---------------------------------------------------------------------------

size = "L"
number_of_particles=10
for particle in range(1,number_of_particles+1):

    for weight_Ni in range(88,101): #percentage of Ni 
    #    for particle in range(1,number_of_particles+1,1):
            NiStandard = list()
            NiOStandard = list()
            Energy_standard = list()
            Energy_sample = list()

            IntensitySample =list()
            WeightedIntensity = list()

            fileStandard= "./normalized_heaviside_interpol_NiO_Ni.csv" #CSV file of the standards
            fileCSVSample = "./normalized_heaviside_spectra_particles_L/normalized_heaviside_spectrum_particle_{}{}.csv".format(size,particle) #CSV file of the particle

            ReadingFiles(fileStandard,fileCSVSample,NiStandard,NiOStandard,Energy_sample,Energy_standard,IntensitySample)

            weight_NiO = 100 - weight_Ni

            weight_function(weight_Ni,weight_NiO,Energy_standard,NiStandard,NiOStandard,WeightedIntensity)

            GraphTitle = "Particle {}{} with {} $\%$Ni + {} $\%$NiO ".format(size,particle,weight_Ni,weight_NiO)
            GraphFileTitle = "distance_shifted_particle_{}{}_{}%Ni_{}%NiO".format(size,particle,weight_Ni,weight_NiO)
            Graph_energy_shifted(Energy_standard,WeightedIntensity,Energy_sample,IntensitySample,GraphTitle,GraphFileTitle)