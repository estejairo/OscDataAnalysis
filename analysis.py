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

from experiments import analyse

ROOT = tk.Tk()
ROOT.withdraw()


file = "../../data/na22-free-rigth.root"
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


analyze(file)

z = raw_input('Press "ENTER" to exit.')
