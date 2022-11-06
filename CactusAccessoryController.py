# -*- coding: utf-8 -*-

"""This is the controller for the "Open as..." menu inside the open file dialog.
"""

import sys
import os

import objc

import Foundation
NSObject = Foundation.NSObject
NSBundle = Foundation.NSBundle


# py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int

class CactusOpenAsAccessoryController(NSObject):
    """Just a holder for some values and an action for a open panel accessory."""

    menuOpenAs = objc.IBOutlet()

    def __new__(cls):
        return cls.alloc()

    def init(self):
        panel = NSBundle.loadNibNamed_owner_( u"OpenAsAccessoryView", self)
        return self

    @objc.IBAction
    def menuOpenAsType_( self, sender ):
        return None
        # return self.menuOpenAs.title()
