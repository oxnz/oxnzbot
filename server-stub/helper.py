import os

class Helper():
    
    @classmethod
    def sudo(cls, abspath):
        cmd = '''osascript -e 'do shell script \"{0}\" with root privileges'''.format(abspath)
        print cmd
        os.system(cmd)
