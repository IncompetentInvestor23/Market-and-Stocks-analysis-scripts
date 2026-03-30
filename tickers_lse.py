# src/tickers_lse.py

"""
Complete list of the LSE 100 and LSE 250 tickers.
Source: based on FTSE index.
"""

def get_lse_tickers():
    """
    Returns all the LSE 100 and LSE 250 tickers.
    Yahoo Finance format: .L at the end.
    """

    #FTSE 100 (The 100 biggest companies)

    ftse100 = ['III.L','ADM.L','AAF.L','ALW.L','AAL.L','ANTO.L','ABF.L','AZN.L','AUTO.L','AV.L',
 'BAB.L','BA.L','BARC.L','BTRW.L','BEZ.L','BKG.L','BP.L','BATS.L','BLND.L','BNZL.L',
 'BTA.L','CNA.L','CCH.L','CPG.L','CTEC.L','DCC.L','DGE.L','EDV.L','ENT.L','EXPN.L',
 'FCIT.L','FLTR.L','FRES.L','GLEN.L','GSK.L','HLN.L','HLMA.L','HSBA.L','IHG.L','IMB.L',
 'INF.L','ITRK.L','JD.L','KGF.L','LAND.L','LGEN.L','LLOY.L','LSEG.L','MNDI.L','MKS.L',
 'MNG.L','NG.L','NWG.L','NXT.L','OCDO.L','PSON.L','PSN.L','PHNX.L','PRU.L','RKT.L',
 'REL.L','RIO.L','RR.L','RTO.L','SBRY.L','SHEL.L','SGE.L','SGRO.L','SSE.L','STAN.L',
 'STJ.L','SVT.L','SMIN.L','SN.L','SPX.L','TSCO.L','ULVR.L','UU.L','VOD.L','WEIR.L',
 'WTB.L','WPP.L']
    #FTSE 250 (The next 250 biggest companies)

    ftse250 = ['ADR.L','ABDN.L','ALFA.L','ASHM.L','ASC.L','ATG.L','BAG.L',
 'BCG.L','BDEV.L','BME.L','BNKR.L','BOY.L','BRBY.L','BREE.L','BYG.L','CAML.L','CCC.L',
 'CCL.L','CEY.L','CHG.L','CLDN.L','CMCX.L','COA.L','COST.L','CRDA.L','CREO.L','CSN.L',
 'CTY.L','CURY.L','DARK.L','DOM.L','DRX.L','DSCV.L','DWL.L','EOT.L','ENOG.L','ESNT.L',
 'EWG.L','FCSS.L','FEVR.L','FGP.L','FOUR.L','FRAS.L','FSV.L','FUTR.L','GAMA.L','GAW.L','GEN.L',
 'GFRD.L','GFTU.L','GNS.L','GOG.L','GRG.L','HAS.L','HFD.L','HIK.L','HMSO.L','HOC.L',
 'HTWS.L','IBST.L','IGG.L','INCH.L','INDV.L','INPP.L','IPO.L','IRV.L','JMAT.L','JTC.L',
 'KLR.L','KIE.L','LMP.L','LOOK.L','MGNS.L','MGGT.L','MAB.L','MCG.L','MONY.L','MOON.L',
 'MTRO.L','NCC.L','NEX.L','NICL.L','NWF.L','OXIG.L','PAG.L','PANR.L','PCIP.L','PET.L',
 'PLUS.L','PNN.L','POLY.L','QTX.L','RAT.L','RCH.L','RDW.L','RMV.L','ROR.L','RS1.L',
 'SAFE.L','SAGA.L','SDR.L','SHED.L','SIXH.L','SNR.L','SSPG.L','STB.L','STEM.L',
 'SUPR.L','SYNT.L','TCAP.L','TBCG.L','TEP.L','TFW.L','THRL.L','TIFS.L','TPT.L','TRIG.L',
 'TRN.L','TUNE.L','UKCM.L','UTG.L','VID.L','VSVS.L','WOSG.L','XPS.L']

    #Combine both lists and eliminate duplicates

    all_tickers = list(set(ftse100 + ftse250))

    print(f"Total tickers LSE loaded: {len(all_tickers)}")
    return all_tickers

if __name__ == '__main__':
    tickers = get_lse_tickers()
