#!/usr/bin/env python3
__author__ = "Sam Danforth"
from random import randint


# Generate random integer from 0 to 255, convert to 8-bit binary number
def generateMessage():
    message = randint(0, 255)
    message = bin(message)
    return message
# TODO: Generate list of 1000 messages


# TODO: Move message creation operations to generate function
# Count number of 1s in message, if even then checksum is 1
def createChecksum(msg):
    count = 0
    checksum = 0
    msg = str(msg)
    msg = msg.replace("0b", "")
    msg = msg.zfill(8)
    for character in msg:
        if character == "1":
            count += 1
        elif character != "0":
            raise ValueError("Message contains non-binary data.")
    if count % 2 == 0:
        checksum = 1
        return checksum, msg
    else:
        return checksum, msg


# Combines message, acknowledgment bit of 0, and checksum into one string
def prepareMessage(message, checksum):
    message = str(message)
    checksum = str(checksum)
    finalMessage = message + "0" + checksum
    return finalMessage
