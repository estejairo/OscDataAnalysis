################################################################
#
#   Scrip para transformar de formato ASCII a arbol de datos,
#   usado en archivos con datos de adquisicion provenientes
#   del osciloscopio.
#
#   Autor: Hernan Oyanadel
#   Editado por: Jairo Gonzalez
#   Estado: Terminado
#
################################################################

from ROOT import  TFile,TTree
import numpy as np
import Tkinter as tk
import Tkconstants, tkFileDialog, tkSimpleDialog
import time
from tqdm import tqdm #libreria para visualizar porcentaje restante

ROOT = tk.Tk()
ROOT.withdraw()


#### Globals

#Folder
folder = "../data/free/right"
# folder = tkFileDialog.askdirectory(initialdir = "..")
print("Folder: "+folder+"\n")

#File
keyword = "rigth"
# keyword = tkSimpleDialog.askstring(title="Globals",
#                                   prompt="File Keyword:")
print("Keyword: "+keyword+"\n")

#Events
events = str(2000)
print("Total Events: "+events+"\n")

#Data points
samples = str(2503)
print("Samples per event: "+samples+"\n")


print("Creating ROOT TTree...\n")
ev = 0
F1 = TFile('../data/na22-free-'+keyword+'.root','recreate')
T1 = TTree("T1","Osc. Signal Events for channels 1, 2 and 3")
T1.SetAutoSave(0)

t = np.zeros(int(samples),dtype=np.float32)
aCh1 = np.zeros(int(samples),dtype=np.float32)
aCh2 = np.zeros(int(samples),dtype=np.float32)
aCh3 = np.zeros(int(samples),dtype=np.float32)

T1.Branch('event',ev,'event/I')
T1.Branch('time',t,'time['+samples+']/F')
T1.Branch('ampCh1',aCh1,'ampCh1['+samples+']/F')
T1.Branch('ampCh2',aCh2,'ampCh2['+samples+']/F')
T1.Branch('ampCh3',aCh3,'ampCh3['+samples+']/F')

print("Reading Data...\n")
for ev in tqdm(range(0,int(events))): 
    c1 = open(folder+'/C1 na22-'+keyword+str(ev).zfill(5)+'.txt')
    c2 = open(folder+'/C2 na22-'+keyword+str(ev).zfill(5)+'.txt')
    c3 = open(folder+'/C3 na22-'+keyword+str(ev).zfill(5)+'.txt')

    i = 0
    j=-1
    for l1,l2,l3 in zip(c1,c2,c3):
        if i<5:
            i+=1
            continue
        else:
            i+=1
            j+=1
        t[j] = np.float32(float(l1.strip().split('\t')[0]))
        aCh1[j] = np.float32(float(l1.strip().split('\t')[1]))
        aCh2[j] = np.float32(float(l2.strip().split('\t')[1]))
        aCh3[j] = np.float32(float(l3.strip().split('\t')[1]))

    T1.Fill()
    c1.close()
    c2.close()
    c3.close()

 
T1.Write("",TFile.kOverwrite)
F1.Close()
z = raw_input('Done.')
