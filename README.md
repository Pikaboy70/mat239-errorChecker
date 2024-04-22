# Overview
This project aims to simulate a checksum based error checker for 8-bit numbers. The "message" sent is 10-bits long. The 
first 8 contain the data, the 9th is an acknowledgement bit (should always be 0), and the 10th bit is the checksum.

The checksum works like a boolean value to check for an even number of ones in the message data. As in the checksum bit 
will be 1 if the message data contains an even number of ones.
Example: A messages of "00001111" will have a checksum of "1." The final message (including the ack bit) will be 
"0000111101."

# Transmitter Class
A "transmitter" will generate a number of messages. This quantity is supplied by the user. However, if none is given, 
the transmitter will default to 10,000 messages. The quantity is inputted through the `Transmitter.generateMessages()`
method. The method takes one argument called "`count`" of type integer, which is used to determine the number of 
messages to generate. `count` must be a natural number, meaning a positive number not including 0. The transmitter will 
then create a checksum for every generated message and attach it to the end of the message data along with the ack bit.

# Noisy Channel Class
A "noisy channel" will take each generated message and have a chance to flip bits as they "travel" through. The chance
of a bit flip is a variable called "`noiseLevel`" of type integer with min 0 and max 100. The noise level is used as a 
percent chance to flip a bit. Example: `noiseLevel = 10` means there is a 10% chance for a bit to flip. The noiseLevel 
can be set used the `NoisyChannel.setNoiseLevel()` method. It takes one argument "`noise`" of type integer (A `
TypeError`will be raised if not an integer) and set the noiseLevel to the value of noise. If nothing is passed into the 
method, it will default to setting a random noise level between 0 and 50 inclusive. An `ArgumentOutOfRangeError` will be
raised if and integer is passes in that is either negative or is greater than 100.

# Receiver Class
A "receiver" will take the garbled messages from the noisy channel and analyze them to determine if they are bad or not.
First the receiver will look at the ack bit. If the bit is 1 the message data is not checked as it is already known to
be a bad message. If the ack bit is 0, the analysis continues. The receiver will then take the first 8 bits of the 
messages and essentially create a new checksum for the data and compare to the checksum bit at the end of the message.
If the two checksums match, the message is assumed to be good and added to a list `goodMessages` and increments an `
acceptedMessages` counter. If the two checksums do not match, 1 is added to the list `badMessages` and a new message 
will be requested from the transmitter. The index of the bad message is saved to use to retrieve the original message 
saved in the transmitter's`preppedMessages` list, send it through the noisy channel again, and determine if the message 
is bad or not. A new message will keep getting requested until a good one is received and incrementing the 
`correctedMessages` counter. This can cause a `RecursionError` when using high noise levels.

# Evaluator Class

Whether a message is determined to be good or bad, it will be sent to the "evaluator" to assess the performance of the
error checker. Two methods are used for this process `falseOrTrueGood` and `falseOrTrueBad`. Both of these methods will 
take the message and the index to compare the received message against the expected message from the 
`Transmitter.preppedMessages` list to determine if the messages good or bad status was determined accurately. Example:
A message that is originally generated as "11000000" has an even number of ones meaning a checksum of "1" will be 
attached making the full message "1100000001". Say the message goes through the noisy channel and exactly two bits get
flipped. For the example the garbled message will now be "1010000001", which still has an even number of ones causing
the receiver to generate a checksum of "1" which will match the checksum bit at the end and will be determined to be a
good message. The evaluator will check the garbled message and the original message to see that they are not matching
and will add this message to `falseGood`.

## Final Report

At the end of the program execution, a report will be printed from this class
which will first display the noise level and total message count. It will then show the number of bad messages detected
along with how many are true bad and how many are false bad. Then a section for the number of accepted messages along
with how many are true good and how many are false good. All counts from total bad messages until the end will also have
the number expressed as a percentage of the total number of messages to the right of the actual count.

### How to use the program:

Everything runs from [main.py](main.py), [errorChecker.py](errorChecker.py) is a class library, and 
[errorChecker.py](errorChecker.py) contains a custom `ArgumentOutOfRangeError` subclassed from the `Exception` class. 
The [main.py](main.py) file is already set up with a `main()`function which runs all necessary methods from the 
`ErrorChecker` class in the correct order. The first line of `main()`will call `Transmitter.generateMessages()`, which 
can be given any positive integer of your choosing or left blank to use the default value. The third line of `main()`
will call `NoisyChannel.setNoiseLevel()`, which can be given any integer 0 through 100 or left blank to choose random. 
Only `generateMessages()` and `setNoiseLevel()` should have their arguments modified if desired. After the error checker
has completed execution, a final line will be printed to the console that says how long execution took in seconds.