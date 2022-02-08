from three_to_one import three_to_one_protocol_bob
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
    #ns.qubits.operate(q2, operators.X)
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

    # Create Bob's context, initialize EPR pairs inside it and call Bob's 3->1 method. Finally, print out whether or not Bob successfully created an EPR Pair with Alice.
    with bob:
        q1, q2, q3 = epr_socket.recv(number=3)
        succ = three_to_one_protocol_bob(q1, q2, q3, bob, socket)
        #print(succ)

        # Fidelity things

        original = bell_state()
        dm_B = get_qubit_state(q3, reduced_dm=False) # Get the qubit state

        dm = original.qstate.dm
        fp = get_fidelity(original, dm_B)
        #print("Fidelity: ", fp)
        #print(dm_B)

    f = open("data/F0-9500_G0-9500.txt", "a")
    if succ:
        f.write("1 {:0.8f}\n".format(fp))
    else:
        f.write("0 {:0.8f}\n".format(0))
    f.close()

    return


if __name__ == "__main__":
    main()
