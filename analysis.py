############################################################
#
#   En este script se generan histogramas para analizar
#   la relacion de amplitudes de pulsos con la posicion de
#   los canales medidos respecto a la fuente radioactiva.
#  
#   Autor: Jairo Gonzalez
#   Estado: En desarrollo
#
###########################################################


from ROOT import  TFile,TTree,TH1F,TH2F,TCanvas,TPaveStats,gStyle
import numpy as np
import Tkinter as tk
import Tkconstants, tkFileDialog, tkSimpleDialog
import time
from tqdm import tqdm #libreria para visualizar porcentaje restante

ROOT = tk.Tk()
ROOT.withdraw()


file = "../data/na22-free-rigth.root"
experiment="free"
keyword = "right"
samples = "2503"
# file = tkFileDialog.askopenfilename(initialdir = "../data",
#                                     title = "Select file",
#                                     filetypes = (("root files","*.root"),
#                                     ("all files","*.*")))
# experiment = tkSimpleDialog.askstring(title="Globals",
#                                   prompt="Experiment mode:")
# keyword = tkSimpleDialog.askstring(title="Globals",
#                                   prompt="File Keyword:")



# Abriendo archivos y cargando arboles
F1 = TFile(file,'update')
data = F1.Get('T2')
nentries = data.GetEntries()

# Creacon de nuevo arbol
ev = 0
T3 = TTree("T3","Peak and Average Peak per Event")
T3.SetAutoSave(0)

peak = np.zeros(int(samples),dtype=np.float32)
avgPeak = np.zeros(int(samples),dtype=np.float32)

T3.Branch('event',ev,'event/I')
T3.Branch('peak',peak,'peak['+samples+']/F')
T3.Branch('avgPeak',avgPeak,'avgPeak['+samples+']/F')





# Calculo del peak de voltaje (peak absoluto y medio)

#valores iniciales
peakCh1 = 0
peakCh2 = 0
peakCh3 = 0
AvgPeakCh1 = 0
AvgPeakCh2 = 0
AvgPeakCh3 = 0

#lectura de eventos
l=0
for h in tqdm(range(0,nentries,1)):
    data.GetEntry(h)

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

    
    for k in range(60):  
        AvgPeakCh1+=data.ampCh1[samplePeakCh1-30+k]
        AvgPeakCh2+=data.ampCh2[samplePeakCh2-30+k]
        AvgPeakCh3+=data.ampCh3[samplePeakCh3-30+k]
    AvgPeakCh1 = AvgPeakCh1/60
    AvgPeakCh2 = AvgPeakCh2/60
    AvgPeakCh3 = AvgPeakCh3/60


#Fin del script
F1.Close()


z = raw_input('Press "ENTER" to exit.')
