"""
This is a canned example for generating descriptors
Please modify as necessary
"""
from __future__ import print_function
from . import rdkit_fixes
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.Chem import rdMolDescriptors as rd
import numpy
from .DescriptorGenerator import DescriptorGenerator
import logging

import sys

def clip(v, name):
    if v > 255:
        logging.warning("%s has >255 counts for a feature vector clipping", name)
        v = 255
    return v
        

class MorganCounts(DescriptorGenerator):
    """Computes Morgan3 bitvector counts"""
    NAME = "Morgan%sCounts"
    def __init__(self, radius=3, nbits=2048):
        if radius == 3 and nbits == 2048:
            self.NAME = self.NAME % "3"
        else:
            self.NAME = self.NAME % ("%s-%s"%radius,nbits)
            
        DescriptorGenerator.__init__(self)
        # specify names and numpy types for all columns
        self.radius = radius
        self.nbits = nbits
        morgan = [("m3-%d"%d, numpy.uint8) for d in range(nbits)]
        self.columns += morgan

    def calculateMol(self, m, smiles, internalParsing=False):
        counts = list(rd.GetHashedMorganFingerprint(m,
                                                    radius=self.radius, nBits=self.nbits))
        counts = [ clip(x,smiles) for x in counts ]
        return counts        

MorganCounts()

class ChiralMorganCounts(DescriptorGenerator):
    """Computes Morgan3 bitvector counts"""
    NAME = "Morgan%sCounts"
    def __init__(self, radius=3, nbits=2048, useChirality=True):
        if radius == 3 and nbits == 2048 and (useChirality is True):
            self.NAME = self.NAME % "Chiral3"
        else:
            if useChirality is True:
                useChrial_string = 'chiral'
            else:
                useChrial_string = ''
                # no mention means nonchiral morgans
            self.NAME = self.NAME % ("%s%s-%s"%useChrial_string,radius,nbits)
            
        DescriptorGenerator.__init__(self)
        # specify names and numpy types for all columns
        self.radius = radius
        self.nbits = nbits
        self.useChirality = useChirality
        morgan = [("m3-%d"%d, numpy.uint8) for d in range(nbits)]
        self.columns += morgan

    def calculateMol(self, m, smiles, internalParsing=False):
        counts = list(rd.GetHashedMorganFingerprint(m,
                                                    radius=self.radius, nBits=self.nbits,useChirality=self.useChirality))
        counts = [ clip(x,smiles) for x in counts ]
        return counts        

MorganCounts()



