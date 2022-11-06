#
#   CactusOutlineWindow.py
#
#   Created by Karsten Wolf on 04.12.13.
#   Copyright 2013 __MyCompanyName__. All rights reserved.
#

from __future__ import print_function


import sys
import os

import pdb
import pprint
pp = pprint.pprint
kwdbg = False
kwlog = True

import AppKit
NSApplication = AppKit.NSApplication
NSWindow = AppKit.NSWindow

NSFilenamesPboardType = AppKit.NSFilenamesPboardType
NSDragOperationCopy = AppKit.NSDragOperationCopy
NSFilenamesPboardType = AppKit.NSFilenamesPboardType
NSDragOperationNone = AppKit.NSDragOperationNone


class CactusOutlineWindow(NSWindow):
    # pass
    def awakeFromNib(self):
        # self.registerForDraggedTypes_([NSFilenamesPboardType])
        pass
    """
    def draggingEntered_(self,sender):
        print( "CactusOutlineWindow.draggingEntered_" )
        pboard = sender.draggingPasteboard()
        types = pboard.types()
        opType = NSDragOperationNone
        if NSFilenamesPboardType in types:
            opType = NSDragOperationCopy
        return opType

    def performDragOperation_(self,sender):
        print( "CactusOutlineWindow.performDragOperation_" )
        pboard = sender.draggingPasteboard()
        successful = False
        if NSFilenamesPboardType in pboard.types():

            files = pboard.propertyListForType_( NSFilenamesPboardType )
            numberOfFiles = files.count()

            # Perform operation using the list of files
            # self.appDelegate.addFiles_( files )
            pp(files)

            successful = True
        return successful
    """