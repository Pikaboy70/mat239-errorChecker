#!/usr/bin/env python3
__author__ = "Sam Danforth"

import noisyChannel
import transmitter

# TODO: Migrate all
acceptedMessages: list[str] = []
failCount: int = 0
noiseLevel: int = 0


def setNoiseLevel(noise: int):
    global noiseLevel
    noiseLevel = noise
    print(noiseLevel)


def goodMessage(message: str):
    global acceptedMessages
    acceptedMessages.append(message)


def badMessage(index: int):
    global failCount, noiseLevel
    failCount += 1
    newMessage = transmitter.requestNewMessage(index)
    message = noisyChannel.bitFlipperSingle(newMessage, noiseLevel)
    analyzeSingleMessage(message)


# TODO: Request message new message if bad
# Determine if message received is good or bad
def analyzeMessages(messages: list[str]):
    index = 0
    for message in messages:
        count: int = 0
        data: str = message[:8]
        ackBit: str = message[8]
        if ackBit == "1":
            badMessage(index)
        checksum: str = message[9]
        dataBits = list(data)
        for bit in dataBits:
            if bit == "1":
                count += 1
            elif bit != "0":
                raise ValueError("Message contains non-binary data")
        if count % 2 == 0 and checksum == "1":
            goodMessage(message)
        if count % 2 == 1 and checksum == "0":
            goodMessage(message)
        else:
            badMessage(index)
        index += 1


def analyzeSingleMessage(message: str):
    pass
