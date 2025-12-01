import ROOT

inFilePath      = "/eos/user/l/lfavilla/rdf-tutorial/TT_semilep_2023_nominal.root"
inTreeName      = "Events"

df              = ROOT.RDataFrame(inTreeName, inFilePath)
branches        = list(map(str, df.GetColumnNames()))
print(f"Available branches: {len(branches)}")