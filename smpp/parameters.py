from commands import *
from exception import SMPPException
from address import SMPPAddress
from binascii import b2a_hex, a2b_hex
from struct import unpack
from cStringIO import StringIO

class SMPPParameters:
	"""PDU generating class"""
	# A list of mandatory parameters and their initial values:
	system_id=""
	password=""
	system_type="ESME"
	service_type=""
	interface_version=0x34
	address=SMPPAddress("")
	source=SMPPAddress("")
	destination=SMPPAddress("")
	esm_class=0
	protocol_id=0
	priority_flag=0
	schedule_delivery_time=0
	validity_period=0
	registered_delivery=0
	replace_if_present_flag=0
	data_coding=0
	sm_default_msg_id=1
	sm_length=0
	short_message=""
	message_id=""
	number_of_dests=0
	dest_flag=0
	no_unsuccess=0
	dl_name=""
	message_state=0x07

	# A list of tag codes for the optional parameters:
	OPT_DEST_ADDR_SUBUNIT = 0x0005
	OPT_DEST_NETWORK_TYPE = 0x0006
	OPT_DEST_BEARER_TYPE = 0x0007
	OPT_DEST_TELEMATICS_ID = 0x0008
	OPT_SOURCE_ADDR_SUBUNIT = 0x000D
	OPT_SOURCE_NETWORK_TYPE = 0x000E
	OPT_SOURCE_BEARER_TYPE = 0x000F
	OPT_SOURCE_TELEMATICS_ID = 0x0010
	OPT_QOS_TIME_TO_LIVE = 0x0017
	OPT_PAYLOAD_TYPE = 0x0019
	OPT_ADDITIONAL_STATUS_INFO_TEXT = 0x001D
	OPT_RECEIPTED_MESSAGE_ID = 0x001E
	OPT_MS_MSG_WAIT_FACILITIES = 0x0030
	OPT_PRIVACY_INDICATOR = 0x0201
	OPT_SOURCE_SUBADDRESS = 0x0202
	OPT_DEST_SUBADDRESS = 0x0203
	OPT_USER_MESSAGE_REFERENCE = 0x0204
	OPT_USER_RESPONSE_CODE = 0x0205
	OPT_SOURCE_PORT = 0x020A
	OPT_DESTINATION_PORT = 0x020B
	OPT_SAR_MSG_REF_NUM = 0x020C
	OPT_LANGUAGE_INDICATOR = 0x020D
	OPT_SAR_TOTAL_SEGMENTS = 0x020E
	OPT_SAR_SEGMENT_SEQNUM = 0x020F
	OPT_SC_INTERFACE_VERSION = 0x0210
	OPT_CALLBACK_NUM_PRES_IND = 0x0302
	OPT_CALLBACK_NUM_ATAG = 0x0303
	OPT_NUMBER_OF_MESSAGES = 0x0304
	OPT_CALLBACK_NUM = 0x0381
	OPT_DPF_RESULT = 0x0420
	OPT_SET_DPF = 0x0421
	OPT_MS_AVAILABILITY_STATUS = 0x0422
	OPT_NETWORK_ERROR_CODE = 0x0423
	OPT_MESSAGE_PAYLOAD = 0x0424
	OPT_DELIVERY_FAILURE_REASON = 0x0425
	OPT_MORE_MESSAGES_TO_SEND = 0x0426
	OPT_MESSAGE_STATE = 0x0427
	OPT_USSD_SERVICE_OP = 0x0501
	OPT_DISPLAY_TIME = 0x1201
	OPT_SMS_SIGNAL = 0x1203
	OPT_MS_VALIDITY = 0x1204
	OPT_ALERT_ON_MESSAGE_DELIVERY = 0x130C
	OPT_ITS_REPLY_TYPE = 0x1380
	OPT_ITS_SESSION_INFO = 0x1383

	# This dict is here to turn object variable names in **kwargs into codes
	_optional_tag = {
		'dest_addr_subunit': OPT_DEST_ADDR_SUBUNIT,
		'dest_network_type': OPT_DEST_NETWORK_TYPE,
		'dest_bearer_type': OPT_DEST_BEARER_TYPE,
		'dest_telematics_id': OPT_DEST_TELEMATICS_ID,
		'source_addr_subunit': OPT_SOURCE_ADDR_SUBUNIT,
		'source_network_type': OPT_SOURCE_NETWORK_TYPE,
		'source_bearer_type': OPT_SOURCE_BEARER_TYPE,
		'source_telematics_id': OPT_SOURCE_TELEMATICS_ID,
		'qos_time_to_live': OPT_QOS_TIME_TO_LIVE,
		'payload_type': OPT_PAYLOAD_TYPE,
		'additional_status_info_text': OPT_ADDITIONAL_STATUS_INFO_TEXT,
		'receipted_message_id': OPT_RECEIPTED_MESSAGE_ID,
		'ms_msg_wait_facilities': OPT_MS_MSG_WAIT_FACILITIES,
		'privacy_indicator': OPT_PRIVACY_INDICATOR,
		'source_subaddress': OPT_SOURCE_SUBADDRESS,
		'dest_subaddress': OPT_DEST_SUBADDRESS,
		'user_message_reference': OPT_USER_MESSAGE_REFERENCE,
		'user_response_code': OPT_USER_RESPONSE_CODE,
		'source_port': OPT_SOURCE_PORT,
		'destination_port': OPT_DESTINATION_PORT,
		'sar_msg_ref_num': OPT_SAR_MSG_REF_NUM,
		'language_indicator': OPT_LANGUAGE_INDICATOR,
		'sar_total_segments': OPT_SAR_TOTAL_SEGMENTS,
		'sar_segment_seqnum': OPT_SAR_SEGMENT_SEQNUM,
		'SC_interface_version': OPT_SC_INTERFACE_VERSION,
		'callback_num_pres_ind': OPT_CALLBACK_NUM_PRES_IND,
		'callback_num_atag': OPT_CALLBACK_NUM_ATAG,
		'number_of_messages': OPT_NUMBER_OF_MESSAGES,
		'callback_num': OPT_CALLBACK_NUM,
		'dpf_result': OPT_DPF_RESULT,
		'set_dpf': OPT_SET_DPF,
		'ms_availability_status': OPT_MS_AVAILABILITY_STATUS,
		'network_error_code': OPT_NETWORK_ERROR_CODE,
		'message_payload': OPT_MESSAGE_PAYLOAD,
		'delivery_failure_reason': OPT_DELIVERY_FAILURE_REASON,
		'more_messages_to_send': OPT_MORE_MESSAGES_TO_SEND,
		'message_state': OPT_MESSAGE_STATE,
		'ussd_service_op': OPT_USSD_SERVICE_OP,
		'display_time': OPT_DISPLAY_TIME,
		'sms_signal': OPT_SMS_SIGNAL,
		'ms_validity': OPT_MS_VALIDITY,
		'alert_on_message_delivery': OPT_ALERT_ON_MESSAGE_DELIVERY,
		'its_reply_type': OPT_ITS_REPLY_TYPE,
		'its_session_info': OPT_ITS_SESSION_INFO
	}

	# _opt_parm_sz is the size of the optional parameters value in octets, 'S' for CString
	_opt_parm_sz = {
		OPT_DEST_ADDR_SUBUNIT: 1,
		OPT_DEST_NETWORK_TYPE: 1,
		OPT_DEST_BEARER_TYPE: 1,
		OPT_DEST_TELEMATICS_ID: 2,
		OPT_SOURCE_ADDR_SUBUNIT: 1,
		OPT_SOURCE_NETWORK_TYPE: 1,
		OPT_SOURCE_BEARER_TYPE: 1,
		OPT_SOURCE_TELEMATICS_ID: 1,
		OPT_QOS_TIME_TO_LIVE: 4,
		OPT_PAYLOAD_TYPE: 1,
		OPT_ADDITIONAL_STATUS_INFO_TEXT: 'S',
		OPT_RECEIPTED_MESSAGE_ID: 'S',
		OPT_MS_MSG_WAIT_FACILITIES: 1,
		OPT_PRIVACY_INDICATOR: 1,
		OPT_SOURCE_SUBADDRESS: 'S',
		OPT_DEST_SUBADDRESS: 'S',
		OPT_USER_MESSAGE_REFERENCE: 2,
		OPT_USER_RESPONSE_CODE: 1,
		OPT_SOURCE_PORT: 2,
		OPT_DESTINATION_PORT: 2,
		OPT_SAR_MSG_REF_NUM: 2,
		OPT_LANGUAGE_INDICATOR: 1,
		OPT_SAR_TOTAL_SEGMENTS: 1,
		OPT_SAR_SEGMENT_SEQNUM: 1,
		OPT_SC_INTERFACE_VERSION: 1,
		OPT_CALLBACK_NUM_PRES_IND: 1,
		OPT_CALLBACK_NUM_ATAG: 'S',
		OPT_NUMBER_OF_MESSAGES: 1,
		OPT_CALLBACK_NUM: 'S',
		OPT_DPF_RESULT: 1,
		OPT_SET_DPF: 1,
		OPT_MS_AVAILABILITY_STATUS: 1,
		OPT_NETWORK_ERROR_CODE: 3,
		OPT_MESSAGE_PAYLOAD: 'S',
		OPT_DELIVERY_FAILURE_REASON: 1,
		OPT_MORE_MESSAGES_TO_SEND: 1,
		OPT_MESSAGE_STATE: 1,
		OPT_USSD_SERVICE_OP: 1,
		OPT_DISPLAY_TIME: 1,
		OPT_SMS_SIGNAL: 2,
		OPT_MS_VALIDITY: 1,
		OPT_ALERT_ON_MESSAGE_DELIVERY: 0,
		OPT_ITS_REPLY_TYPE: 1,
		OPT_ITS_SESSION_INFO: 2,
	}

	_optionals = {}

	def __init__(self, command, **kwargs):
		if isinstance(command, str):
			command = command_a2b[command]
		self.command = command
		self._determine_optionals()
		for variable, value in kwargs.items():
			if variable == "pdu":
				self.parse_pdu(value)
				continue
			elif variable == "source" or variable == "destination" or variable == "address":
				if not isinstance(value, SMPPAddress):
					raise SMPPException("SMPPParameters expects addresses to be of type SMPPAddress")
			vars(self)[variable] = value

	def _determine_optionals(self):
		# Lists which optional parameters are allowed for the given command/response. Default is none.
		if self.command == SUBMIT_SM:
			self._optionals_allowed = [self.OPT_USER_MESSAGE_REFERENCE, self.OPT_SOURCE_PORT, self.OPT_SOURCE_ADDR_SUBUNIT, self.OPT_DESTINATION_PORT, self.OPT_DEST_ADDR_SUBUNIT, self.OPT_SAR_MSG_REF_NUM, self.OPT_SAR_TOTAL_SEGMENTS, self.OPT_SAR_SEGMENT_SEQNUM, self.OPT_MORE_MESSAGES_TO_SEND, self.OPT_PAYLOAD_TYPE, self.OPT_MESSAGE_PAYLOAD, self.OPT_PRIVACY_INDICATOR, self.OPT_CALLBACK_NUM, self.OPT_CALLBACK_NUM_PRES_IND, self.OPT_CALLBACK_NUM_ATAG, self.OPT_SOURCE_SUBADDRESS, self.OPT_DEST_SUBADDRESS, self.OPT_USER_RESPONSE_CODE, self.OPT_DISPLAY_TIME, self.OPT_SMS_SIGNAL, self.OPT_MS_VALIDITY, self.OPT_MS_MSG_WAIT_FACILITIES, self.OPT_NUMBER_OF_MESSAGES, self.OPT_ALERT_ON_MESSAGE_DELIVERY, self.OPT_LANGUAGE_INDICATOR, self.OPT_ITS_REPLY_TYPE, self.OPT_ITS_SESSION_INFO, self.OPT_USSD_SERVICE_OP]
		elif self.command == DATA_SM:
			self._optionals_allowed = [self.OPT_SOURCE_PORT, self.OPT_SOURCE_ADDR_SUBUNIT, self.OPT_SOURCE_NETWORK_TYPE, self.OPT_SOURCE_BEARER_TYPE, self.OPT_SOURCE_TELEMATICS_ID, self.OPT_DESTINATION_PORT, self.OPT_DEST_ADDR_SUBUNIT, self.OPT_DEST_NETWORK_TYPE, self.OPT_DEST_BEARER_TYPE, self.OPT_DEST_TELEMATICS_ID, self.OPT_SAR_MSG_REF_NUM, self.OPT_SAR_TOTAL_SEGMENTS, self.OPT_SAR_SEGMENT_SEQNUM, self.OPT_MORE_MESSAGES_TO_SEND, self.OPT_QOS_TIME_TO_LIVE, self.OPT_PAYLOAD_TYPE, self.OPT_MESSAGE_PAYLOAD, self.OPT_SET_DPF, self.OPT_RECEIPTED_MESSAGE_ID, self.OPT_MESSAGE_STATE, self.OPT_NETWORK_ERROR_CODE, self.OPT_USER_MESSAGE_REFERENCE, self.OPT_PRIVACY_INDICATOR, self.OPT_CALLBACK_NUM, self.OPT_CALLBACK_NUM_PRES_IND, self.OPT_CALLBACK_NUM_ATAG, self.OPT_SOURCE_SUBADDRESS, self.OPT_DEST_SUBADDRESS, self.OPT_USER_RESPONSE_CODE, self.OPT_DISPLAY_TIME, self.OPT_SMS_SIGNAL, self.OPT_MS_VALIDITY, self.OPT_MS_MSG_WAIT_FACILITIES, self.OPT_NUMBER_OF_MESSAGES, self.OPT_ALERT_ON_MESSAGE_DELIVERY, self.OPT_LANGUAGE_INDICATOR, self.OPT_ITS_REPLY_TYPE, self.OPT_ITS_SESSION_INFO]
		elif self.command == SUBMIT_MULTI:
			self._optionals_allowed = [self.OPT_USER_MESSAGE_REFERENCE, self.OPT_SOURCE_PORT, self.OPT_SOURCE_ADDR_SUBUNIT, self.OPT_DESTINATION_PORT, self.OPT_DEST_ADDR_SUBUNIT, self.OPT_SAR_MSG_REF_NUM, self.OPT_SAR_TOTAL_SEGMENTS, self.OPT_SAR_SEGMENT_SEQNUM, self.OPT_PAYLOAD_TYPE, self.OPT_MESSAGE_PAYLOAD, self.OPT_PRIVACY_INDICATOR, self.OPT_CALLBACK_NUM, self.OPT_CALLBACK_NUM_PRES_IND, self.OPT_CALLBACK_NUM_ATAG, self.OPT_SOURCE_SUBADDRESS, self.OPT_DEST_SUBADDRESS, self.OPT_DISPLAY_TIME, self.OPT_SMS_SIGNAL, self.OPT_MS_VALIDITY, self.OPT_MS_MSG_WAIT_FACILITIES, self.OPT_ALERT_ON_MESSAGE_DELIVERY, self.OPT_LANGUAGE_INDICATOR]
		elif self.command == DATA_SM_RESP:
			self._optionals_allowed = [self.OPT_DELIVERY_FAILURE_REASON, self.OPT_NETWORK_ERROR_CODE, self.OPT_ADDITIONAL_STATUS_INFO_TEXT, self.OPT_DPF_RESULT]
		elif self.command == BIND_TRANSMITTER_RESP or self.command == BIND_RECEIVER_RESP or self.command == BIND_TRANSCEIVER_RESP:
			self._optionals_allowed = [self.OPT_SC_INTERFACE_VERSION]
		elif self.command == DELIVER_SM:
			self._optionals_allowed = [self.OPT_USER_MESSAGE_REFERENCE, self.OPT_SOURCE_PORT, self.OPT_DESTINATION_PORT, self.OPT_SAR_MSG_REF_NUM, self.OPT_SAR_TOTAL_SEGMENTS, self.OPT_SAR_SEGMENT_SEQNUM, self.OPT_USER_RESPONSE_CODE, self.OPT_PRIVACY_INDICATOR, self.OPT_PAYLOAD_TYPE, self.OPT_MESSAGE_PAYLOAD, self.OPT_CALLBACK_NUM, self.OPT_SOURCE_SUBADDRESS, self.OPT_DEST_SUBADDRESS, self.OPT_LANGUAGE_INDICATOR, self.OPT_ITS_SESSION_INFO, self.OPT_NETWORK_ERROR_CODE, self.OPT_MESSAGE_STATE, self.OPT_RECEIPTED_MESSAGE_ID]
		else:
			self._optionals_allowed = []

	def add_optional(self, **kwargs):
		"""Add an optional parameter, in the form of SMPPParameters.add_optional(param1 = value1, param2 = value2, ...)
		supported optional parameters can be seen via SMPPParameters._optionals_allowed on an object initialized with the
		correct command code."""
		for tag, value in kwargs.items():
			if not self._optional_tag.has_key(tag):
				raise SMPPException("SMPPParameters unknown optional parameter: %s" % tag)
			tag_code = self._optional_tag[tag]
			if not tag_code in self._optionals_allowed:
				raise SMPPException("SMPPParameters, optional parameter %s not allowed in %s" % (tag, command_b2a[self.command]))
			sz = self._opt_parm_sz[tag_code] # Get the size of the argument, 'S' is for null-terminated string
			if isinstance(value, int):
				if sz == 'S':
					raise SMPPPException("SMPPParameters expected string value for %s" % tag)
			elif isinstance(value, str):
				if not sz == 'S':
					raise SMPPPException("SMPPParameters expected integer value for %s" % tag)
			self._optionals[tag_code] = value

	def get_optionals(self):
		"""Get a dictionary representing the optional parameters initialized either by parse_pdu() or add_optional()"""
		return self._optionals

	def has_optionals(self):
		"""Boolean check for whether we have optional parameters from either parse_pdu() or add_optional()"""
		if len(self._optionals) > 0:
			return True
		return False

	def length(self):
		"""Return the length of the PDU given by prepare_pdu() / __repr__()"""
		return (len(self.prepare_pdu()) / 2)

	def _readstr(self, d):
		ret = ""
		while 1:
			c = d.read(1)
			if c == '\0':
				break
			ret += c
		return ret

	def parse_pdu(self, pdu):
		"""Read a binary PDU and parse it into object variables."""
		length = len(pdu)
		d = StringIO(pdu) # So we can use read()
		left = lambda: length - d.tell()
		readx = lambda x: d.read(x) if left() >= x else None
		readone = lambda: ord(d.read(1)) if left() >= 1 else None

		src_addr_ton = None
		src_addr_npi = None
		src_addr = None
		dest_addr_ton = None
		dest_addr_npi = None
		dest_addr = None
		if self.command == BIND_TRANSMITTER_RESP or self.command == BIND_RECEIVER_RESP or self.command == BIND_TRANSCEIVER_RESP:
			self.system_id = self._readstr(d)
		elif self.command == DATA_SM_RESP:
			self.message_id = self._readstr(d)
		elif self.command == DELIVER_SM:
			self.system_type = self._readstr(d)
			src_addr_ton = readone()
			src_addr_npi = readone()
			src_addr = self._readstr(d)
			dest_addr_ton = readone()
			dest_addr_npi = readone()
			dest_addr = self._readstr(d)
			self.esm_class = readone()
			self.protocol_id = readone()
			self.priority_flag = readone()
			self.schedule_delivery_time = readone()
			self.validity_period = readone()
			self.registered_delivery = readone()
			self.replace_if_present_flag = readone()
			self.data_coding = readone()
			self.sm_default_msg_id = readone()
			self.sm_length = readone()
			self.short_message = readx(self.sm_length)
		elif self.command == DATA_SM:
			self.system_type = self._readstr(d)
			src_addr_ton = readone()
			src_addr_npi = readone()
			src_addr = self._readstr(d)
			dest_addr_ton = readone()
			dest_addr_npi = readone()
			dest_addr = self._readstr(d)
			self.esm_class = readone()
			self.registered_delivery = readone()
			self.data_coding = readone()

		if src_addr and src_addr_ton and src_addr_npi:
			self.source = SMPPAddress(src_addr)
			self.source.set_ton(src_addr_ton)
			self.source.set_npi(src_addr_npi)
		if dest_addr and dest_addr_ton and dest_addr_npi:
			self.destination = SMPPAddress(dest_addr)
			self.destination.set_ton(dest_addr_ton)
			self.destination.set_npi(dest_addr_ton)

		while left() > 0:
			# It seems we have optional parameters!
			opt_code = readx(2)
			opt_code = unpack("!H", opt_code)[0]
			opt_len = readx(2)
			opt_len = unpack("!H", opt_len)[0]
			opt_val = readx(opt_len)
			print "Got optional parameter: %.4X, length %.4X, value: %s" % (opt_code, opt_len, opt_val)
			sz = self._opt_parm_sz[opt_code]
			if not sz == 'S':
				if sz == 4:
					opt_val = unpack("!L", opt_val)[0]
				elif sz == 2:
					opt_val = unpack("!L", opt_val)[0]
			if not opt_code in self._optionals_allowed:
				raise SMPPException("SMPPParameters, pdu contains illegal optional parameter code %.4X" % opt_code)
			self._optionals[opt_code] = opt_val

	def __repr__(self):
		"""__repr__() -> prepare_pdu()"""
		return self.prepare_pdu()

	def prepare_pdu(self):
		"""Generate a hexlified version of a PDU for use in the SMPP module"""
		pdub=""
		if len(self.system_type) == 0 or not self.system_type[-1] == '\0':
			self.system_type += '\0'

		if self.command == BIND_TRANSMITTER \
		or self.command == BIND_RECEIVER \
		or self.command == BIND_TRANSCEIVER:
			if len(self.system_id) == 0 or not self.system_id[-1] == '\0':
				self.system_id += '\0'
			if len(self.password) == 0 or not self.password[-1] == '\0':
				self.password += '\0'
			if len(self.system_id) > 16:
				raise SMPPException("Systemid too long!")
			if len(self.password) > 9:
				raise SMPPException("Password too long!")
			if len(self.system_type) > 13:
				raise SMPPException("Systype too long!")

			pdub += b2a_hex(self.system_id)
			pdub += b2a_hex(self.password)
			pdub += b2a_hex(self.system_type)
			pdub += "%.2X" % self.interface_version
			pdub += "%s" % self.address
		elif self.command == DATA_SM:
			pdub += b2a_hex(self.system_type)
			pdub += "%s" % self.source
			pdub += "%s" % self.destination
			pdub += "%.2X" % self.esm_class
			pdub += "%.2X" % self.registered_delivery
			pdub += "%.2X" % self.data_coding
		elif self.command == SUBMIT_SM:
			pdub += b2a_hex(self.system_type)
			pdub += "%s" % self.source
			pdub += "%s" % self.destination
			pdub += "%.2X" % self.esm_class
			pdub += "%.2X" % self.protocol_id
			pdub += "%.2X" % self.priority_flag
			pdub += "%.2X" % self.schedule_delivery_time
			pdub += "%.2X" % self.validity_period
			pdub += "%.2X" % self.registered_delivery
			pdub += "%.2X" % self.replace_if_present_flag
			pdub += "%.2X" % self.data_coding
			pdub += "%.2X" % self.sm_default_msg_id	
			pdub += "%.2X" % self.sm_length
			pdub += "%.2X" % self.short_message
		elif self.command == DELIVER_SM_RESP:
			pdub += "00" # message_id hardcoded to null, as per spec

		# Now add optional parameters
		for key in self._optionals.keys():
			if key in self._optionals_allowed:
				value = ""
				sz = self._opt_parm_sz[key]
				if sz == 'S':
					value = b2a_hex(self._optionals[key])
				elif sz > 0:
					fmt = "%%.%dX" % (self._opt_parm_sz[key] * 2)
					value = fmt % self._optionals[key]

				pdub += "%.4X" % key
				pdub += "%.4X" % (len(value) / 2)
				pdub += value
		return pdub


