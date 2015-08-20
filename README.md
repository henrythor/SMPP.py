#SMPP.py

A synchronous SMPP library written in Python

I wrote this library a while back when I needed a library for contacting SMPP
services. At that point none of the available libraries were good enough for
my use though that might have changed by now. It's based on SMPP v3.4 and
major parts for sending SMPP messages are done, if I remember correctly.

The receiving stuff wasn't finished, and since I don't have access to an SMPP
server at the moment, I figure I'll put it out there and let someone working
in telecom in need of a synchronous library for SMPP figure it out.

CHANGELOG:
Version 0.1 - Henry Baldursson
* Initial version
  * Supports binding, sending DATA_SM, SUBMIT_SM, ENQUIRE_LINK, and reading relevant responses. 
  * KeepAlive
  * All mandatory- and optional parameters
  * Parsing
  * Rudimentary polling for commands.

EXAMPLES:
How to send data to a specific port:
```
	from smpp import *
	smpp=SMPP("host", 2775)
	smpp.bind_transmitter("user", "pass", "OTA")
	sender = SMPPAddress("Telecom")
	recipient = SMPPAddress("111222333444)

	params = SMPPParameters(DATA_SM, source = sender, \
	destination = recipient, \
	esm_class = 0x02, \
	data_coding = 0x04)
	params.add_optional(message_payload = data, \
	source_port = 2948, \
	destination_port = 2948)
	(rheader, rparams) = smpp.data_sm(params)
	smpp.unbind()
	return rheader.status
```

How to listen for commands (to be extended):
```
	from smpp import *
	smpp = SMPP('smsc', 2775) #, keepalive=False)
	smpp.bind_receiver('user', 'pass', 'VAS')
	smpp.listen()
	smpp.unbind()
```
