from epl import epl_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket, get_qubit_state
#from netqasm.sdk.toolbox.sim_states import qubit_from, to_dm, get_fidelity
#from netqasm.sdek.classical_communication.message import StructuredMessage
#from netqasm.logging.output import get_new_app_logger
from numpy import pi


#def prepare_state(epr_1, epr_2, phi):
    #epr_1.X()
    #epr_1.rot_Z(angle=phi)
    #epr_2.X()
    #epr_2.rot_Z(angle=phi)


def main(app_config=None): #phi=0

   

    # Create a socket for classical communication
    socket = Socket("alice", "bob")
    

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")
    

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name=app_config.app_name,
        epr_sockets=[epr_socket]
        )


    # Create Alice's context, initialize EPR pairs inside it and call Alice's EPL method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:
        #initialize EPR pair
        epr_1, epr_2 = epr_socket.create(number=2)

        #prepare_state(epr_1, epr_2, phi)

        succ = epl_protocol_alice(epr_1, epr_2, alice, socket)


if __name__ == "__main__":
    main()
