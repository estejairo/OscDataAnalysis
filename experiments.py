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


from ROOT import  TFile,TTree,TH1F,TH2F,TGraph,TMultiGraph,TCanvas,TPaveStats,gStyle
import numpy as np
import time
from tqdm import tqdm #libreria para visualizar porcentaje restante



###########################################################
#
#   select
#   Selecciona los eventos del archivo file_input que
#   posean ruido rms menor a las referencias de ruido al
#   inicio y al medio del eventi (ref_init_noise_rms y 
#   ref_final_noise_rms respectivamente.)
#
###########################################################
def select(file_input,ref_init_noise_rms,ref_final_noise_rms):
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
    final_noise_rms = 0
    print("Selecting events...")
    for h in tqdm(range(0,nentries,1)): #incluye estado porcentual
        data.GetEntry(h)

        #Ruido RMS al incio del evento (primeras 625 muestras)
        for i in range(625):
            init_noise_rms += np.power(data.ampCh1[i],2)
        init_noise_rms = np.sqrt(init_noise_rms/i)

        #Ruido RMS al medio del evento (siguientes 500 muestras)
        for j in range(1125,2502,1):
            final_noise_rms += np.power(data.ampCh1[j],2) 
        final_noise_rms = np.sqrt(final_noise_rms/i)

        # Se guarda el evento en el nuevo arbol,
        #  solo si cumple condicion
        if ((init_noise_rms < ref_init_noise_rms)and(final_noise_rms < ref_final_noise_rms)):
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

    peak1 = np.zeros(1,dtype=np.float32)
    peak2 = np.zeros(1,dtype=np.float32)
    peak3 = np.zeros(1,dtype=np.float32)

    T3.Branch('event',ev,'event/I')
    T3.Branch('peak1',peak1,'peak1[1]/F')
    T3.Branch('peak2',peak2,'peak2[1]/F')
    T3.Branch('peak3',peak3,'peak3[1]/F')


    # Creacon de otro nuevo arbol
    T4 = TTree("T4","Average Peak voltage  per Event")
    T4.SetAutoSave(0)

    avgPeak1 = np.zeros(1,dtype=np.float32)
    avgPeak2 = np.zeros(1,dtype=np.float32)
    avgPeak3 = np.zeros(1,dtype=np.float32)

    T4.Branch('event',ev,'event/I')
    T4.Branch('avgPeak1',avgPeak1,'avgPeak1[1]/F')
    T4.Branch('avgPeak2',avgPeak2,'avgPeak2[1]/F')
    T4.Branch('avgPeak3',avgPeak3,'avgPeak3[1]/F')



    # Calculo del peak de voltaje (peak absoluto y medio)

    print("Reading Data...")
    for ev in tqdm(range(0,nentries)): 
        data.GetEntry(ev)

        peakCh1 = 0
        peakCh2 = 0
        peakCh3 = 0
        avgPeakCh1 = 0
        avgPeakCh2 = 0
        avgPeakCh3 = 0

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

        peak1[0] = np.float32(peakCh1)
        peak2[0] = np.float32(peakCh2)  
        peak3[0] = np.float32(peakCh3)   
        T3.Fill()

        for k in range(60):  
            avgPeakCh1+=data.ampCh1[samplePeakCh1-30+k]
            avgPeakCh2+=data.ampCh2[samplePeakCh2-30+k]
            avgPeakCh3+=data.ampCh3[samplePeakCh3-30+k]
        avgPeak1[0] = np.float32(avgPeakCh1/60.0)
        avgPeak2[0] = np.float32(avgPeakCh2/60.0)
        avgPeak3[0] = np.float32(avgPeakCh3/60.0)
        T4.Fill()


    #Fin del script
    T3.Write("",TFile.kOverwrite) 
    T4.Write("",TFile.kOverwrite) 
    F1.Close()
    return

