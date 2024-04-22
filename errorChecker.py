#!/usr/bin/env python3
__author__ = "Sam Danforth"
from random import randint
from customErrors import ArgumentOutOfRangeError


class ErrorChecker:
    """Static class containing other classes and methods for binary message error checking process"""


class Transmitter(ErrorChecker):
    """Message transmitter/sender, created them and sends them out"""
    generatedMessages: list[str] = []
    preppedMessages: list[str] = []
    messageCount: int = 0

    # Generate list of random 8-bit binary numbers
    # count is the number of messages to generate, 10_000 is used as the default
    @staticmethod
    def generateMessages(count: int = 10000) -> list[str]:
        if count < 1:  # Check for valid input (must be a natural number)
            raise ValueError("Message count must be positive and more than 0")
        Transmitter.messageCount = count  # Update class variable
        for i in range(0, Transmitter.messageCount):
            message = randint(0, 255)  # Choose random 8-bit binary number (integer from 0-255)
            # Remove extra characters added by binary conversion and fill with leading zeros
            message = bin(message).replace("0b", "").zfill(8)
            # Add to list of messages before attaching checksum
            Transmitter.generatedMessages.append(message)
        return Transmitter.generatedMessages

    # Create checksum for list of messages
    @staticmethod
    def creatChecksums(messages: list[str]) -> list[str]:
        checksum: bool
        for msg in messages:  # Iterate through message list
            checksum = Transmitter.createChecksumSingle(msg)  # Call checksum creation function for each message
            # Also add ack bit of 0 before checksum
            if checksum:
                msg = msg + "01"  # Checksum of 1 for true
            else:
                msg = msg + "00"  # Checksum of 0 for false
            Transmitter.preppedMessages.append(msg)  # Add appended message to a list of known good messages
        return Transmitter.preppedMessages

    @staticmethod
    def createChecksumSingle(message: str) -> bool:  # Create checksum for a single binary message
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

    # Called by receiver if it gets a bad message
    @staticmethod
    def getNewMessage(index: int) -> str:
        message: str = Transmitter.preppedMessages[index]  # Get original message
        noise: int = NoisyChannel.noiseLevel
        garbledMessage = NoisyChannel.bitFlipperSingle(message, noise)  # Send back through noisy channel
        return garbledMessage


class NoisyChannel(ErrorChecker):
    """Transmitter sends messages through here, randomly flipping them on their way to destination"""
    noiseLevel: int = 0
    garbledMessages: list[str] = []

    @staticmethod
    def setNoiseLevel(noise: int = randint(0, 50)) -> None:
        if noise is not int:
            raise TypeError("Must pass in an integer")
        if 0 <= noise <= 100:
            NoisyChannel.noiseLevel = noise
        else:
            raise ArgumentOutOfRangeError("Must be between 0 and 100 (inclusive)")

    # Flip bits for list of messages
    @staticmethod
    def bitFlipper(messages: list[str]) -> list[str]:
        noiseLevel = NoisyChannel.noiseLevel
        garbledMessages: list[str] = []
        for msg in messages:
            garbledMessage = NoisyChannel.bitFlipperSingle(msg, noiseLevel)  # Run every message through bit flipper
            garbledMessages.append(garbledMessage)  # Add to garbled messages list
        return garbledMessages

    # Noisy channel simulation for a single message
    @staticmethod
    def bitFlipperSingle(message: str, noiseLevel: int) -> str:
        index: int = 0
        charList = list(message)
        for char in charList:
            randomInt = randint(1, 100)
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


