import math
from netqasm.sdk.classical_communication.message import StructuredMessage


def three_to_one_protocol_alice(q1, q2, q3, alice, socket):
    """
    Implements Alice's side of the BBPSSW distillation protocol.
    This function should perform the gates and measurements for 3->1 using
    qubits q1 and q2, then send the measurement outcome to Bob and determine
    if the distillation was successful.
    
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param q3: Alice's qubit from the third entangled pair
    :param alice: Alice's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    a1, a2 = three_to_one_gates_and_measurement_alice(q1, q2, q3)
    alice.flush()

    # Send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    a1 = int(a1)
    a2 = int(a2)

    socket.send_structured(StructuredMessage("The outcome is: ", (a1, a2)))
    b1, b2 = socket.recv_structured().payload

    if (a1, a2) == (b1, b2):
        return True
    else:
        return False


def three_to_one_gates_and_measurement_alice(q1, q2, q3):
    """
    Performs the gates and measurements for Alice's side of the 3->1 protocol
    :param q1: Alice's qubit from the first entangled pair
    :param q2: Alice's qubit from the second entangled pair
    :param q3: Alice's qubit from the third entangled pair
    :return: A pair of integer 0/1 indicating Alice's measurement outcomes from measuring the qubits
    """
    q3.cnot(q2)
    q1.cnot(q3)

    #Bell measurement
    q1.cnot(q2)
    q1.H()
    m1 = q1.measure()
    m2 = q2.measure()
    return m1, m2


def three_to_one_protocol_bob(q1, q2, q3, bob, socket):
    """
    Implements Bob's side of the 3->1 distillation protocol.
    This function should perform the gates and measurements for 3->1 using
    qubits q1 and q2, then send the measurement outcome to Alice and determine
    if the distillation was successful.
    
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param q3: Bob's qubit from the third entangled pair
    :param bob: Bob's NetQASMConnection
    :param socket: Alice's classical communication socket to Bob
    :return: True/False indicating if protocol was successful
    """
    b1, b2 = three_to_one_gates_and_measurement_bob(q1, q2, q3)
    bob.flush()

    # Send measurement result to Bob, receive measurement result from Bob and check if protocol was successful
    b1 = int(b1)
    b2 = int(b2)

    socket.send_structured(StructuredMessage("The outcome is: ", (b1, b2)))
    a1, a2 = socket.recv_structured().payload

    if (a1, a2) == (b1, b2):
        return True
    else:
        return False

def three_to_one_gates_and_measurement_bob(q1, q2, q3):
    """
    Performs the gates and measurements for Bob's side of the 3->1 protocol
    :param q1: Bob's qubit from the first entangled pair
    :param q2: Bob's qubit from the second entangled pair
    :param q3: Bob's qubit from the third entangled pair
    :return: A pair of integer 0/1 indicating Bob's measurement outcomes from measuring the qubits
    """
    q3.cnot(q2)
    q1.cnot(q3)

    #Bell measurement
    q1.cnot(q2)
    q1.H()
    m1 = q1.measure()
    m2 = q2.measure()
    return m1, m2

