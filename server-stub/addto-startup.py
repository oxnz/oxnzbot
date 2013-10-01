#!/usr/bin/env python
#coding: utf-8

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
    print 'add startup item for darwin'
    plist = '/Library/LaunchDaemons/org.oxnzbot.plist'

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
    Helper.sudo(os.path.abspath(__file__))

if __name__ == '__main__':
    main()