RDKIT_PROPS = {"1.0.0": ['BalabanJ', 'BertzCT', 'Chi0', 'Chi0n', 'Chi0v', 'Chi1', 'Chi1n',
                         'Chi1v', 'Chi2n', 'Chi2v', 'Chi3n', 'Chi3v', 'Chi4n', 'Chi4v',
                         'EState_VSA1', 'EState_VSA10', 'EState_VSA11', 'EState_VSA2',
                         'EState_VSA3', 'EState_VSA4', 'EState_VSA5', 'EState_VSA6',
                         'EState_VSA7', 'EState_VSA8', 'EState_VSA9', 'ExactMolWt',
                         'FpDensityMorgan1', 'FpDensityMorgan2', 'FpDensityMorgan3',
                         'FractionCSP3', 'HallKierAlpha', 'HeavyAtomCount', 'HeavyAtomMolWt',
                         'Ipc', 'Kappa1', 'Kappa2', 'Kappa3', 'LabuteASA', 'MaxAbsEStateIndex',
                         'MaxAbsPartialCharge', 'MaxEStateIndex', 'MaxPartialCharge',
                         'MinAbsEStateIndex', 'MinAbsPartialCharge', 'MinEStateIndex',
                         'MinPartialCharge', 'MolLogP', 'MolMR', 'MolWt', 'NHOHCount',
                         'NOCount', 'NumAliphaticCarbocycles', 'NumAliphaticHeterocycles',
                         'NumAliphaticRings', 'NumAromaticCarbocycles', 'NumAromaticHeterocycles',
                         'NumAromaticRings', 'NumHAcceptors', 'NumHDonors', 'NumHeteroatoms',
                         'NumRadicalElectrons', 'NumRotatableBonds', 'NumSaturatedCarbocycles',
                         'NumSaturatedHeterocycles', 'NumSaturatedRings', 'NumValenceElectrons',
                         'PEOE_VSA1', 'PEOE_VSA10', 'PEOE_VSA11', 'PEOE_VSA12', 'PEOE_VSA13',
                         'PEOE_VSA14', 'PEOE_VSA2', 'PEOE_VSA3', 'PEOE_VSA4', 'PEOE_VSA5',
                         'PEOE_VSA6', 'PEOE_VSA7', 'PEOE_VSA8', 'PEOE_VSA9', 'RingCount',
                         'SMR_VSA1', 'SMR_VSA10', 'SMR_VSA2', 'SMR_VSA3', 'SMR_VSA4', 'SMR_VSA5',
                         'SMR_VSA6', 'SMR_VSA7', 'SMR_VSA8', 'SMR_VSA9', 'SlogP_VSA1', 'SlogP_VSA10',
                         'SlogP_VSA11', 'SlogP_VSA12', 'SlogP_VSA2', 'SlogP_VSA3', 'SlogP_VSA4',
                         'SlogP_VSA5', 'SlogP_VSA6', 'SlogP_VSA7', 'SlogP_VSA8', 'SlogP_VSA9',
                         'TPSA', 'VSA_EState1', 'VSA_EState10', 'VSA_EState2', 'VSA_EState3',
                         'VSA_EState4', 'VSA_EState5', 'VSA_EState6', 'VSA_EState7', 'VSA_EState8',
                         'VSA_EState9', 'fr_Al_COO', 'fr_Al_OH', 'fr_Al_OH_noTert', 'fr_ArN',
                         'fr_Ar_COO', 'fr_Ar_N', 'fr_Ar_NH', 'fr_Ar_OH', 'fr_COO', 'fr_COO2',
                         'fr_C_O', 'fr_C_O_noCOO', 'fr_C_S', 'fr_HOCCN', 'fr_Imine', 'fr_NH0',
                         'fr_NH1', 'fr_NH2', 'fr_N_O', 'fr_Ndealkylation1', 'fr_Ndealkylation2',
                         'fr_Nhpyrrole', 'fr_SH', 'fr_aldehyde', 'fr_alkyl_carbamate', 'fr_alkyl_halide',
                         'fr_allylic_oxid', 'fr_amide', 'fr_amidine', 'fr_aniline', 'fr_aryl_methyl',
                         'fr_azide', 'fr_azo', 'fr_barbitur', 'fr_benzene', 'fr_benzodiazepine',
                         'fr_bicyclic', 'fr_diazo', 'fr_dihydropyridine', 'fr_epoxide', 'fr_ester',
                         'fr_ether', 'fr_furan', 'fr_guanido', 'fr_halogen', 'fr_hdrzine', 'fr_hdrzone',
                         'fr_imidazole', 'fr_imide', 'fr_isocyan', 'fr_isothiocyan', 'fr_ketone',
                         'fr_ketone_Topliss', 'fr_lactam', 'fr_lactone', 'fr_methoxy', 'fr_morpholine',
                         'fr_nitrile', 'fr_nitro', 'fr_nitro_arom', 'fr_nitro_arom_nonortho',
                         'fr_nitroso', 'fr_oxazole', 'fr_oxime', 'fr_para_hydroxylation', 'fr_phenol',
                         'fr_phenol_noOrthoHbond', 'fr_phos_acid', 'fr_phos_ester', 'fr_piperdine',
                         'fr_piperzine', 'fr_priamide', 'fr_prisulfonamd', 'fr_pyridine', 'fr_quatN',
                         'fr_sulfide', 'fr_sulfonamd', 'fr_sulfone', 'fr_term_acetylene', 'fr_tetrazole',
                         'fr_thiazole', 'fr_thiocyan', 'fr_thiophene', 'fr_unbrch_alkane', 'fr_urea', 'qed']
               }

CURRENT_VERSION = "1.0.0"

FUNCS = {name:func for name, func in Descriptors.descList}
def applyFunc(name, m):
    try:
        return FUNCS[name](m)
    except:
        logging.exception("function application failed (%s->%s)",
            name, Chem.MolToSmiles(m))
                       
        return None

class RDKit2D(DescriptorGenerator):
    """Computes all RDKit Descriptors"""
    NAME = "RDKit2D"
    def __init__(self, properties=RDKIT_PROPS[CURRENT_VERSION]):
        DescriptorGenerator.__init__(self)
        # specify names and numpy types for all columns
        if not properties:
            self.columns = [ (name, numpy.float64) for name,func in sorted(Descriptors.descList) ]
        else:
            columns = self.columns
            failed = []
            
            for name in properties:
                if name in sorted(FUNCS):
                    columns.append((name, numpy.float64))
                else:
                    logging.error("Unable to find specified property %s"%name)
                    failed.append(name)
            if failed:
                raise ValueError("%s: Failed to initialize: unable to find specified properties:\n\t%s"%(
                    self.__class__.__name__,
                    "\n\t".join(failed)))
        
    def calculateMol(self, m, smiles, internalParsing=False):
        res = [ applyFunc(name, m) for name, _ in self.columns ]
        return res
    

RDKit2D()

    
