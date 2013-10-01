import os

__author__ = '0xnz'
__version__ = '0.1'
__all__ = ['Helper']

class Helper():
    
    @classmethod
    def sudo(cls, command):
        cmd = """osascript -e 'do shell script "{0}" with administrator privileges'""".format(command)
        os.system(cmd)
