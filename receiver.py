#!/usr/bin/env python3
__author__ = "Sam Danforth"


# TODO: Request message new message if bad
# Determine if message received is good or bad
def analyzeMessage(message):
    count = 0
    data = message[:8]
    ackBit = message[8]
    if ackBit == "1":  # Acknowledgment should be 0, if it's 1 it must be bad message
        return False
    checksum = message[9]
    dataBits = list(data)
    for bit in dataBits:  # Count how many 1s are in the received message
        if bit == "1":
            count += 1
        elif bit != "0":
            raise ValueError("Message contains non-binary data.")
    # Basically creating a new checksum for the received message and checking it matches the checksum bit
    if count % 2 == 0 and checksum == "1":
        return True
    if count % 2 == 1 and checksum == "0":
        return True
    else:
        return False
