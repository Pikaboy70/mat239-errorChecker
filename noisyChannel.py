#!/usr/bin/env python3
__author__ = "Sam Danforth"
from random import randint


# Take binary number and randomly flip bits to its opposite (0->1, 1->0)
def bitFlipper(message):
    charList = list(message)
    noiseLevel = randint(0, 100)  # Generate random percentage to be used as flip probability
    print(f"Probability of bit flip: {noiseLevel}%")
    for char in charList:
        index = charList.index(char)
        if randint(0, 100) <= noiseLevel:
            if char == "0":
                charList[index] = "1"
            elif char == "1":
                charList[index] = "0"
            else:
                raise ValueError("Message contains non-binary data.")
    garbledMessage = ''.join(charList)
    return garbledMessage
