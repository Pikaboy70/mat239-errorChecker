# !/usr/bin/env python3
__author__ = "Sam Danforth"
from errorChecker import *
import time


def main():
    startTime = time.time()
    messages = Transmitter.generateMessages()
    messages = Transmitter.creatChecksums(messages)
    NoisyChannel.setNoiseLevel()
    messagesToSend = NoisyChannel.bitFlipper(messages)
    Receiver.analyzeMessages(messagesToSend)
    Evaluator.createReport()
    totalTime = time.time() - startTime
    print(f"\nExecution time: {totalTime:.3f} seconds")


if __name__ == "__main__":
    main()
