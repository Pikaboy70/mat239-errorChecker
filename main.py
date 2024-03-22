# !/usr/bin/env python3
__author__ = "Sam Danforth"
import noisyChannel
import receiver
import transmitter


def main():
    num = transmitter.generateMessage()
    checksum, num = transmitter.createChecksum(num)
    message = transmitter.prepareMessage(num, checksum)
    print(f"Original message: {message}")
    garbledMessage = noisyChannel.bitFlipper(message)
    print(f"Message received: {garbledMessage}")
    goodMessage = receiver.analyzeMessage(garbledMessage)
    print(f"Good message? {goodMessage}")


if __name__ == "__main__":
    main()
