#!/usr/bin/env python3
__author__ = "Sam Danforth"
from random import randint
import receiver


# TODO: Migrate all functions to NoisyChannel class
# Take binary number and randomly flip bits to its opposite (0->1, 1->0)
def bitFlipper(messages: list[str]):
    noiseLevel = randint(0, 100)
    receiver.setNoiseLevel(noiseLevel)
    garbledMessages: list[str] = []
    # print(f"Probability of bit flip: {noiseLevel}%")
    for msg in messages:
        garbledMessage = bitFlipperSingle(msg, noiseLevel)
        # Join modded character list with empty string to create new message
        garbledMessages.append(garbledMessage)  # Add to edited messages list
    return garbledMessages


# Noisy channel simulator for a single message
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
    return garbledMessage
