import logging
from google.appengine.ext import ndb

class Command(ndb.Model):
    receiver = ndb.StringProperty(required=True)
    command = ndb.StringProperty(required=True)
    stamp = ndb.DateTimeProperty(required=True, auto_now_add=True)

    @classmethod
    def getCmdFor(cls, receiver):
        query = cls.query(cls.receiver == receiver)
        query.order(cls.stamp)
        cmdList = query.fetch(1)
        if len(cmdList) == 0:
            return None
        else:
            return cmdList[0]

    @classmethod
    def putCmdFor(cls, cmd, recv):
        cmd = Command(receiver=recv, command=cmd)
        cmd.put()
