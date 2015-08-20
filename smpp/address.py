from exception import SMPPException
from binascii import b2a_hex

class SMPPAddress:
	def __init__(self, address):
		self.ton = 0x00
		self.npi = 0x00

		if not isinstance(address, str):
			raise SMPPException("SMPPAddress: Expected a string, got %s" % type(address))
		if not address.isdigit() and address.isalnum():
			self.ton = 0x05
		if len(address) == 0 or not address[-1] == '\0':
			address += '\0'
		self.address = address
	def __repr__(self):
		return "%.2X%.2X%s" % (self.ton, self.npi, b2a_hex(self.address))
	def set_ton(self, ton):
		"""0x00: Unknown
		0x01: International
		0x02: National
		0x03: Network specific
		0x04: Subscriber number
		0x05: Alphanumeric
		0x06: Abbreviated"""
		self.ton = ton
	def set_npi(self, npi):
		"""0x00: Unknown
		0x01: ISDN (E163/E164)
		0x03: Data (X.121)
		0x04: Tele (F.69)
		0x06: Land Mobile (E.212)
		0x08: National
		0x09: Private
		0x0A: ERMES
		0x0E: Internet (IP)
		0x12: WAP Client Id (to be defined by WAP Forum)"""
		self.npi = npi


