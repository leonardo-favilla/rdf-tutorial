import ROOT

inFilePaths     = ["/eos/user/l/lfavilla/rdf-tutorial/TT_semilep_2023_nominal.root"]
inTreeName      = "Events"

tchain          = ROOT.TChain(inTreeName)
for inFilePath in inFilePaths:
    tchain.Add(inFilePath)

df              = ROOT.RDataFrame(tchain)
branches        = list(map(str, df.GetColumnNames()))
print(f"Available branches: {len(branches)}")