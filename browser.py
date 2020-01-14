###########################################
#
#   Scrip para abrir archivos .root con
#   viewer de ROOT.
#
#   Autor: Hernan Oyanadel
#
###########################################

from ROOT import  TFile,TTree,TBrowser,TGraph,TCanvas,TMultiGraph
#ev = 10
Files0 = TFile('../data/na22-free-tree.root','read')

B = TBrowser()
#T1.StartViewer()
z = raw_input('Done.')
