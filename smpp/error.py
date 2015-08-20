from exception import SMPPException

class SMPPError:
	ESME_ROK		= 0x00000000 
	ESME_RINVMSGLEN		= 0x00000001 
	ESME_RINVCMDLEN		= 0x00000002 
	ESME_RINVCMDID		= 0x00000003 
	ESME_RINVBNDSTS		= 0x00000004 
	ESME_RALYBND		= 0x00000005 
	ESME_RINVPRTFLG		= 0x00000006 
	ESME_RINVREGDLVFLG	= 0x00000007 
	ESME_RSYSERR		= 0x00000008 
	ESME_RINVSRCADR		= 0x0000000A 
	ESME_RINVDSTADR		= 0x0000000B 
	ESME_RINVMSGID		= 0x0000000C 
	ESME_RBINDFAIL		= 0x0000000D 
	ESME_RINVPASWD		= 0x0000000E 
	ESME_RINVSYSID		= 0x0000000F 
	ESME_RCANCELFAIL	= 0x00000011 
	ESME_RREPLACEFAIL	= 0x00000013 
	ESME_RMSGQFUL		= 0x00000014 
	ESME_RINVSERTYP		= 0x00000015 
	ESME_RINVNUMDESTS	= 0x00000033 
	ESME_RINVDLNAME		= 0x00000034 
	ESME_RINVDESTFLAG	= 0x00000040 
	ESME_RINVSUBREP		= 0x00000042 
	ESME_RINVESMCLASS	= 0x00000043 
	ESME_RCNTSUBDL		= 0x00000044 
	ESME_RSUBMITFAIL	= 0x00000045 
	ESME_RINVSRCTON		= 0x00000048 
	ESME_RINVSRCNPI		= 0x00000049 
	ESME_RINVDSTTON		= 0x00000050 
	ESME_RINVDSTNPI		= 0x00000051 
	ESME_RINVSYSTYP		= 0x00000053 
	ESME_RINVREPFLAG	= 0x00000054 
	ESME_RINVNUMMSGS	= 0x00000055 
	ESME_RTHROTTLED		= 0x00000058 
	ESME_RINVSCHED		= 0x00000061 
	ESME_RINVEXPIRY		= 0x00000062 
	ESME_RINVDFTMSGID	= 0x00000063 
	ESME_RX_T_APPN		= 0x00000064 
	ESME_RX_P_APPN		= 0x00000065 
	ESME_RX_R_APPN		= 0x00000066 
	ESME_RQUERYFAIL		= 0x00000067 
	ESME_RINVOPTPARSTREAM	= 0x000000C0 
	ESME_ROPTPARNOTALLWD	= 0x000000C1 
	ESME_RINVPARLEN		= 0x000000C2 
	ESME_RMISSINGOPTPARAM	= 0x000000C3 
	ESME_RINVOPTPARAMVAL	= 0x000000C4 
	ESME_RDELIVERYFAILURE	= 0x000000FE 
	ESME_RUNKNOWNERR	= 0x000000FF 
	_error_description={
		ESME_ROK:		'OK',
		ESME_RINVMSGLEN:	'Message Length is invalid',
		ESME_RINVCMDLEN:	'Command Length is invalid',
		ESME_RINVCMDID:		'Invalid Command ID',
		ESME_RINVBNDSTS:	'Incorrect BIND Status for given command',
		ESME_RALYBND:		'ESME Already in Bound State',
		ESME_RINVPRTFLG:	'Invalid Priority Flag',
		ESME_RINVREGDLVFLG:	'Invalid Registered Delivery Flag',
		ESME_RSYSERR:		'System Error',
		ESME_RINVSRCADR:	'Invalid Source Address',
		ESME_RINVDSTADR:	'Invalid Dest Addr',
		ESME_RINVMSGID:		'Message ID is invalid',
		ESME_RBINDFAIL:		'Bind Failed',
		ESME_RINVPASWD:		'Invalid Password',
		ESME_RINVSYSID:		'Invalid System ID',
		ESME_RCANCELFAIL:	'Cancel SM Failed',
		ESME_RREPLACEFAIL:	'Replace SM Failed',
		ESME_RMSGQFUL:		'Message Queue Full',
		ESME_RINVSERTYP:	'Invalid Service Type',
		ESME_RINVNUMDESTS:	'Invalid number of destinations',
		ESME_RINVDLNAME:	'Invalid Distribution List name',
		ESME_RINVDESTFLAG:	'Destination flag is invalid (submit_multi)',
		ESME_RINVSUBREP:	'Invalid "submit with replace" request (i.e.  submit_sm with replace_if_present_flag set)',
		ESME_RINVESMCLASS:	'Invalid esm_class field data',
		ESME_RCNTSUBDL:		'Cannot Submit to Distribution List ',
		ESME_RSUBMITFAIL:	'submit_sm or submit_multi failed',
		ESME_RINVSRCTON:	'Invalid Source address TON ',
		ESME_RINVSRCNPI:	'Invalid Source address NPI       ',
		ESME_RINVDSTTON:	'Invalid Destination address TON',
		ESME_RINVDSTNPI:	'Invalid Destination address NPI',
		ESME_RINVSYSTYP:	'Invalid system_type field',
		ESME_RINVREPFLAG:	'Invalid replace_if_present flag',
		ESME_RINVNUMMSGS:	'Invalid number of messages',
		ESME_RTHROTTLED:	'Throttling error (ESME has exceeded allowed message limits)',
		ESME_RINVSCHED:		'Invalid Scheduled Delivery Time',
		ESME_RINVEXPIRY:	'Invalid message validity period (Expiry time)',
		ESME_RINVDFTMSGID:	'Predefined Message Invalid or Not Found',
		ESME_RX_T_APPN:		'ESME Receiver Temporary App Error Code',
		ESME_RX_P_APPN:		'ESME Receiver Permanent App Error Code',
		ESME_RX_R_APPN:		'ESME Receiver Reject Message Error Code',
		ESME_RQUERYFAIL:	'query_sm request failed',
		ESME_RINVOPTPARSTREAM:	'Error in the optional part of the PDU Body.',
		ESME_ROPTPARNOTALLWD:	'Optional Parameter not allowed',
		ESME_RINVPARLEN:	'Invalid Parameter Length.',
		ESME_RMISSINGOPTPARAM:	'Expected Optional Parameter missing',
		ESME_RINVOPTPARAMVAL:	'Invalid Optional Parameter Value',
		ESME_RDELIVERYFAILURE:	'Delivery Failure (used for data_sm_resp)',
		ESME_RUNKNOWNERR:	'Unknown Error',
	}
	def __init__(self, error=ESME_RUNKNOWNERR):
		errcode=None
		if not isinstance(error, int):
			raise SMPPException("Expected integer, got %s!" % type(error))
		self.errcode = error
	def __repr__(self):
		if self.errcode == None:
			self.errcode = self.ESME_RUNKNOWNERR
		return self._error_description[self.errcode]