class Receiver(ErrorChecker):
    """Receives messages after going through channel, determines if they are good or bad messages"""

    # Increments counter tracking how many messages were accepted immediately
    @staticmethod
    def goodMessage(message: str, index: int) -> None:
        Evaluator.acceptedMessages += 1
        Evaluator.goodMessages.append(message)
        if Evaluator.falseOrTrueGood(message, index):  # Send message to evaluator
            Evaluator.trueGood.append(message)
        else:
            Evaluator.falseGood.append(message)

    # Gets new message from transmitter, determines if bad again or not
    @staticmethod
    def requestNewMessage(index: int) -> None:
        newMessage: str = Transmitter.getNewMessage(index)
        isGood: bool = Receiver.analyzeSingleMessage(newMessage)
        Evaluator.correctedMessages += 1
        if not isGood:
            Receiver.requestNewMessage(index)

    # Increment counter of how many times a new message was requested
    @staticmethod
    def badMessage(message: str, index: int) -> None:
        Evaluator.badMessages.append(message)
        isBad: bool = Evaluator.falseOrTrueBad(message, index)
        if isBad:
            Evaluator.trueBad.append(message)
            Receiver.requestNewMessage(index)
        else:
            Evaluator.falseBad.append(message)

    # Determine how many messages in a list have accurate checksums
    @staticmethod
    def analyzeMessages(messages: list[str]) -> None:
        index: int = 0
        isGood: bool
        for message in messages:
            isGood = Receiver.analyzeSingleMessage(message)
            if isGood:
                Receiver.goodMessage(message, index)
            else:
                Receiver.badMessage(message, index)
            index += 1

    # Create checksum for message received and compare to the checksum bit of the message
    @staticmethod
    def analyzeSingleMessage(message: str) -> bool:
        ackBit = message[8]
        if ackBit == "1":  # Ack bit should always be 0, message is bad if it's 1
            return False
        messageData = message[:8]  # Get first 8 bits, message content
        checksum = message[9]
        expectedChecksum = Transmitter.createChecksumSingle(messageData)
        if expectedChecksum and checksum == "1":
            return True
        elif not expectedChecksum and checksum == "0":
            return True
        else:
            return False


class Evaluator(ErrorChecker):
    """Evaluates performance of the error checking process"""
    acceptedMessages: int = 0  # Good, including false good
    correctedMessages: int = 0  # Number of times a new message was requested
    goodMessages: list[str] = []  # Includes false good
    trueGood: list[str] = []
    falseGood: list[str] = []
    badMessages: list[str] = []  # Includes false bad
    trueBad: list[str] = []
    falseBad: list[str] = []

    # Generate report of the error checker
    @staticmethod
    def createReport() -> None:
        trueGoodRate: float = (len(Evaluator.trueGood) / Transmitter.messageCount) * 100
        falseGoodRate: float = (len(Evaluator.falseGood) / Transmitter.messageCount) * 100
        trueBadRate: float = (len(Evaluator.trueBad) / Transmitter.messageCount) * 100
        falseBadRate: float = (len(Evaluator.falseBad) / Transmitter.messageCount) * 100
        acceptanceRate: float = (Evaluator.acceptedMessages / Transmitter.messageCount) * 100
        errorDetectionRate: float = (len(Evaluator.badMessages) / Transmitter.messageCount) * 100

        print(f"Noise level used: {NoisyChannel.noiseLevel}%")
        print(f"Total number of messages generated: {Transmitter.messageCount}\n")
        print(f"Number of bad messages detected: {len(Evaluator.badMessages)} ({errorDetectionRate:.2f}%)")
        print(f"Number of requests for new messages: {Evaluator.correctedMessages}\n")
        print(f"Number of true bad: {len(Evaluator.trueBad)} ({trueBadRate:.2f}%)")
        print(f"Number of false bad: {len(Evaluator.falseBad)} ({falseBadRate:.2f}%)\n")
        print(f"Number of accepted messages: {Evaluator.acceptedMessages} ({acceptanceRate:.2f}%)")
        print(f"Number of true good: {len(Evaluator.trueGood)} ({trueGoodRate:.2f}%)")
        print(f"Number of false good {len(Evaluator.falseGood)} ({falseGoodRate:.2f}%)")

    # Checks if good message is a true good message
    @staticmethod
    def falseOrTrueGood(message: str, index: int) -> bool:
        expectedMessage = Transmitter.preppedMessages[index]
        expectedMessage = expectedMessage[:8]
        receivedMessage = message[:8]
        if expectedMessage == receivedMessage:
            return True
        else:
            return False

    # Detects if bad message is an error
    @staticmethod
    def falseOrTrueBad(message: str, index: int) -> bool:
        expectedMessage = Transmitter.preppedMessages[index]
        receivedMessage = message[:8]
        expectedMessage = expectedMessage[:8]
        if expectedMessage == receivedMessage:
            return False
        else:
            return True
