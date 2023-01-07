#Kohn-Sham density functional theory (KS-DFT) has been implemented through derived classes of the pyscf.scf.hf.SCF 

from pyscf import gto, lo.tools,dft

#The efficient second-order Newton-Rapson Algorithm

from rdkit import Chem
from rdkit.Chem import AllChem
import py3Dmol

H2 = 'H 0 0 0; H 0 0 1.1'
mol_hartree = gto.M(atom=H2, basis = 'ccpvdz', symmetry = True) 
mf_hartree = dft.RKS(mol_hartree)
#xc functional choice
mf_hartree.xc = 'lda,vwn' #default LDA functional -> exhanfe-correlation energy 
mf_hartree = mf_hartree.newton() # second-order algorithm
normal = mf_hartree.kernel()

#define xc functional via DFT.xc
mf_hartree.xc('pbe,pbe') #PBE exchange plus PBE correlation

HF_X, LDA_X = .6, .08
B88_X = 1. - HF_X - LDA_X
LYP_C = .81
VWN_C = 1. -  LYP_C
mf_hartree.xc = f'{HF_X:} * HF + {LDA_X:} * LDA + {B88_X:} * B88, {LYP_C:} * LYP + {VWN_C:} * VWN'
customized = mf_hartree.kernel()

smiles_file = "c1ccccc1"
mol = Chem.MolFromSmiles(smiles_file)
mol = Chem.AddHs(mol)

AllChem.EmbedMolecule(mol)
AllChem.MMFFOptimizeMolBlock(mol, 'mol')


v = py3Dmol.view()
v.addModel(Chem.MolToMolBlock(mol), 'mol')
v.setStyle({'stick':{}})

#getting all the elements from molecule
elements = [atom.GetSymbol() for atom in mol.GetAtoms()]
#Atom coordinates
coordinates = mol.GetConformer().GetPositions()
#
atoms = [(elements, coordinates) for elements, coordinates in zip(elements, coordinates)]
pysc_mole = gto.Mole(basis="sto-3g")
pysc_mole.atom = atoms
pysc_mole.build();


