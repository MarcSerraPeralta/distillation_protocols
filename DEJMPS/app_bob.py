from dejmps import dejmps_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity

import netsquid as ns
from netsquid.qubits import operators
from netqasm.runtime.settings import get_simulator, Simulator

def bell_state():
    if get_simulator() != Simulator.NETSQUID:
        raise RuntimeError("`qubit_from` function only possible with NetSquid simulator")

    q1, q2 = ns.qubits.create_qubits(2)
    ns.qubits.operate(q1, operators.H)
    ns.qubits.operate([q1, q2], operators.CNOT)
    return q1

def main(app_config=None):
    
    # Create a socket for classical communication
    socket = Socket("bob", "alice")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice", min_fidelity=0)

    # Initialize Bob's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
    )

    # Create Bob's context, initialize EPR pairs inside it and call Bob's DEJMPS method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        epr_1, epr_2 = epr_socket.recv(number=2)
        succ = dejmps_protocol_bob(epr_1, epr_2, bob, socket)

        # Fidelity calculation
        original = bell_state()
        dm_exp = get_qubit_state(epr_2, reduced_dm=False)
        fidelity = get_fidelity(original, dm_exp)
    
    # save data
    f = open("data/P0-7500_G1-0000.txt", "a")
    if succ:
        f.write("1 {:0.8f}\n".format(fidelity))
    else:
        f.write("0 {:0.8f}\n".format(0))
    f.close()

    return


if __name__ == "__main__":
    main()
