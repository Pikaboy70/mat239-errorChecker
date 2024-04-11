# !/usr/bin/env python3
__author__ = "Sam Danforth"
import noisyChannel
import receiver
import transmitter


# TODO: Create ErrorChecker class if time permits
def main():
    nums: list[str] = transmitter.generateMessages()
    nums = transmitter.createChecksums(nums)
    garbledMessages = noisyChannel.bitFlipper(nums)
    goodMessage = receiver.analyzeMessages(garbledMessages)
    print(f"Good message? {goodMessage}")


if __name__ == "__main__":
    main()  # Do not run, might return something but will be far from correct
