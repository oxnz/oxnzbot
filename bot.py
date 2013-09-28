#!/usr/bin/env python
#
# Copyright 2013 oxnz <yunxinyi@gmail.com>, All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
from google.appengine.api import xmpp

class XmppPresenceHandler(webapp2.RequestHandler):
	"""Handler class for XMPP status updates."""

	def post(self, status):
		"""POST handler for XMPP presence.


		Args:
			status: A string which will be either available or
			unavailable and will indicate the status of the user.
		"""
		sender = self.request.get('from')
		im_from = datastore_types.IM('xmpp', bare_jid(sender))
		suspend = (status == 'unavailable')




class XMPPHandler(webapp2.RequestHandler):
	def post(self):
		print 'post...'
		message = xmpp.Message(self.request.POST)
		if message.body[0:5].lower() == 'hello':
			message.reply('Greetings!')
		elif message.body[0:4].lower() == 'send':
			xmpp.send_invite('yunxinyi@gmail.com')
			status = xmpp.send_message('yunxinyi@gmail.com', 'sending')
			if not (status == xmpp.NO_ERROR):
				print 'error while sending'
		else:
			print 'from:', message.sender, 'to:',  message.to
			print 'body:', message.body
	def request(self):
		print 'request...'

APPLICATION = webapp2.WSGIApplication([
    ('/_ah/xmpp/presence/(available|unavailable)/', XmppPresenceHandler),
    ('/_ah/xmpp/message/chat/', XmppHandler)
], debug=True)
