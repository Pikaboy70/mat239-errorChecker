This project aims to simulate a checksum based error checker for 8-bit numbers. The "message" sent is 10-bits long. The 
first 8 contain the data, the 9th is an acknowledgement bit (should always be 0), and the 10th bit is the checksum.

The checksum works like a boolean value to check for an even number of ones in the message data. As in the checksum bit 
will be 1 if the message data contains an even number of ones.
Example: A messages of "00001111" will have a checksum of "1." The final message (including the ack bit) will be 
"0000111101."

A "transmitter" will generate a number of messages. This quantity is supplied by the user. However, if none is given, 
the transmitter will default to 10,000 messages. The quantity is inputted through the `Transmitter.generateMessages()`
method. The method takes one argument called "`count`" of type integer, which is used to determine the number of messages
to generate. "`count`" has a default value of 10,000 if none is given. The transmitter will then create a checksum for 
every generated message and attach it to the end of the message data along with the ack bit.

A "noisy channel" will take each generated message and have a chance to flip bits as they "travel" through. The chance
of a bit flip is a variable called "`noiseLevel`" of type integer with min 0 and max 100. The noise level is used as a 
percent chance to flip a bit. Example: `noiseLevel = 10` means there is a 10% chance for a bit to flip. The noiseLevel can
be set used the `NoisyChannel.setNoiseLevel()` method. It takes one argument "`noise`" of type integer and set the 
noiseLevel to the value of noise. If nothing is passed into the method, it will default to setting a random noise level 
between 0 and 100 inclusive.

A "receiver" will take the garbled messages from the noisy channel and analyze them to determine if they are bad or not.
First the receiver will look at the ack bit. If the bit is 1 the message data is not checked as it is already known to
be a bad message. If the ack bit is 0, the analysis continues. The receiver will then take the first 8 bits of the 
messages and essentially create a new checksum for the data and compare to the checksum bit at the end of the message.
If the two checksums match, the message is assumed to be good and added to a list "`acceptedMessages`." If the two 
checksums do not match, 1 is added to the "`failCount`" variable.

After all messages have been analyzed, the final report will print to the console. The report will first say what noise
level was used. Useful if a random noise level was used instead of supplying one. Next will be the number of bad 
messages detected (value of `failCount`). Next is the number of accepted messages (length of the `acceptedMessages` list). 
The total number of messages generated will be shown after. The final part of the report is the fail rate, which uses 
the `failRate` variable of type float. The fail rate is calculated and then is formatted to be expressed as a percentage
rounded to three decimal places.

How to use the program:

Everything runs from [main.py](main.py) as [errorChecker.py](errorChecker.py) is a class library. The [main.py](main.py)
file is already set up with a `main()`function which runs all necessary methods from the `ErrorChecker` class in the 
correct order. The first line of `main()`will call `Transmitter.generateMessages()`, which can be given any positive 
integer of your choosing or left blank to use the default value. The third line of `main()` will call 
`NoisyChannel.setNoiseLevel()`, which can be given any integer 0 through 100 or left blank to choose random. Only 
`generateMessages()` and `setNoiseLevel()` should have their inputs modified if desired.