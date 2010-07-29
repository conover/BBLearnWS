#
# A simple script to demostrate connecting to Blackboard Learn 9.1 
# Web Services using the Python Suds SOAP client library.
#
# Use at your own risk.
#
# Written by Chris Conover on July 29, 2010

# Requires Suds 0.4 Beta for plugin support
# https://fedorahosted.org/suds/
from suds.client 	import Client
from suds.plugin 	import Plugin
from suds.wsse  	import Timestamp, UsernameToken, Security

# The base web service URL of your server
WS_BASE_URL = '' # They call it https://your.institution.edu/webapps/ws/services/

# Suds does not provide the "type" attribute on the Password tag 
# of the UsernameToken in the WS-Security SOAP headers. Create
# a plugin which adds it at send time.
class Learn9Plugin(Plugin):
	def sending(self, context):
		password = context.envelope.childAtPath('Header/Security/UsernameToken/Password')
		password.set('Type', 'http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-username-token-profile-1.0#PasswordText')

# WS-Security Headers. Timestamp token MUST come before UsernameToken
security = Security()
security.tokens.append(Timestamp())
# Set initial WS-Security user ID and password.
# Password will be updated with the result of the `initialize` operation.
security.tokens.append(UsernameToken('session', 'nosession')) 

client = Client(	WS_BASE_URL + 'Context.WS?wsdl',
					location = WS_BASE_URL + 'Context.WS', # Learn 9.1 WSDL misreports service endpoints so set it manually
					autoblend = True, # Learn 9.1 WSDLs use nested imports
					wsse = security, # Add WS-Security tokens
					plugins = [Learn9Plugin()]) # Add WS-Security/UsernameToken/Password Type fix

session_password = client.service.initialize()
client.options.wsse.tokens[1].password = session_password