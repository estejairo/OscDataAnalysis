auto c1 = new TCanvas('c1','All events',1500,500);

TMultiGraph *selectedEventsCh1 = new TMultiGraph('selectedEventsCh1','Ch1 Amplitude Vs Time; Time [s]; Amplitude [V]');
//selectedEventsCh1 = TMultiGraph('selectedEventsCh1','Ch1 Amplitude Vs Time - Selected Pulses; Time [s]; Amplitude [V]');

for (int i = 0; i<100; i++)
{
    selectedData->GetEntry(i);
    TGraph* graph1 = new TGraph(2502,selectedData.time,selectedData.ampCh1);
    //graph1 = TGraph(2502,selectedData.time,selectedData.ampCh1)
    selectedEventsCh1->Add(graph1);
    delete graph1;
} 
        

        


    //Ajuste y dibujo de histogramas
   

    c1.cd(1)
    selectedEventsCh1.Draw('AL')