import urllib
import urllib2
import socket
import cookielib
import os

def hpost(url, data):
#    req = urllib2.Request(url, data)
    req = urllib2.Request(url)
    resp = urllib2.urlopen(req)
    return resp.read()

data = urllib.urlencode({
    'a':'b',
    })

lurl = 'http://localhost:8080/'
ourl = 'http://oxnzbot.appspot.com'
xurl = 'http://oxnzbot.appspot.com/_ah/xmpp/'
burl = 'http://www.baidu.com/'

print hpost(xurl, data)
