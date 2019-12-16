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