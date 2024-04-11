#!/usr/bin/env python3
__author__ = "Sam Danforth"
from random import randint
import noisyChannel

# TODO: Migrate all functions to Transmitter class
goodMessages: list[str] = []


def storeGoodMessages(messages: list[str]):
    global goodMessages
    goodMessages = messages


# Generate random integer from 0 to 255, convert to 8-bit binary number, add to list total 10,000
def generateMessages():
    messages: list[str] = []
    for i in range(0, 10000):  # Generate 10,000 messages total
        message = randint(0, 255)  # Choose random 8-bit binary number (integer from 0-255)
        # Remove extra characters added by binary conversion and fill with leading zeros
        message = bin(message).replace("0b", "").zfill(8)
        messages.append(message)
    return messages


# Count number of 1s in message, if even then checksum is 1
def createChecksums(messages: list[str]):
    preppedMessages: list[str] = []
    count: int = 0
    for msg in messages:  # Iterate through message list
        for char in msg:  # Iterate through each character in message
            if char == "1":  # Check for how many ones are in the message
                count += 1
            elif char != "0":
                raise ValueError("Message contains non-binary data")
        # Create checksum and prepare message
        if count % 2 == 0:  # Even number of ones
            preppedMessages.append(msg + "01")  # Add ack bit (always 0) and then checksum of 1
        else:
            preppedMessages.append(msg + "00")  # Add ack bit and checksum of 0
        count = 0  # Reset counter
    storeGoodMessages(preppedMessages)
    return preppedMessages


def requestNewMessage(index: int):
    global goodMessages
    messageToResend = goodMessages[index]
    messageToResend = noisyChannel.bitFlipperSingle(messageToResend)
