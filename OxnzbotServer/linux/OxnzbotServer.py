#!/usr/bin/env python
#coding: utf-8

import os
import time

class Command(object):
    pass

class HttpService(object):
    def __init__(self, url):
        pass
    def doPost(self):
        pass
    def doGet(self):
        pass


class OxnzbotServer(object):
    def __init__(self, httpService):
        super(OxnzbotServer, self).__init__()
        self.__httpService = httpService
    def getCommand(self):
        return 'echo hello'
    def execCommand(self, command):
        os.system(command)
    def postResult(self, result):
        pass
    def serve_forever(self):
        while True:
            cmd = self.getCommand()
            if cmd != None:
                self.execCommand(cmd)
            else:
                time.sleep(1)

def main():
    server = OxnzbotServer(HttpService('http://oxnzbot.appspot.com/_ah/xmpp/'))
    server.serve_forever()

if __name__ == '__main__':
    main()
