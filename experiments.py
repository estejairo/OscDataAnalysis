############################################################
#
#   En este script se definen las funciones necesarias para
#   analisis de datos muestrados en texto mediante un 
#   osciloscopio.
#  
#   Autor: Jairo Gonzalez
#   Estado: En desarrollo
#
###########################################################


from ROOT import  TFile,TTree
import numpy as np
import time
from tqdm import tqdm #libreria para visualizar porcentaje restante



###########################################################
#
#   select
#   Selecciona los eventos del archivo file_input que
#   posean ruido rms menor a las referencias de ruido al
#   inicio y al medio del eventi (ref_init_noise_rms y 
#   ref_mid_noise_rms respectivamente.)
#
###########################################################
def select(file_input,ref_init_noise_rms,ref_mid_noise_rms):
    print("Starting Selection Algorithm...")
    # Abriendo archivos y cargando arboles
    print("Open file: "+file_input)
    F1 = TFile(file_input,'update')
    data = F1.Get('T1') #arbol con datos de interes
    nentries = data.GetEntries()    #numero total de eventos

    # Creando nuevo arbol
    T2 = TTree("T2","Selected Osc. Signal Events for channels 1, 2 and 3")
    T2 = data.CloneTree(0) #es una copia del original
    T2.SetName("T2") #pero con nuevo nombre
    T2.SetAutoSave(0) #para evitar arboles duplicados

    # lectura de eventos. se seleccionan los que cumplan
    #  las restricciones
    init_noise_rms = 0
    mid_noise_rms = 0
    print("Selecting events...")
    for h in tqdm(range(0,nentries,1)): #incluye estado porcentual
        data.GetEntry(h)

        #Ruido RMS al incio del evento (primeras 625 muestras)
        for i in range(625):
            init_noise_rms += np.power(data.ampCh1[i],2)
        init_noise_rms = np.sqrt(init_noise_rms/i)

        #Ruido RMS al medio del evento (siguientes 500 muestras)
        for j in range(625,1125,1):
            mid_noise_rms += np.power(data.ampCh1[j],2) 
        mid_noise_rms = np.sqrt(mid_noise_rms/i)

        # Se guarda el evento en el nuevo arbol,
        #  solo si cumple condicion
        if ((init_noise_rms < ref_init_noise_rms)and(mid_noise_rms < ref_mid_noise_rms)):
            T2.Fill()
    
    #se sobreescribe el nuevo arbol en el archivo original
    T2.Write("",TFile.kOverwrite) 
    F1.Close()
    print("Done.")
    return



def analyze(file):
    print("Starting Analysis Algorithm...")
    # Abriendo archivos y cargando arboles
    print("Open file: "+file)
    F1 = TFile(file,'update')
    data = F1.Get('T2')
    nentries = data.GetEntries()

    # Creacon de nuevo arbol
    ev = 0
    T3 = TTree("T3","Peak voltage per Event")
    T3.SetAutoSave(0)

    peak1 = np.zeros(nentries,dtype=np.float32)
    peak2 = np.zeros(nentries,dtype=np.float32)
    peak3 = np.zeros(nentries,dtype=np.float32)

    T3.Branch('peak1',peak1,'peak1'+str(nentries)+'/F')
    T3.Branch('peak2',peak2,'peak2'+str(nentries)+'/F')
    T3.Branch('peak3',peak3,'peak3'+str(nentries)+'/F')


    # Creacon de otro nuevo arbol
    T4 = TTree("T4","Average Peak voltage  per Event")
    T4.SetAutoSave(0)

    avgPeak1 = np.zeros(nentries,dtype=np.float32)
    avgPeak2 = np.zeros(nentries,dtype=np.float32)
    avgPeak3 = np.zeros(nentries,dtype=np.float32)

    T4.Branch('avgPeak1',avgPeak1,'avgPeak1'+str(nentries)+'/F')
    T4.Branch('avgPeak2',avgPeak2,'avgPeak2'+str(nentries)+'/F')
    T4.Branch('avgPeak3',avgPeak3,'avgPeak3'+str(nentries)+'/F')



    # Calculo del peak de voltaje (peak absoluto y medio)

    print("Reading Data...")
    peakCh1 = 0
    peakCh2 = 0
    peakCh3 = 0
    avgPeakCh1 = 0
    avgPeakCh2 = 0
    avgPeakCh3 = 0
    for ev in tqdm(range(0,nentries)): 
        data.GetEntry(ev)

        #lectura de muestras
        for j in range(625,1125,1):
            #Almacenamiento de peak y calculo de ruido
            if (data.ampCh1[j]>=peakCh1):
                peakCh1 = data.ampCh1[j]
                samplePeakCh1 = j
            
            if (data.ampCh2[j]>=peakCh2):
                peakCh2 = data.ampCh2[j]
                samplePeakCh2 = j

            if (data.ampCh3[j]>=peakCh3):
                peakCh3 = data.ampCh3[j]
                samplePeakCh3 = j

        peak1[ev] = peakCh1
        peak2[ev] = peakCh2   
        peak3[ev] = peakCh3    
        T3.Fill()

        for k in range(60):  
            avgPeakCh1+=data.ampCh1[samplePeakCh1-30+k]
            avgPeakCh2+=data.ampCh2[samplePeakCh2-30+k]
            avgPeakCh3+=data.ampCh3[samplePeakCh3-30+k]
        avgPeak1[ev] = avgPeakCh1/60.0
        avgPeak2[ev] = avgPeakCh2/60.0
        avgPeak3[ev] = avgPeakCh3/60.0
        T4.Fill()


    #Fin del script
    T3.Write("",TFile.kOverwrite) 
    T4.Write("",TFile.kOverwrite) 
    F1.Close()
    return