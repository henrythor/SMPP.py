from keepalive import SMPPKeepAlive
from error import SMPPError
from header import SMPPHeader
from parameters import SMPPParameters
from address import SMPPAddress
import socket
import threading
from struct import unpack
from commands import *
from binascii import b2a_hex, a2b_hex
from time import sleep

class SMPP:
	"""A Limited Synchronous SMPP API designed for ease of use"""
	CLOSED=0
	OPEN=1
	BOUND_TX=2
	BOUND_RX=3
	BOUND_TRX=4
	BIND_TX=BOUND_TX
	BIND_RX=BOUND_RX
	BIND_TRX=BOUND_TRX

	def __init__(self, host, port, keepalive=True, debug=True):
		if isinstance(port, str):
			port = int(port)
		self.host=host
		self.port=port
		self._socket=None
		self._socket_lock=threading.Lock()
		self.state=self.CLOSED
		self.outseq=0
		self.debug=debug
		self._connect()
		self._keepalive_thread = None
		if keepalive:
			self._keepalive_thread = SMPPKeepAlive(self)
			self._keepalive_thread.start()

	def _keepalive(self):
		ret = None
		if self.state >= self.BOUND_TX:
			if self.debug:
				print "Sending keepalive"
			ret = self.enquire_link()
		return ret

	def _takesocket(self):
		self._socket_lock.acquire()
		# We have the lock now
		return self._socket

	def _releasesocket(self):
		self._socket_lock.release()
		sleep(0.0001) # Yield to thread scheduler
		return None

	def _disconnect(self):
		if self.state >= self.BOUND_TX:
			self._unbind()
		self._socket.close()
		self.state=self.CLOSED

	def _connect(self):
		if not self.state == self.CLOSED:
			raise SMPPException("Attempting to connect out of turn!")

		self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
		self._socket.settimeout(30.0)
		try:
			self._socket.connect((self.host, self.port))
		except socket.error:
			raise
		state=self.OPEN

	def _send_raw(self, data):
		# Verify state is sane (socket open, and we're bound)
		sock = self._takesocket() # It'll be released by _sock_read
		if self.debug:
			cmd = unpack("!L", data[4:8])[0]
			print "Sending %s.." % (command_b2a[cmd])
		if self.debug:
			print ">> %s" % b2a_hex(data)
		try:
			sock.sendall(data)
		except Exception, e:
			if self.debug:
				print "Got error writing to socket, reconnecting"
			oldstate = self.state
			self.state = self.CLOSED
			self._connect()
			sock = self._releasesocket()
			self.rebind(oldstate)
			raise
		return sock

	def _sock_read(self, sock, length):
		defer = None
		try:
			defer = sock.recv(length)
		except socket.timeout:
			if self.debug:
				print "Reading timed out"
			defer = ""
		except Exception, e:
			if self.debug:
				print "Got error reading from socket, reconnecting %s" % e
			oldstate = self.state
			self.state = self.CLOSED
			self._connect()
			sock = self._releasesocket() # Acquired in _send_raw
			self._rebind(oldstate)
		return defer

	def _read_resp(self, sock, expect_cmd, expect_seq):
		rawpdu = ""

		if self.debug:
			print "Waiting for %s response" % response_b2a[expect_cmd]

		while len(rawpdu) < 4:
			rawpdu += self._sock_read(sock, 4-len(rawpdu)) # Get the length
		length = unpack('!L', rawpdu)[0]
		left = length - 4 # We've already read 4 bytes of the PDU

		tries = 10
		while left > 0 and tries > 0:
			buf = self._sock_read(sock, left)
			left -= len(buf)
			rawpdu += buf
			tries -= 1	

		if not len(rawpdu) == length:
			raise SMPPException("Error in reading response for %s" % response_b2a[expect_cmd])

		sock = self._releasesocket() # Acquired by _send_raw

		if self.debug:
			print "<< %s" % b2a_hex(rawpdu)

		header = SMPPHeader(pdu = rawpdu[0:16])
		params = None
		if header.length > 16:
			params = SMPPParameters(header.command, pdu = rawpdu[16:])

		if self.debug and header.command == GENERIC_NACK_RESP:
			print "Got a generic NACK. Our request was probably malformed!"
		if not header.command == expect_cmd:
			raise SMPPException("Received %s response out of turn", response_b2a[command])
		if not header.seq == expect_seq:
			raise SMPPException("Received a reply I didn't expect. Expected seq: %d, but got %d" % (expect_seq, header.seq))

		if self.debug:
			print "%s response: %s" % (response_b2a[expect_cmd], SMPPError(header.status))
		return (header, params)

	def _get_outseq(self):
		self.outseq += 1
		if self.outseq > 0xFFFFFFFF:
			self.outseq = 1 # Roll over, we have a maximum of 32 bits for seq
		return self.outseq

	def _read_cmd(self):
		rawpdu = ""
		while len(rawpdu) < 4:
			if self.debug:
				print "Waiting for command.."
			sock = self._takesocket() 
			rawpdu += self._sock_read(sock, 4-len(rawpdu)) # Get the length
			print rawpdu
			sock = self._releasesocket() # Acquired earlier
		length = unpack('!L', rawpdu)[0]
		left = length - len(rawpdu) # We've already read 4 bytes of the PDU
		if self.debug:
			print "We've got %d more bytes to read.." % left

		tries = 10
		while left > 0 and tries > 0:
			sock = self._takesocket() 
			buf = self._sock_read(sock, left)
			sock = self._releasesocket() # Acquired earlier
			left -= len(buf)
			rawpdu += buf
			tries -= 1	


		if not len(rawpdu) == length:
			raise SMPPException("Error in reading command, got %d octets, expected %d" % (len(rawpdu), length))

		if self.debug:
			print "<< %s" % b2a_hex(rawpdu)

		header = SMPPHeader(pdu = rawpdu[0:16])
		params = None
		if len(rawpdu) > 16:
			params = SMPPParameters(header.command, pdu = rawpdu[16:])

		if self.debug:
			print "Got command %s" % command_b2a[header.command]
		return (header, params)

	def send_resp(self, header, params):
		"""Send response"""
		if not isinstance(params, SMPPParameters):
			raise SMPPException("send_resp: params should be of type SMPPParameters")
		if not isinstance(header, SMPPHeader):
			raise SMPPExceptiuon("send_resp: header should be of type SMPPHeader")
		if not params.command == header.command:
			raise SMPPException("send_resp: params not initialized properly")

		pdu = "%s%s" % (header, params)

		if self.debug:
			print "Sending response to %s.." % response_b2a(header.command)
		if self.debug:
			print ">> %s" % pdu

		sock = self._takesocket() # It'll be released by _sock_read
		try:
			sock.sendall(a2b_hex(pdu))
		except Exception, e:
			if self.debug:
				print "Got error writing to socket, reconnecting"
			oldstate = self.state
			self.state = self.CLOSED
			self._connect()
			sock = self._releasesocket()
			self.rebind(oldstate)
			raise
		sock = self._releasesocket()

	def bind_transmitter(self, user, passw, desc):
		return self.bind(self.BIND_TX, user, passw, desc)
	def bind_receiver(self, user, passw, desc):
		return self.bind(self.BIND_RX, user, passw, desc)
	def bind_transceiver(self, user, passw, desc):
		return self.bind(self.BIND_TRX, user, passw, desc)

	def bind(self, bind_type, user, passw, desc):
		"""Bind as receiver, transmitter, or tranceiver"""
		command = None
		tostate = None
		if self.state >= self.BOUND_TX:
			raise SMPPException("Already bound!")

		if bind_type == self.BIND_TX:
			command = 'bind_transmitter'
			tostate = self.BOUND_TX
		elif bind_type == self.BIND_RX:
			command = 'bind_receiver'
			tostate = self.BOUND_RX
		elif bind_type == self.BINT_TRX:
			command = 'bind_transceiver'
			tostate = self.BOUND_TRX

		if not command:
			raise SMPPException("Unknown bind type")

		params = SMPPParameters(command, system_id = user, password = passw, system_type = desc)

		seq=self._get_outseq()
		header = SMPPHeader(length = params.length(), command = command, seq = seq)
		pdu = "%s%s" % (header, params)

		sock = self._send_raw(a2b_hex(pdu))
		(rheader, rparams) = self._read_resp(sock, response_a2b[command], seq)
		if not rheader.status == SMPPError.ESME_ROK:
			raise SMPPException(SMPPError(rheader.status))
		self.state = tostate
		self.bind_params = params
		self.bindtype = command

	def _rebind(self, state):
		command = ""
		if state == self.BOUND_TX:
			command = "bind_transmitter"
		elif state == self.BOUND_RX:
			command = "bind_receiver"
		elif state == self.BOUND_TRX:
			command = "bind_transceiver"
		else:
			raise SMPPException("SMPP: _rebind: unknown state!")
		if not self.bind_params:
			raise SMPPException("SMPP: _rebind couldn't find bind parameters")
		seq = self._get_outseq()
		header = SMPPHeader(length = self.bind_params.length(), command = command, seq = seq)
		pdu = "%s%s" % (header, self.bind_params)
		sock = self._send_raw(pdu)
		(rheader, rparams) = self._read_resp(sock, response_a2b[command], seq)
		if not rheader.status == SMPPError.ESME_ROK:
			raise SMPPException(SMPPError(rheader.status))
		self.state = state

	def unbind(self):
		"""Unbind from server"""
		# Do stuff
		if not self.state >= self.BOUND_TX:
			raise SMPPException("unbind called out of turn!")
		seq = self._get_outseq()
		pdu = "%s" % SMPPHeader(length = 0, command = 'unbind', seq = seq)
		sock = self._send_raw(a2b_hex(pdu))
		(rheader, rparams) = self._read_resp(sock, response_a2b['unbind'], seq)
		self.state = self.OPEN
		status = rheader.status

		if not status == SMPPError.ESME_ROK:
			raise SMPPException(SMPPError(status))
		return self._disconnect()

	def command(self, command, params):
		"""Send arbitrary command"""
		if not isinstance(params, SMPPParameters):
			raise SMPPException("%s: params should be of type SMPPParameters" % command)
		if not params.command == command_a2b[command]:
			raise SMPPException("%s: params not initialized properly" % command)
		seq = self._get_outseq()
		header = SMPPHeader(length = params.length(), command = command, seq = seq)

		pdu = "%s%s" % (header, params)

		s = self._send_raw(a2b_hex(pdu))
		(rheader, rparams) = self._read_resp(s, response_a2b[command], seq) # Read delivery info
		return (rheader, rparams)

	def send_ota(self, wbxml, sender, recipient):
		"""Wrapper for data_sm"""
		success = False
		if isinstance(sender, str):
			sender = SMPPAddress(sender)
		if isinstance(recipient, str):
			recipient = SMPPAddress(recipient)

		params = SMPPParameters(DATA_SM, source = sender, \
			destination = recipient, \
			esm_class = 0x02, \
			data_coding = 0x04)
		params.add_optional(message_payload = a2b_hex(wbxml), \
			source_port = 2948, \
			destination_port = 2948)
		(rheader, rparams) = self.data_sm(params)
		if rheader.status == SMPPError.ESME_ROK:
			return { 'error': 0, 'success': 1, 'msg': 'Success' }
		else:
			message = "%s" % SMPPError(rheader.status)
			optionals = rparams.get_optionals()
			if len(optionals) > 0:
				message = "status: '%s', delivery_failure_reason: '%.2X', network_error_code: '%.6X', additional_status_info_text: '%s', dpf_result: '%.2X'" % (SMPPError(rheader.status), optionals.get(SMPPParameters.OPT_DELIVERY_FAILURE_REASON, ""), optionals.get(SMPPParameters.OPT_NETWORK_ERROR_CODE, ""), optionals.get(SMPPParameters.OPT_ADDITIONAL_STATUS_INFO_TEXT, ""), optionals.get(SMPPParameters.OPT_DPF_RESULT, ""))
			return { 'error': 1, 'success': 0, 'msg': message }

	def listen(self, listener):
		"""Method to listen for commands and performing actions."""

		if not isinstance(listener, SMPPListener):
			raise SMPPException("listen(): listener should be an instance of SMPPListener")
		while 1:
			if listener.stop = True:
				break
			# DATA_SM
			# DELIVER_SM
			# We respond with DATA_SM_RESP and DELIVER_SM_RESP
			(header, params) = self._read_cmd()
			if header.command == DELIVER_SM:
				if self.debug:
					print "We got a DELIVER_SM"
					print "From %s to %s" % (params.source.address, params.destination.address)
					print "Message: %s" % params.short_message
				(rheader, rparams) = listener.deliver_sm(header, params)
			if header.command == DATA_SM:
				if self.debug:
					print "We got a DATA_SM"
					print "From %s to %s" % (params.source.address, params.destination.address)
				(rheader, rparams) = listener.data_sm(header, params)

			self.send_resp(rheader, rparams)

	def enquire_link(self):
		"""Confidence check of the communication path between an ESME and an SMSC"""
		seq = self._get_outseq()
		pdu = "%s" % SMPPHeader(length = 0, command = 'enquire_link', seq = seq)
		sock = self._send_raw(a2b_hex(pdu))
		(rheader, rparams) = self._read_resp(sock, response_a2b['enquire_link'], seq)

		if rheader.status == SMPPError.ESME_ROK:
			return True
		else:
			return False

	def data_sm(self, params):
		"""DATA_SM wrapper for command()
		params: SMPPParameters(DATA_SM) object."""
		return self.command('data_sm', params)

	def query_sm(self, params):
		"""QUERY_SM wrapper for command()
		params: SMPPParameters(QUERY_SM) object."""
		return self.command('query_sm', params)

	def submit_sm(self, params):
		"""SUBMIT_SM wrapper for command()
		params: SMPPParameters(SUBMIT_SM) object."""
		return self.command('submit_sm', params)

	def replace_sm(self, params):
		"""REPLACE_SM wrapper for command()
		params: SMPPParameters(REPLACE_SM) object."""
		return self.command('replace_sm', params)

	def cancel_sm(self, params):
		"""CANCEL_SM wrapper for command()
		params: SMPPParameters(CANCEL_SM) object."""
		return self.command('cancel_sm', params)

	def submit_multi(self, params):
		"""SUBMIT_MULTI wrapper for command()
		params: SMPPParameters object."""
		return self.command('submit_multi', params)


