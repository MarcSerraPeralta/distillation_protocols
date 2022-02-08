from epl import epl_protocol_bob
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity

import netsquid as ns 
from netsquid.qubits import operators
from netqasm.runtime.settings import get_simulator, Simulator

def bell_state():
    if get_simulator() != Simulator.NETSQUID:
        raise RuntimeError("'qubit_from' function only possible with NETSquid simulator")

    q1, q2 = ns.qubits.create_qubits(2)
    ns.qubits.operate(q1, operators.H)
    ns.qubits.operate([q1, q2], operators.CNOT)
    ns.qubits.operate(q2, operators.X)
    return q1


def main(app_config=None):
    
   
    # Create a socket for classical communication
    socket = Socket("bob", "alice")
    

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("alice")


    # Initialize Alice's NetQASM connection
    bob = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
        )
    

    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with bob:
        #initialize EPR pair
        epr_1, epr_2 = epr_socket.recv(number=2)
        succ = epl_protocol_bob(epr_1, epr_2, bob, socket)
        print( "Success for BOB: ", succ)

        #Fidelity stuff

        original = bell_state()
        #compute density matrix
        dm_b = get_qubit_state(epr_1, reduced_dm=False)
        dm = original.qstate.dm
        fidelity = get_fidelity(original, dm_b)
        print("Fidelity: ", fidelity)

    #save data
    f = open("data/F0-9500_G0-9500.txt", "a")
    if succ:
       f.write("1 {:0.8f}\n".format(fidelity)) 
    else:
        f.write("0 {:0.8f}\n".format(0))

    f.close()

    return
        


if __name__ == "__main__":
    main()
