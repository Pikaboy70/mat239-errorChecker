#!/usr/bin/env python3
__author__ = "Sam Danforth"


# TODO: Migrate everything to the classes
class ErrorChecker(object):
    def __init__(self):
        pass


class Transmitter(ErrorChecker):
    generatedMessages: list[str] = []

    def __init__(self):
        super().__init__()


class NoisyChannel(ErrorChecker):
    def __init__(self):
        super().__init__()


class Receiver(ErrorChecker):
    def __init__(self):
        super().__init__()
