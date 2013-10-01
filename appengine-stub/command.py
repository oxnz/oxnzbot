import logging
from google.appengine.ext import ndb

__author__ = '0xnz <yunxinyi@gmail.com>'
__version__ = '0.1'

class Command(ndb.Model):
    receiver = ndb.StringProperty(required=True)
    command = ndb.StringProperty(required=True)
    stamp = ndb.DateTimeProperty(required=True, auto_now_add=True)

    @classmethod
    def getCmdFor(cls, recv):
        query = cls.query(cls.receiver == recv)
        query.order(cls.stamp)
        cmdList = query.fetch()
        if len(cmdList) == 0:
            return None
        else:
            return cmdList[0]

    @classmethod
    def putCmdFor(cls, cmd, recv):
        cmd = Command(receiver=recv, command=cmd)
        cmd.put()
