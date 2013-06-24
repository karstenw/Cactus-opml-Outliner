# -*- coding: utf-8 -*-

"""
"""

import sys
import os

import objc

import Foundation
NSObject = Foundation.NSObject
NSBundle = Foundation.NSBundle


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
        return self.menuOpenAs.title()
