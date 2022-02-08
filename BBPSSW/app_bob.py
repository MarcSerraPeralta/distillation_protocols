from bbpssw import bbpssw_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity

import netsquid as ns
from netsquid.qubits import operators
from netqasm.runtime.settings import get_simulator, Simulator



def bell_state():
    if get_simulator() != Simulator.NETSQUID:
        raise RuntimeError("Only possible with NetSquid Simulator")
    q1, q2 = ns.qubits.create_qubits(2)
    ns.qubits.operate(q1, operators.H)
    ns.qubits.operate([q1, q2], operators.CNOT)
    return q1

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket("bob", "alice")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's BBPSSW method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
    # Initialize EPR pairs
        epr1, epr2 = epr_socket.recv(number=2)

        # Call BBPSSW method
        success = bbpssw_protocol_bob(epr1, epr2, bob, socket)

        # Fidelity
        original = bell_state()
        dm_exp = get_qubit_state(epr1, reduced_dm=False)
        fidelity = get_fidelity(original, dm_exp)

    print("Bob measurement is:", success)
    print("The fidelity is: ", fidelity)

    f = open("data/P0-0000_G0-6000.txt", "a")
    if success:
        f.write("1 {}\n".format(fidelity))
    else:
        f.write("0 {}\n".format(0))
    f.close()
    
    return


if __name__ == "__main__":
    main()
