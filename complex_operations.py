import os
import ROOT
from datetime import datetime

#### Input/Output info ####
inFilePaths     = ["/eos/user/l/lfavilla/rdf-tutorial/TT_semilep_2023_nominal.root"]
inTreeName      = "Events"
outFilePath     = "output_complex.root"


#### User info ####
username = str(os.environ.get('USER'))
inituser = str(os.environ.get('USER')[0])
uid      = int(os.getuid())
WorkDir  = os.environ["PWD"]

#### LOAD utils/postselection.h ####
text_file           = open(WorkDir+"/utils/library.h", "r")
library             = text_file.read()
def my_initialization_function():
    print(ROOT.gInterpreter.ProcessLine(".O"))
    ROOT.gInterpreter.Declare('{}'.format(library))
    print("end of initialization")
my_initialization_function()


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


df              = df.Define("PuppiMET_T1_pt_nominal_vec", "RVec<float>{ (float) PuppiMET_T1_pt_nominal}")\
                    .Define("PuppiMET_T1_pt_jesTotalup_vec", "RVec<float>{ (float) PuppiMET_T1_pt_jesTotalup}")\
                    .Define("PuppiMET_T1_pt_jesTotaldown_vec", "RVec<float>{ (float) PuppiMET_T1_pt_jesTotaldown}")
df              = df.Vary(
                            ["Jet_pt_nominal", "PuppiMET_T1_pt_nominal_vec"],
                            "RVec<RVec<RVec<float>>>{{Jet_pt_jesTotalup, Jet_pt_jesTotaldown}, {PuppiMET_T1_pt_jesTotalup_vec, PuppiMET_T1_pt_jesTotaldown_vec}}",
                            variationTags=["UP", "DOWN"],
                            variationName="scenario")
df              = df.Define("Electron_isTight_idx",                 "func_TightElectron_idx(Electron_pt, Electron_eta, Electron_cutBased)")
df              = df.Define("HadronTransverseMass",                 "func_MHT(GoodJet_idx, Jet_pt_nominal, Jet_phi, Jet_eta, Jet_mass_nominal)")
df              = df.Filter("PuppiMET_T1_pt_nominal > 50.0",        "MET cut at 50 GeV")
df              = df.Filter("nTopLep >= 1",                         "at least one TopLeptonic")
df              = df.Define("MHT_new",                              "func_MHT(GoodJet_idx, Jet_pt_nominal, Jet_phi, Jet_eta, Jet_mass_nominal)")
report          = df.Report()

#### Create histograms ####
h_mht           = df.Histo1D(("MHT_new",                            "MHT;MHT [GeV];Events;", 50, 0, 1000), "MHT_new")  # computation booked, not run
h_mht_varied    = ROOT.RDF.Experimental.VariationsFor(h_mht)
print(h_mht)
print(h_mht_varied.GetKeys())
#### Save histograms to output file ####
outFile                 = ROOT.TFile(outFilePath, "RECREATE")
for key in h_mht_varied.GetKeys():
    h_mht_varied[key].Write()
outFile.Close()


#### Print out some info ####
print(f"How many times was data processed? {df.GetNRuns()}")
print(report.Print())


t1              = datetime.now()
print(f"Job finished in: {t1-t0}")