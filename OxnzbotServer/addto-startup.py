#!/usr/bin/env python
#coding: utf-8

#Description: make server-stub auto load.

__author__ = '0xnz'
__version__ = '0.1'

import os
import sys
import re
import time
import ctypes
import platform
from helper import Helper

def add_startup_linux():
    pass

def add_startup_darwin():
    #Helper.sudo('python {0}'.format(os.path.abspath(__file__)))
    try:
        import plistlib
    except ImportError, e:
        print '*** error: {0}'.format(e.message)
    print 'add startup item for darwin'
    fplist = '/Library/LaunchDaemons/com.appspot.oxnzbot.plist'
    pl = dict(
            GroupName = 'wheel',
            Label = 'com.appspot.oxnzbot',
            PrograpArguments = list([
                '/usr/bin/python',
                os.path.abspath(__file__)
                ]),
            RunAtLoad = True,
            UserName = 'root',
            WorkingDirectory = '/',
            StandardOutPath = '/var/log/oxnzbot.log',
            StandardErrorPath = '/var/log/oxnzbot.log',
            KeepAlive = dict(
                SuccessfulExit = False,
                )
            )
    plistlib.writePlist(pl, fplist)
    return

def add_startup_windows():
    pass

def main():
    filename = os.path.abspath(__file__)
    add_startup_funcs = {
            'Darwin'    : add_startup_darwin,
            'Windows'   : add_startup_windows,
            'Linux'     : add_startup_linux,
            }
    add_startup_funcs.get(platform.system())()

if __name__ == '__main__':
    main()
