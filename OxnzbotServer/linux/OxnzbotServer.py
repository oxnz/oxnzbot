#!/usr/bin/env python
#coding: utf-8

import os
import time
import threading
import commands

class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError

class Command(object):
    pass

class HttpService(object):
    def __init__(self, url):
        pass
    def doPost(self):
        pass
    def doGet(self):
        pass

class GetCommandThread(threading.Thread):
    def __init__(self, commandPool):
        super(GetCommandThread, self).__init__()
        self.__commandPool = commandPool
    def run(self):
        print 'get command run'
        while True:
            time.sleep(1)
            self.__commandPool.append('echo hello')

class ExecCommandThread(threading.Thread):
    def __init__(self, commandPool, resultPool):
        super(ExecCommandThread, self).__init__()
        self.__commandPool = commandPool
        self.__resultPool = resultPool
    def run(self):
        print 'exec command run'
        if len(self.__commandPool) > 0:
            cmd = self.__commandPool[0]
            result = commands.getstatusoutput(cmd)
            self.__resultPool.append(result)
            del self.__commandPool[0]


class PostResultThread(threading.Thread):
    def __init__(self, resultPool):
        super(PostResultThread, self).__init__()
        self.__resultPool = resultPool
    def run(self):
        print 'post result run...'
        while len(self.__resultPool) > 0:
            result = self.__resultPool.pop()
            print 'result:', result

class OxnzbotServer(object):
    state = Enum(["START", "STOP"])
    def __init__(self, httpService):
        super(OxnzbotServer, self).__init__()
        self.__state = OxnzbotServer.state.STOP
        self.__commandPool = list()
        self.__resultPool = list()
        self.__getCommandThread = GetCommandThread(self.__commandPool)
        self.__execCommandThread = ExecCommandThread(self.__commandPool,
                self.__resultPool)
        self.__postResultThread = PostResultThread(self.__resultPool)
    def start(self):
        self.__state = OxnzbotServer.state.START
        self.__getCommandThread.start()
        self.__execCommandThread.start()
        self.__postResultThread.start()
    def stop(self):
        if self.__state != OxnzbotServer.state.STOP:
            self.__state = OxnzbotServer.state.STOP
    def restart(self):
        self.stop()
        self.start()

def main():
    server = OxnzbotServer(HttpService('http://oxnzbot.appspot.com/_ah/xmpp/'))
    server.start()

if __name__ == '__main__':
    main()
