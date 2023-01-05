from qiskit.algorithms import VQE
#H2 molecule
from qiskit import Aer 
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.converters.second_quantization.qubit_converter import QubitConverter
from qiskit_nature.problems.second_quantization.electronic import ElectronicStructureProblem
from qiskit_nature.mappers.second_quantization import JordanWignerMapper #https://www.youtube.com/watch?v=43riaeeRDHo
#Jordan-Wingner Transformation that maps the spin operators
from qiskit_nature.circuit.library import HartreeFock
#Hartree-Fock quantum state circuit
from qiskit.circuit import Parameter, QuantumCircuit, QuantumRegister


Tbackend = Aer.get_backend('statevector_simulator')

H2 = "H .0 .0 .0; H .0 .0 0.739"
driver = PySCFDriver(atom=H2)
qmolecule = driver.run()

problem = ElectronicStructureProblem(driver)
second_q_ops = problem.second_q_ops()
main_p = second_q_ops[0]

mapper = JordanWignerMapper()
converter = QubitConverter(mapper=mapper)