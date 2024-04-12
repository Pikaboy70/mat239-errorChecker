#!/usr/bin/env python3
__author__ = "Sam Danforth"
from random import randint


class ErrorChecker(object):

    # Generate report for error checking
    @staticmethod
    def calculateSuccess():
        print(f"Noise level used: {NoisyChannel.noiseLevel}%\n")
        print(f"Number of bad messages detected: {Receiver.failCount}")
        print(f"Number of accepted messages: {len(Receiver.acceptedMessages)}")
        print(f"Total number of messages generated: {Transmitter.messageCount}\n")
        failRate: float = Receiver.failCount / Transmitter.messageCount
        print(f"Fail rate: {failRate * 100:.3f}%")


class Transmitter(ErrorChecker):
    generatedMessages: list[str] = []
    preppedMessages: list[str] = []
    messageCount: int = 0

    @staticmethod
    def generateMessages(count: int = 10000):  # Count is the number of messages to generate, default 10,000
        if count < 1:
            raise ValueError("Message count must be positive")
        Transmitter.messageCount = count
        for i in range(0, Transmitter.messageCount):  # Generate inputted number of messages total
            message = randint(0, 255)  # Choose random 8-bit binary number (integer from 0-255)
            # Remove extra characters added by binary conversion and fill with leading zeros
            message = bin(message).replace("0b", "").zfill(8)
            Transmitter.generatedMessages.append(message)  # Add to list of pre-checksum messages
        return Transmitter.generatedMessages

    @staticmethod
    def creatChecksums(messages: list[str]):
        checksum: bool
        for msg in messages:  # Iterate through message list
            checksum = Transmitter.createChecksumSingle(msg)  # Call checksum creation function for each message
            if checksum:
                msg = msg + "01"  # Checksum of 1 for true
            else:
                msg = msg + "00"  # Checksum of 0 for false
            # Also add ack bit of 0 before checksum
            Transmitter.preppedMessages.append(msg)  # Add appended message to a list of known good messages
        return Transmitter.preppedMessages

    @staticmethod
    def createChecksumSingle(message: str):  # Create checksum for a single binary message
        count: int = 0
        checksum: bool
        # Count the number of 1s in the message
        for char in message:
            if char == "1":
                count += 1
            elif char != "0":
                raise ValueError("Message contains non-binary data")
        if count % 2 == 1:  # Basically check if count is even or not
            return False
        elif count % 2 == 0:
            return True

    @staticmethod
    def getNewMessage(index: int):
        message = Transmitter.preppedMessages[index]
        garbledMessage = NoisyChannel.bitFlipperSingle(message, NoisyChannel.noiseLevel)
        return garbledMessage


class NoisyChannel(ErrorChecker):
    noiseLevel: int = 0
    garbledMessages: list[str] = []

    @staticmethod
    def setNoiseLevel(noise: int = randint(0, 100)):
        NoisyChannel.noiseLevel = noise

    @staticmethod
    def bitFlipper(messages: list[str]):
        noiseLevel = NoisyChannel.noiseLevel
        garbledMessages: list[str] = []
        for msg in messages:
            garbledMessage = NoisyChannel.bitFlipperSingle(msg, noiseLevel)  # Run every message through bit flipper
            garbledMessages.append(garbledMessage)  # Add to edited messages list
        return garbledMessages

    @staticmethod
    def bitFlipperSingle(message: str, noiseLevel: int):
        index: int = 0
        charList = list(message)
        for char in charList:
            randomInt = randint(0, 100)
            if randomInt <= noiseLevel:
                if char == "0":  # Change 0 to 1
                    charList[index] = "1"
                elif char == "1":  # Change 1 to 0
                    charList[index] = "0"
                else:
                    raise ValueError("Message contains non-binary data.")
            index += 1
        garbledMessage = ''.join(charList)
        # Join modded character list with empty string to create new message
        return garbledMessage


# TODO: Request new message when bad
class Receiver(ErrorChecker):
    acceptedMessages: list[str] = []
    failCount: int = 0

    @staticmethod
    def goodMessage(message: str):
        Receiver.acceptedMessages.append(message)

    @staticmethod
    def badMessage(index: int):
        Receiver.failCount += 1
        # newMessage = Transmitter.getNewMessage(index)
        # Receiver.analyzeSingleMessage(newMessage, index)

    @staticmethod
    def analyzeMessages(messages: list[str]):
        index: int = 0
        for message in messages:
            Receiver.analyzeSingleMessage(message, index)
            index += 1

    @staticmethod
    def analyzeSingleMessage(message: str, index: int):
        ackBit = message[8]
        if ackBit == "1":
            Receiver.badMessage(index)
            return
        messageData = message[:8]
        checksum = message[9]
        expectedChecksum = Transmitter.createChecksumSingle(messageData)
        if expectedChecksum and checksum == "1":
            Receiver.goodMessage(message)
        elif not expectedChecksum and checksum == "0":
            Receiver.goodMessage(message)
        else:
            Receiver.badMessage(index)
        pass