def graphAnalysis(file_input,experiment,keyword):

    ##Graphs

    F1 = TFile(file_input,'read')
    selectedData = F1.Get('T2')
    averageData = F1.Get('T4')

    #Creacion de canvas
    c1 = TCanvas('c1','Mode: '+experiment+'- Side: '+keyword,1500,500)
    c1.Divide(3,1)
    c3 = TCanvas('c3','Selected Events',1500,500)
    c3.Divide(3,1)
    c4 = TCanvas('c4','Position Vs Amplitude')
    c5 = TCanvas('c5','Position Vs Amplitude Distribution')

    # Creando histogramas
    leftHistogram   = TH1F('leftHistogram ','Left Channel Histogram; Average Peak Amplitude [V]',96,0,0.06)
    centerHistogram = TH1F('centerHistogram','Center Channel Histogram; Average Peak Amplitude [V]',96,0,0.06)
    rightHistogram  = TH1F('rightHistogram','Right Channel Histogram; Average Peak Amplitude [V]',96,0,0.06)
    oneEvent_PosAmp = TH1F('oneEvent_PosAmp','Amplitude Vs Strip Coordinate; Amplitude [V]; Strip Coordinate #',8,0,8.5)
    amplitudeDistr  = TH2F('amplitudeDistr','Position Vs Amplitude Distribution; Amplitude [V]; Strip Coordinate #',8,0,8.5,96,0,0.06)
    selectedEventsCh1 = TMultiGraph('selectedEventsCh1','Ch1 Amplitude Vs Time - Selected Pulses; Time [s]; Amplitude [V]')
    selectedEventsCh2 = TMultiGraph('selectedEventsCh2','Ch2 Amplitude Vs Time - Selected Pulses; Time [s]; Amplitude [V]')
    selectedEventsCh3 = TMultiGraph('selectedEventsCh3','Ch3 Amplitude Vs Time - Selected Pulses; Time [s]; Amplitude [V]')
    nentries=selectedData.GetEntries()


    for i in tqdm(range(0, nentries)):
        averageData.GetEntry(i)
        selectedData.GetEntry(i)
        leftHistogram.Fill(averageData.avgPeak1)
        centerHistogram.Fill(averageData.avgPeak2)
        rightHistogram.Fill(averageData.avgPeak3)
        amplitudeDistr.Fill(3,averageData.avgPeak1)
        amplitudeDistr.Fill(4,averageData.avgPeak2)
        amplitudeDistr.Fill(5,averageData.avgPeak3)
        if ((i%1)==0):
            graph1 = TGraph(2502,selectedData.time,selectedData.ampCh1)
            graph2 = TGraph(2502,selectedData.time,selectedData.ampCh2)
            graph3 = TGraph(2502,selectedData.time,selectedData.ampCh3)
            selectedEventsCh1.Add(graph1)
            selectedEventsCh2.Add(graph2)
            selectedEventsCh3.Add(graph3)
            del graph1
            del graph2
            del graph3
        
        

    oneEvent_PosAmp.SetBinContent(3,int(averageData.avgPeak1*1000))
    oneEvent_PosAmp.SetBinContent(4,int(averageData.avgPeak2*1000))
    oneEvent_PosAmp.SetBinContent(5,int(averageData.avgPeak3*1000))

    #propiedades de histograma        
    gStyle.SetOptFit(0111)


    #Ajuste y dibujo de histogramas
    c1.cd(1)
    #leftHistogram.Fit('gaus','','',0.07995,0.15005)
    leftHistogram.Draw()

    c1.cd(2)
    #centerHistogram.Fit('gaus','','',0.07995,0.15005)
    centerHistogram.Draw()

    c1.cd(3)
    #rightHistogram.Fit('gaus','','',0.07995,0.15005)
    rightHistogram.Draw()


    c3.cd(1)
    selectedEventsCh1.Draw('AL')
    c3.cd(2)
    selectedEventsCh2.Draw('AL')
    c3.cd(3)
    selectedEventsCh3.Draw('AL')

    c4.cd()
    oneEvent_PosAmp.Fit('gaus','','',1,7)
    oneEvent_PosAmp.Draw()


    c5.cd()
    amplitudeDistr.Draw('colz')

    c1.Update()
    c3.Update()
    c4.Update()
    c5.Update()

    print("Saving graphs into PDF...")
    c1.SaveAs('../../graphs/test/'+experiment+'-'+keyword+' side.pdf')
    c3.SaveAs('../../graphs/test/'+experiment+'-'+keyword+' - Selected Events.pdf')
    c4.SaveAs('../../graphs/test/oneEvent_PosAmp.pdf')
    c5.SaveAs('../../graphs/test/amplitudeDistr.pdf')
    return