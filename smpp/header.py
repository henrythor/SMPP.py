from commands import *
from exception import SMPPException
from struct import unpack

class SMPPHeader:
	"""PDU Header generating class"""
	command=0
	length=0
	status=0
	seq=0
	def __init__(self, **kwargs):
		for variable, value in kwargs.items():
			if variable == "pdu":
				self.parse_pdu(value)
				continue
			elif variable == "command" and isinstance(value, str):
				value = command_a2b[value]
			if not isinstance(value, int):
				raise SMPPException("SMPPHeader: %s, expected int, got %s" % (variable, type(value)))
			vars(self)[variable] = value
	def __repr__(self):
		"""__repr__() -> prepare_pdu()"""
		return self.prepare_pdu()
	def prepare_pdu(self):
		pduh = ""
		pduh += "%.8X" % (self.length + 16) # Command length
		pduh += "%.8X" % self.command  # Command identifier
		pduh += "%.8X" % self.status # Command status
		pduh += "%.8X" % self.seq # Sequence number
		return pduh
	def parse_pdu(self, pdu):
		if not len(pdu) == 16:
			raise SMPPException("SMPPHeader, parse_pdu expected pdu to be 16 octets, not %d" % len(pdu))
		(self.length, self.command, self.status, self.seq) = unpack('!LLLL', pdu)
		return


