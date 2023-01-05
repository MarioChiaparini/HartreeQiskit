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

#loading the molecule
H2 = "H .0 .0 .0; H .0 .0 0.739"
driver = PySCFDriver(atom=H2,  
                     unit=UnitsType.ANGSTROM,
                     basis='sto3g')
qmolecule = driver.run()
#build the eletronic structure problem 
problem = ElectronicStructureProblem(driver)
#Generate the second-quantized operators 
second_q_ops = problem.second_q_ops()
#Hamiltonian
main_p = second_q_ops[0]

mapper = JordanWignerMapper()
converter = QubitConverter(mapper=mapper)

#Fermionic operador mapped to qubits operators
num_particles = (problem.grouped_property_transformed.num_alpha,
                problem.grouped_property_transformed.num_beta)
qoperador = converter.convert(main_p, num_particles=num_particles) 

#Create a Hartree-Fock circuit
num_particles = (problem.grouped_property_transformed.num_alpha,
             problem.grouped_property_transformed.num_beta)

num_spin_orbitals = 2 * problem.grouped_property_transformed.num_spin_orbitals
init_state = HartreeFock(num_spin_orbitals, num_particles, converter)

#Create dummy parametrized circuit
theta = Parameter('a')
n = qubit_op.num_qubits
qc = QuantumCircuit(qubit_op.num_qubits)
qc.rz(theta*0,0)
ansatz = qc
ansatz.compose(init_state, front=True, inplace=True)

#Pass it through VQE
algorithm = VQE(ansatz,quantum_instance=backend)
result = algorithm.compute_minimum_eigenvalue(qubit_op).eigenvalue
print(result)