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

from ROOT import TFile,TH1F,TH2F,TCanvas,TPaveStats,gStyle
from experiments import select, analyze

import time
from tqdm import tqdm #libreria para visualizar porcentaje restante

EVENTOS = 2000
MUESTRAS = 2502
ref_init_noise_rms = 0.002
ref_mid_noise_rms = 0.03


file_input = "../../data/na22-free-rigth.root"
experiment="free"
keyword = "right"
#file_output = "../../data/na22-free-rigth-selected.root"

# file = tkFileDialog.askopenfilename(initialdir = "../data",
#                                     title = "Select file",
#                                     filetypes = (("root files","*.root"),
#                                     ("all files","*.*")))

## Data Selection
select(file_input,ref_init_noise_rms,ref_mid_noise_rms)

## Average Peak voltage per event
analyze(file_input)


##Graphs

F1 = TFile(file_input,'read')
selectedData = F1.Get('T2')
peakData = F1.Get('T3')
averageData = F1.Get('T4')

#Creacion de canvas
c1 = TCanvas('c1','Mode: '+experiment+'- Side: '+keyword)
c1.Divide(1,3)
c2 = TCanvas('c2','Mode: '+experiment+'- Side: '+keyword+' - All Channels')
c3 = TCanvas('c3','Selected Events')
#c3.Divide(1,3)
c4 = TCanvas('c4','Position Vs Amplitude')
c5 = TCanvas('c5','Position Vs Amplitude Distribution')

# Creando histogramas
leftHistogram   = TH1F('leftHistogram ','Left Channel Histogram',96,0,0.06)
centerHistogram = TH1F('centerHistogram','Center Channel Histogram',96,0,0.06)
rightHistogram  = TH1F('rightHistogram','Right Channel Histogram',96,0,0.06)
fullHistogram   = TH1F('fullHistogram','All Channels',96,0,0.06)
oneEvent_PosAmp = TH1F('oneEvent_PosAmp','Position Vs Amplitude',8,0,8.5)
amplitudeDistr  = TH2F('amplitudeDistr','Position Vs Amplitude Distribution',8,0,8.5,96,0,0.06)

nentries=selectedData.GetEntries()

for i in tqdm(range(0, nentries)):
    averageData.GetEntry(i)
    leftHistogram.Fill(averageData.avgPeak1)
    centerHistogram.Fill(averageData.avgPeak2)
    rightHistogram.Fill(averageData.avgPeak3)
    fullHistogram.Fill(averageData.avgPeak3)
    fullHistogram.Fill(averageData.avgPeak3)
    fullHistogram.Fill(averageData.avgPeak3)
    amplitudeDistr.Fill(3,averageData.avgPeak1)
    amplitudeDistr.Fill(4,averageData.avgPeak2)
    amplitudeDistr.Fill(5,averageData.avgPeak3)

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

c2.cd()
fullHistogram.Draw()

c4.cd()
oneEvent_PosAmp.Fit('gaus','','',1,7)
oneEvent_PosAmp.Draw()


c5.cd()
amplitudeDistr.Draw('colz')

c1.Update()
c2.Update()
c3.Update()
c4.Update()
c5.Update()

c1.SaveAs('../../graphs/test/'+experiment+'-'+keyword+' side.pdf')
c2.SaveAs('../../graphs/test/'+experiment+'-'+keyword+' - All Channels.pdf')
c3.SaveAs('../../graphs/test/'+experiment+'-'+keyword+' - Selected Events.pdf')
c4.SaveAs('../../graphs/test/oneEvent_PosAmp.pdf')
c5.SaveAs('../../graphs/test/amplitudeDistr.pdf')

z = raw_input('Press "ENTER" to exit.')

