from three_to_one import three_to_one_protocol_alice
from netqasm.sdk import EPRSocket
from netqasm.sdk.external import NetQASMConnection, Socket

def main(app_config=None):

    # Create a socket for classical communication
    socket = Socket("alice", "bob")

    # Create a EPR socket for entanglement generation
    epr_socket = EPRSocket("bob")

    # Initialize Alice's NetQASM connection
    alice = NetQASMConnection(
        app_name = app_config.app_name,
        epr_sockets = [epr_socket]
        )

    # Create Alice's context, initialize EPR pairs inside it and call Alice's 3->1 method. Finally, print out whether or not Alice successfully created an EPR Pair with Bob.
    with alice:

        q1, q2, q3 = epr_socket.create(number=3)
        succ = three_to_one_protocol_alice(q1, q2, q3, alice, socket)

        #print(succ)
        
    return


if __name__ == "__main__":
    main()
