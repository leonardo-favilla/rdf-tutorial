#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"


using namespace ROOT::VecOps;
// using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;
using rvec_b = const RVec<bool> &;

RVec<int> func_TightElectron_idx(rvec_f Electron_pt, rvec_f Electron_eta, rvec_f Electron_cutBased)
{
    RVec<int> idx;
    for(int i = 0; i<Electron_pt.size(); i++)
        {
            if(Electron_cutBased[i]>=4 && Electron_pt[i] > 50 && abs(Electron_eta[i])<2.5)
            {
                idx.emplace_back(i);
            }
        }
    return idx;
}

float func_MHT(rvec_f GoodJet_idx, rvec_f Jet_pt, rvec_f Jet_phi, rvec_f Jet_eta, rvec_f Jet_mass)
{
    RVec<ROOT::Math::PtEtaPhiMVector> v;
    for(int i = 0; i < GoodJet_idx.size(); i++)
        {
            const ROOT::Math::PtEtaPhiMVector tmp_ {Jet_pt[GoodJet_idx[i]], Jet_eta[GoodJet_idx[i]], Jet_phi[GoodJet_idx[i]], Jet_mass[GoodJet_idx[i]]};
            v.emplace_back(tmp_);
        }
    auto v_sum_lv = Sum(v, ROOT::Math::PtEtaPhiMVector());
    return v_sum_lv.M();
}