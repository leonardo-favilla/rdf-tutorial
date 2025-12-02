import os
import ROOT
from datetime import datetime


#### Input/Output info ####
inFilePaths     = ["/eos/user/l/lfavilla/rdf-tutorial/TT_semilep_2023_nominal.root"]
inTreeName      = "Events"
outFilePath     = "output.root"






#### Open input files ####
tchain          = ROOT.TChain(inTreeName)
for inFilePath in inFilePaths:
    tchain.Add(inFilePath)


######## MAIN CODE ########
t0              = datetime.now()
print(f"Local time: {t0}")

df              = ROOT.RDataFrame(tchain)
nev             = df.Count()
branches        = list(map(str, df.GetColumnNames()))
print(f"Available branches: {len(branches)}")

#### Apply a simple filters ####
df_met_g250             = df.Filter("PuppiMET_T1_pt > 250.0", "MET cut at 250 GeV")         # computation booked, not run
nev_met_g250            = df_met_g250.Count()                                               # computation booked, not run
df_nJets_ge4            = df_met_g250.Filter("nJet >= 4", "at least four jets")             # computation booked, not run
nev_nJets_ge4           = df_nJets_ge4.Count()                                              # computation booked, not run
df_nTopMixed_ge1        = df_nJets_ge4.Filter("nTopMixed >= 1", "at least one TopMixed")    # computation booked, not run
nev_nTopMixed_ge1       = df_nTopMixed_ge1.Count()                                          # computation booked, not run
#### Define new variables ####
df_leadjetpt            = df_nTopMixed_ge1.Define("LeadingJet_pt", "(float)Max(Jet_pt)")    # computation booked, not run
#### Create histograms ####
h_met_pt                = df_leadjetpt.Histo1D(("h_met_pt",     "PuppiMET_T1_pt;PuppiMET_T1_pt [GeV];Events;", 50, 0, 1000), "PuppiMET_T1_pt")  # computation booked, not run
h_leadjet_pt            = df_leadjetpt.Histo1D(("h_leadjet_pt", "Leading Jet pt;Leading Jet pt [GeV];Events;", 50, 0, 1000), "LeadingJet_pt")   # computation booked, not run


#### Trigger the actions ####
print("Actions are now triggered, computations start...")
print(f"Number of events before any cut:                {nev.GetValue()}")
print(f"Number of events after MET > 250 GeV:           {nev_met_g250.GetValue()}")
print(f"Number of events after at least 4 jets:         {nev_nJets_ge4.GetValue()}")
print(f"Number of events after at least 1 TopMixed:     {nev_nTopMixed_ge1.GetValue()}")
#### Save histograms to output file ####
outFile                 = ROOT.TFile(outFilePath, "RECREATE")
h_met_pt.Write()
h_leadjet_pt.Write()
outFile.Close()

#### Print out some info ####
print(f"How many times was data processed? {df_leadjetpt.GetNRuns()}")


t1              = datetime.now()
print(f"Job finished in: {t1-t0}")