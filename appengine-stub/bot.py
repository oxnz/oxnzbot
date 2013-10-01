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

__author__ = '0xnz <yunxinyi@gmail.com>'
__version__ = '0.1'

import datetime
from google.appengine.api import (datastore_types, xmpp)
from google.appengine.ext import ndb
from google.appengine.ext.webapp import xmpp_handlers
import webapp2
from webapp2_extras import jinja2
import logging
from command import Command

BOSS_JID='yunxinyi@gmail.com'

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
        sender = bare_jid(self.request.get('from'))
        logging.debug('XmppPresenceHandler method post from %s status %s' % (sender, status))
#        if status == 'probe':
#            xmpp.send_presence()

class XmppHandler(webapp2.RequestHandler):
    def post(self):
        sender = bare_jid(self.request.get('from'))
        if sender == BOSS_JID:
            '''parse a new cmd and save it.'''
            message = xmpp.Message(self.request.POST)
            logging.info('BOSS command: %s' % message.body)
            try:
                recv, cmd = message.body.split('++')
            except ValueError:
                message.reply('Are you kidding me? Why are you saying "%s"' % message.body)
            else:
                logging.info('caching comamnd %s for %s' % (cmd, recv))
                Command.putCmdFor(cmd, recv)
                message.reply('cached for [%s]' % recv)
        #TODO: validate if sender a real server
        elif sender != BOSS_JID:
            return
            '''send result to boss'''
            logging.info('not BOSS, sending command')
            result = self.request.get('result')
            msg = 'result from server [%s]:\n%s' % (sender, result)
            xmpp.send_message(BOSS_JID, msg)
            cmd = Command.getCmdFor(sender)
            if cmd == None:
                logging.debug('server %s is sleep 4 seconds cause no command available' % sender)
                self.response.write('sleep 4')
            else:
                self.response.write(cmd.command)
                cmd.key.delete()
        else:
            '''neither boss nor server, do nothing'''
            pass
    def get(self):
        self.response.write('<h1>Under Construction...</h1>')

class XmppErrorHandler(webapp2.RequestHandler):
    def post(self):
        error_sender = self.request.get('from')
        error_stanza = self.request.get('stanza')
        logging.error('XMPP error received from %s (%s)', error_sender,
                error_stanza)
        def get(self):
            self.response.write('Error occured')

class CapsidHandler(webapp2.RequestHandler):
    '''Handle command'''
    def get(self):
        sender = self.request.get('from')
        logging.info('get method of CapsidHandler sender: %s' % sender)
        cmd = Command.getCmdFor(sender)
        if cmd == None:
            self.response.write('')
        else:
            self.response.write(cmd.command)
            cmd.key.delete()
    def post(self):
        sender = self.request.get('from')
        command = self.request.get('command')
        status = self.request.get('result')
        output = self.request.get('output')
        msg = '[%s]$ %s\n%s\n(status=%s)' % (sender, command, status, output)
        #TODO: add checking if the msg delivery success
        xmpp.send_message(BOSS_JID, msg)
        self.response.write("posting: Hello, capsid is serviceing")

APPLICATION = webapp2.WSGIApplication([
    ('/_ah/xmpp/__0x01379/', CapsidHandler),
    ('/_ah/xmpp/subscription/(subscribe|subscribed|unsubscribe|unsubscribed)/', XmppSubscribeHandler),
    ('/_ah/xmpp/presence/(probe|available|unavailable)/', XmppPresenceHandler),
    ('/_ah/xmpp/message/chat/', XmppHandler),
    ('/_ah/xmpp/error/', XmppErrorHandler),
    ], debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
