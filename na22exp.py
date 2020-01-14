############################################################
#
#   En este script se generan histogramas para analizar
#   la relacion de amplitudes de pulsos con la posicion de
#   los canales medidos respecto a la fuente radioactiva.
#  
#   Autor: Jairo Gonzalez
#   Estado: Terminado
#
###########################################################

from experiments import select, analyze, graphAnalysis
import Tkinter as tk
import Tkconstants, tkFileDialog, tkSimpleDialog


ref_init_noise_rms = 0.005
ref_final_noise_rms = 0.005

ROOT = tk.Tk()
ROOT.withdraw()
filez = tkFileDialog.askopenfilenames(parent=ROOT,title='Choose files')
lst = list(filez)

for file_input in lst:
    print "\n##########################\nProcessing file: "+file_input+"\n"
    select(file_input,ref_init_noise_rms,ref_final_noise_rms)
    analyze(file_input)
    if "free" in file_input:
        if "right" in file_input:
            graphAnalysis(file_input,"free","right")
        elif "center" in file_input:
            graphAnalysis(file_input,"free","center")
        else:
            graphAnalysis(file_input,"free","left")
    else:
        if "right" in file_input:
            graphAnalysis(file_input,"collimator","right")
        elif "center" in file_input:
            graphAnalysis(file_input,"collimator","center")
        else:
            graphAnalysis(file_input,"collimator","left")
    

z = raw_input('Press "ENTER" to exit.')

