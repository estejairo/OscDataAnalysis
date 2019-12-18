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

from experiments import select, analyze, graphAnalysis

import time
from tqdm import tqdm #libreria para visualizar porcentaje restante

EVENTOS = 2000
MUESTRAS = 2502
ref_init_noise_rms = 0.005
ref_final_noise_rms = 0.005

# ROOT = tk.Tk()
# ROOT.withdraw()
# filez = tkFileDialog.askopenfilenames(parent=root,title='Choose files')
# lst = list(filez)

# for file_input in lst:
#     select(file_input,ref_init_noise_rms,ref_final_noise_rms)
#     analyze(file_input)

file_input = "../../data/na22-free-rigth.root"
experiment="free"
keyword = "right"

## Data Selection
#select(file_input,ref_init_noise_rms,ref_final_noise_rms)

## Average Peak voltage per event
#analyze(file_input)


## Data graph
graphAnalysis(file_input,experiment,keyword)

z = raw_input('Press "ENTER" to exit.')

