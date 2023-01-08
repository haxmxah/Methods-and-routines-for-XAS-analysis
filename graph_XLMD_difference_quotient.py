
# Marta Xiulan Aribó Herrera
# Autmun 2022/2023
# TFG
# Another rogram to plot difference intensitites as a function of energy from Image J specific csv files and
# overlap spectra.

#---------------------------------------------------------------------------
#                               LIBRARIES & FUNCTIONS
#---------------------------------------------------------------------------
import csv
import matplotlib.pyplot as plt
import numpy as np
import scienceplots
import matplotlib.transforms as mtransforms

plt.style.use('science')

def Graph(x,y,GraphTitle,GraphFileTitle):
    plt.plot(x,y,linewidth=1)

    plt.title(GraphTitle)
    plt.xlabel('Energy(eV)')
    plt.ylabel("Intensity")
     
    plt.savefig(GraphFileTitle+".jpg",dpi=300)
    plt.close()


def ReadingFiles_And_Normalization(CSVFile,energy,intensity,NormalizedIntensity,index):
    with open (CSVFile, newline = '') as file:
        reader = csv.reader(file, delimiter = ' ')
        file.seek(0)
        next(reader, None)
        for fila in reader:
            energy.append(float(fila[0]))
            intensity.append(float(fila[1]))

    intensity_norm=intensity[index]
    print(energy[index])
    for i in range (0, len(intensity)):

        NormalizedIntensity.append((intensity[i]-min(intensity))/(intensity_norm-min(intensity)))


def WritingFiles(energy,NormalizedIntensity,CSVTitle):
    with open (CSVTitle, 'w', newline = '') as csvfile:
            write_csv = csv.writer(csvfile, delimiter = ' ')
            write_csv.writerow(['Energy',"Normalized Heaviside Sample Signal"])
            for j in range(0,len(NormalizedIntensity),1):
                write_csv.writerow([energy[j],NormalizedIntensity[j]])

#---------------------------------------------------------------------------
#                         Body
#---------------------------------------------------------------------------

size = "S"
index= 200
particle = 48

#reading and normalization of horizontal polarised light

CSVFile_LH = "./spectra_particles_2A_5_LH_{}/spectrum_particle_{}{}.csv".format(size,size,particle)
energy_LH = list()
intensity_LH = list() 
NormalizedIntensity_LH = list()
ReadingFiles_And_Normalization(CSVFile_LH,energy_LH,intensity_LH,NormalizedIntensity_LH,index)

#reading and normalization of vertical polarised light

CSVFile_LV = "./spectra_particles_2A_6_LV_{}/spectrum_particle_{}{}.csv".format(size,size,particle)
energy_LV = list()
intensity_LV = list()
NormalizedIntensity_LV = list()
ReadingFiles_And_Normalization(CSVFile_LV,energy_LV,intensity_LV,NormalizedIntensity_LV,index)

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
    DifferenceIntensity.append(-NormalizedIntensity_LH[j]+NormalizedIntensity_LV[j])

fig = plt.figure()

# to change size of subplot's
# set height of each subplot as 8
fig.set_figheight(5)

# set width of each subplot as 8
fig.set_figwidth(7)

#Generating graphs

spec = plt.GridSpec(ncols=2, nrows=2,
                        width_ratios=[1,1], wspace=0.25,
                        hspace=0.2, height_ratios=[3, 1])

ax0 = fig.add_subplot(spec[0])
ax0.plot(np.array(energy_LV),np.array(NormalizedIntensity_LV ),'-',color="darkorange",linewidth=1, label= f'{index}')
ax0.plot(np.array(energy_LV),np.array(NormalizedIntensity_LH ),'-',color="blueviolet",linewidth=1,label= f'{index}')

ax1 = fig.add_subplot(spec[2],sharex=ax0)
ax1.plot(np.array(energy_LV),np.array(DifferenceIntensity),'-',color="black",linewidth=0.5,label= f'{index,energy_LH[index]}')
plt.legend()
plt.savefig((":)_XLMD_particle_{}{}.jpg").format(str(size),str(particle)),dpi=800)

plt.close()

#XLMD computed via division and generating graphs

LH= np.array(NormalizedIntensity_LH)+1
LV= np.array(NormalizedIntensity_LV)+1

VH = "VH"
GraphTitle = "XMLD spectra quotient of the particle {}{}".format(size,particle)
GraphFileTitle = "XMLD_spectra_quotient_particle_{}{}".format(size,particle)
Graph(energy_LV,LV/LH,GraphTitle,GraphFileTitle)
    
