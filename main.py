# !/usr/bin/env python3
__author__ = "Sam Danforth"
from errorChecker import *


def main():
    messages = Transmitter.generateMessages()
    messages = Transmitter.creatChecksums(messages)
    NoisyChannel.setNoiseLevel()
    messagesToSend = NoisyChannel.bitFlipper(messages)
    Receiver.analyzeMessages(messagesToSend)
    ErrorChecker.calculateSuccess()


if __name__ == "__main__":
    main()
