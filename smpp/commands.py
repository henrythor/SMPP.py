BIND_RECEIVER =		0x00000001
BIND_TRANSMITTER =	0x00000002
QUERY_SM =		0x00000003
SUBMIT_SM =		0x00000004
DELIVER_SM =		0x00000005
UNBIND =		0x00000006
REPLACE_SM =		0x00000007
CANCEL_SM =		0x00000008
BIND_TRANSCEIVER =	0x00000009
OUTBIND =		0x0000000B
ENQUIRE_LINK =		0x00000015
SUBMIT_MULTI =		0x00000021
ALERT_NOTIFICATION =	0x00000102
DATA_SM =		0x00000103
GENERIC_NACK_RESP =	0x80000000
BIND_RECEIVER_RESP =	0x80000001
BIND_TRANSMITTER_RESP =	0x80000002
QUERY_SM_RESP =		0x80000003
SUBMIT_SM_RESP =	0x80000004
DELIVER_SM_RESP =	0x80000005
UNBIND_RESP =		0x80000006
REPLACE_SM_RESP =	0x80000007
CANCEL_SM_RESP =	0x80000008
BIND_TRANSCEIVER_RESP =	0x80000009
ENQUIRE_LINK_RESP =	0x80000015
SUBMIT_MULTI_RESP =	0x80000021
DATA_SM_RESP =		0x80000103

command_a2b = {
	"bind_receiver":		BIND_RECEIVER,
	"bind_transmitter":		BIND_TRANSMITTER,
	"query_sm":			QUERY_SM,
	"submit_sm":			SUBMIT_SM,
	"deliver_sm":			DELIVER_SM,
	"unbind":			UNBIND,
	"replace_sm":			REPLACE_SM,
	"cancel_sm":			CANCEL_SM,
	"bind_transceiver":		BIND_TRANSCEIVER,
	"outbind":			OUTBIND,
	"enquire_link":			ENQUIRE_LINK,
 	"submit_multi":			SUBMIT_MULTI,
	"alert_notification":		ALERT_NOTIFICATION,
 	"data_sm":			DATA_SM
}

response_a2b = {
	"generic_nack":		GENERIC_NACK_RESP,
	"bind_receiver":	BIND_RECEIVER_RESP,
	"bind_transmitter":	BIND_TRANSMITTER_RESP,
	"query_sm":		QUERY_SM_RESP,
	"submit_sm":		SUBMIT_SM_RESP,
	"deliver_sm":		DELIVER_SM_RESP,
	"unbind":		UNBIND_RESP,
	"replace_sm":		REPLACE_SM_RESP,
	"cancel_sm":		CANCEL_SM_RESP,
	"bind_transceiver":	BIND_TRANSCEIVER_RESP,
	"enquire_link":		ENQUIRE_LINK_RESP,
	"submit_multi":		SUBMIT_MULTI_RESP,
	"data_sm":		DATA_SM_RESP
}

command_b2a = {
	BIND_RECEIVER:		"bind_receiver",
	BIND_TRANSMITTER:	"bind_transmitter",
	QUERY_SM:		"query_sm",
	SUBMIT_SM:		"submit_sm",
	DELIVER_SM:		"deliver_sm",
	UNBIND:			"unbind",
	REPLACE_SM:		"replace_sm",
	CANCEL_SM:		"cancel_sm",
	BIND_TRANSCEIVER:	"bind_transceiver",
	OUTBIND:		"outbind",
	ENQUIRE_LINK:		"enquire_link",
	SUBMIT_MULTI:		"submit_multi",
	ALERT_NOTIFICATION:	"alert_notification",
	DATA_SM:		"data_sm",
}

response_b2a = {
	GENERIC_NACK_RESP:	"generic_nack",
	BIND_RECEIVER_RESP:	"bind_receiver",
	BIND_TRANSMITTER_RESP:	"bind_transmitter",
	QUERY_SM_RESP:		"query_sm",
	SUBMIT_SM_RESP:		"submit_sm",
	DELIVER_SM_RESP:	"deliver_sm",
	UNBIND_RESP:		"unbind",
	REPLACE_SM_RESP:	"replace_sm",
	CANCEL_SM_RESP:		"cancel_sm",
	BIND_TRANSCEIVER_RESP:	"bind_transceiver",
	ENQUIRE_LINK_RESP:	"enquire_link",
	SUBMIT_MULTI_RESP:	"submit_multi",
	DATA_SM_RESP:		"data_sm",
}


