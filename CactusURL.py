
# -*- coding: utf-8 -*-


"""A class to handle all of Cactus URL conversion needs.
"""

import sys
import os

import traceback

import datetime
import unicodedata

import struct

import mactypes
import appscript
asc = appscript

import CactusVersion
kwdbg = CactusVersion.developmentversion
kwlog = CactusVersion.developmentversion

import pdb

import re

from urllib.parse import urlparse

import Foundation
NSURL = Foundation.NSURL
NSString = Foundation.NSString


# py3 stuff
punicode = str
pstr = bytes
py3 = True
punichr = chr
long = int

def NSURL2str( nsurl ):
    if isinstance(nsurl, NSURL):
        return str(nsurl.absoluteString())
    return nsurl


class CactusURL(object):
    def __init__(self, url):
        # str, unicode or NSURL
        self.inputurl = url
        t = type(url)
        if t in (str, unicode):
            self.url = url
        elif t in (NSURL,):
            self.url = NSURL2str( url )
        p = urlparse( self.url )
        self.schema = p.schema
    def ascachepath(self):
        pass

