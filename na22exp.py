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

from experiments import select


EVENTOS = 2000
MUESTRAS = 2502
ref_init_noise_rms = 0.002
ref_mid_noise_rms = 0.03


file_input = "../../data/na22-free-rigth.root"
#file_output = "../../data/na22-free-rigth-selected.root"

# file = tkFileDialog.askopenfilename(initialdir = "../data",
#                                     title = "Select file",
#                                     filetypes = (("root files","*.root"),
#                                     ("all files","*.*")))

select(file_input,ref_init_noise_rms,ref_mid_noise_rms)




z = raw_input('Press "ENTER" to exit.')

