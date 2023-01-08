# Marta Xiulan Aribó Herrera
# Autmun 2022/2023
# TFG
# Program to plot intensities as a function of energy from Image J specific csv files.

#---------------------------------------------------------------------------
#                               LIBRARIES & FUNCTIONS
#-------------------------
import csv
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit,least_squares
import csv

plt.rcParams.update({
        "text.usetex": True,
        "font.family": "Serif"
    })

def XMLD_graph(x,y,GraphTitle,GraphFileTitle):
    
    plt.figure(figsize=(15,10))
    plt.plot(x,y,linewidth=1, marker = 'o')

    plt.title(GraphTitle)
    plt.xlabel('Angle(º)')
    plt.ylabel("XMLD")

    #plt.xticks([885,865,875,885])
     
    plt.savefig(GraphFileTitle + ".jpg",dpi=300)
    plt.close()
    return

def XLMD_fit_plot(x,y,y_fitted,GraphTitle,GraphFileTitle):

    plt.figure(figsize=(15,10))
    plt.plot(x,y,linewidth=1, marker = 'o', markersize=4, label='data')
    plt.plot(x, y_fitted, 'r-', label='modelo fiteado')

    plt.title(GraphTitle)
    plt.xlabel("Angle(º)")
    plt.ylabel("XMLD")

    plt.legend(loc='best')

    plt.savefig(GraphFileTitle + ".jpg",dpi=300)
    plt.close()
    return

def function(p,x):
    return p[0]+p[1]*np.cos(x)**2

def remainder(p, x, y):
    # p is a vector with the parameters
    # x is a vector x
    # y is a vector y
    param_list =[]
    y_modelo = function(p, x)
    plt.clf()
    plt.plot(x,y,'o',x,y_modelo,'r-')
    plt.pause(0.05)
    param_list.append(p)
    return y_modelo - y

def calculate_of_cov(res,y):
    U, S, V = np.linalg.svd(res.jac, full_matrices=False)
    threshold = np.finfo(float).eps * max(res.jac.shape) * S[0]
    S = S[S > threshold]
    V = V[:S.size]
    pcov = np.dot(V.T / S**2, V)

    s_sq = 2 * res.cost / (y.size - res.x.size)
    pcov = pcov * s_sq
    return pcov

def parameters_uncertainties(pcov,res):
    pstd = np.sqrt(np.diag(pcov))
    print('Parámetros hallados (con incertezas):')
    for i,param in enumerate(res.x):
        print('parametro[{:d}]: {:5.3f} ± {:5.3f}'.format(i,param,pstd[i]/2))
    return

#---------------------------------------------------------------------------
#                         Body
#---------------------------------------------------------------------------


angles =[0,15,30,45,60,75,90]
CSVFile = 'results_particles.csv'
number_of_particles = 36
particle = 0


with open (CSVFile, newline='') as file:

    reader = csv. reader(file, delimiter = ',')

    for i in range (1,number_of_particles*2,2):
        
        file.seek(0)
        next(reader,None)

        particle = particle + 1

        intensity_without_background = list() 
        intensity_with_background = list()
        intensity_of_background =list()

        XMLD= list()
        I_i = list()

        for fila in reader:
            print('intensity',fila[i],'background',fila[i+1])
            print(len(fila))
            intensity_with_background.append(float(fila[i]))
            intensity_of_background.append(float(fila[i+1]))
            intensity_without_background.append(float(fila[i])/float(fila[i+1]))

        for angle in range(0,7):
            XMLD.append((intensity_without_background[angle]-intensity_without_background[angle+7])/(intensity_without_background[angle]+intensity_without_background[angle+7]))

        CSVFileTitle = "XLMD_particle_difference_"+str(particle)+".csv"

        with open(CSVFileTitle, 'w', newline='') as filewrite:
            write = csv.writer(filewrite, delimiter=' ')
            write.writerow(['Angle(º)', 'XLMD'])
            for j in range(0,len(XMLD)):
                write.writerow([angles[j],XMLD[j]])

        GraphFileTitle = "graph_XLMD_difference_particle_with_fit_"+str(particle)
        GraphTitle = "XLMD as a function of the angle for the particle "+str(particle)
        XMLD_graph(angles,XMLD,GraphTitle,GraphFileTitle)
        
        p = [1,1]        
        res = least_squares(remainder,p,args = (np.array(angles)*np.pi/180,np.array(XMLD)), verbose = 1)
        
        print('founded parameters')
        print(res.x)

        pcov = calculate_of_cov(res,np.array(XMLD))

        # De la matriz de covarianza podemos obtener los valores de desviación estándar
        # de los parametros hallados
        pstd = np.sqrt(np.diag(pcov))      

        print('Parámetros hallados (con incertezas):')

        for k,param in enumerate(res.x):
            print('parametro[{:d}]: {:5.3f} ± {:5.3f}'.format(k,param,pstd[k]/2))
            I_i.append(param)
            I_i.append(pstd[k]/2)

        XMLD_fitted = function(res.x,np.array(angles)*np.pi/180 )

        GraphTitle_fit = 'XMLD with fit of the particle {} with $I= I_0 + I_1\cdot \cos \phi$ where $I_0 =${:5.3f} $\pm$ {:5.3f} $I_1 =${:5.3f} $\pm${:5.3f}'.format(particle,I_i[0],I_i[1],I_i[2],I_i[3])
        
        XLMD_fit_plot(angles,XMLD,XMLD_fitted,GraphTitle_fit,GraphFileTitle)