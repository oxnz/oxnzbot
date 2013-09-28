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
import datetime
from google.appengine.api import datastore_types
from google.appengine.api import xmpp
from google.appengine.ext import ndb
from google.appengine.ext.webapp import xmpp_handlers
import webapp2
from webapp2_extras import jinja2
import logging

class Contact(ndb.Model):
	"""Model to hold questions"""
	pass

def bare_jid(sender):
	"""Identify the user by bare jid.

	Example:
		node@domain/resource will return node@domain
	See http://wiki.xmpp.org/web/Jabber_Resources for more details.

	Args:
		sender: String; A jabber or XMPP sender.

	Returns:
		The bare Jabber ID of the sender.
	"""
	return sender.split('/')[0]

class XmppSubscribeHandler(webapp2.RequestHandler):
	def post(self, notification):
		sender = bare_jid(self.request.get('from'))
		logging.debug('XmppSubscribeHandler %s got notification %s' % (sender, notification))
		#roster.add_contact(sender)

class XmppPresenceHandler(webapp2.RequestHandler):
	"""Handler class for XMPP status updates."""

	def post(self, status):
		"""POST handler for XMPP presence.


		Args:
			status: A string which will be either available or
			unavailable and will indicate the status of the user.
		"""
		sender = self.request.get('from')
		logging.debug('XmppPresenceHandler method post from %s status %s' % (sender, status))

class XmppHandler(webapp2.RequestHandler):
	def post(self):
		logging.debug('XmppHandler post method')
		message = xmpp.Message(self.request.POST)
		if message.body[0:5].lower() == 'hello':
			message.reply('Greetings!')
		elif message.body[0:4].lower() == 'send':
			xmpp.send_invite('yunxinyi@gmail.com')
			to = 'yunxinyi@gmail.com'
			status = xmpp.send_message(to, 'sending')
			if not (status == xmpp.NO_ERROR):
				print 'error while sending'
		else:
			message.reply('Are you kidding me?')
			logging.debug('from %s content %s' % (message.sender, message.body))

class XmppErrorHandler(webapp2.RequestHandler):
	def post(self):
		error_sender = self.request.get('from')
		error_stanza = self.request.get('stanza')
		logging.error('XMPP error received from %s (%s)', error_sender,
				error_stanza)


APPLICATION = webapp2.WSGIApplication([
	('/', LatestHandler),
	('/_ah/xmpp/subscription/(subscribe|subscribed|unsubscribe|unsubscribed)/', XmppSubscribeHandler),
	('/_ah/xmpp/presence/(available|unavailable)/', XmppPresenceHandler),
	('/_ah/xmpp/message/chat/', XmppHandler),
	('/_ah/xmpp/error/', XmppErrorHandler),
], debug=True)

def main():
	run_wsgi_app(application)

if __name__ == '__main__':
	main()
