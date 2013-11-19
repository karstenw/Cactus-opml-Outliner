# -*- coding: utf-8 -*-

"""
"""



import objc

import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL
NSMutableDictionary = Foundation.NSMutableDictionary
NSUserDefaults = Foundation.NSUserDefaults
NSBundle = Foundation.NSBundle


import AppKit
NSApplication = AppKit.NSApplication
NSWindowController = AppKit.NSWindowController


import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType


#
# Open URL Delegate
#
class OpenURLWindowController(NSWindowController):
    """Present a dialog for entering a URL for http document retrieval."""

    label = objc.IBOutlet()
    textfield = objc.IBOutlet()
    menuLastVisited = objc.IBOutlet()
    menuOpenAs = objc.IBOutlet()

    # class defined in OpenURL.nib
    # OpenURLWindowController(NSWindowController)
    #
    #
    # actions
    #
    # OK:
    # Cancel:
    # clearMenu:
    # lastVisitedMenuSelection:
    #
    # label
    # textfield
    #
    #
    # visitedURLs
    # menuLastVisited
    def __new__(cls):
        return cls.alloc()

    def init(self):
        self = self.initWithWindowNibName_("OpenURL")
        window = self.window()
        window.setDelegate_( self )
        window.setTitle_( u"Open URL…" )
        window.makeFirstResponder_(self.textfield)

        app = NSApplication.sharedApplication()
        delg = app.delegate()

        self.readAsType = CactusOPMLType
        self.visitedURLs = delg.visitedURLs[:]
        self.menuLastVisited.removeAllItems()

        defaults = NSUserDefaults.standardUserDefaults()
        self.noOfRecentURLs = 40
        try:
            self.noOfRecentURLs = int(defaults.objectForKey_( u'txtNoOfRecentURLs'))
        except StandardError, err:
            print "ERROR reading defaults.", repr(err)

        # cap recentURLs to max size
        if len(self.visitedURLs) > self.noOfRecentURLs:
            self.visitedURLs = self.visitedURLs[:self.noOfRecentURLs]

        for url in self.visitedURLs:
            self.menuLastVisited.addItemWithTitle_( url )
        self.showWindow_(self)
        self.retain()
        return self

    @objc.IBAction
    def clearMenu_(self, sender):
        self.visitedURLs = []
        app = NSApplication.sharedApplication()
        delg = app.delegate()
        delg.visitedURLs = self.visitedURLs
        self.menuLastVisited.removeAllItems()

    @objc.IBAction
    def lastVisitedMenuSelection_(self, sender):
        urlSelected = self.menuLastVisited.title()
        self.textfield.setStringValue_( urlSelected )

    @objc.IBAction
    def openAsMenuSelection_(self, sender):
        self.readAsType = self.menuOpenAs.title()

    def windowWillClose_(self, notification):
        self.autorelease()

    @objc.IBAction
    def OK_(self, sender):
        "User pressed OK button. Get data and try to open that stuff."

        app = NSApplication.sharedApplication()
        delg = app.delegate()
        t_url = self.textfield.stringValue()
        url = NSURL.URLWithString_( t_url )
        self.readAsType = self.menuOpenAs.title()
        if t_url == u"":
            self.close()
            return
        if t_url not in self.visitedURLs:
            self.visitedURLs.insert( 0, t_url )
            n = len(self.visitedURLs)
            if n > self.noOfRecentURLs:
                self.visitedURLs = self.visitedURLs[:self.noOfRecentURLs]
        else:
            # put visited url at top
            self.visitedURLs.remove( t_url )
            self.visitedURLs.insert( 0, t_url )
            self.menuLastVisited.removeAllItems()
            for menuItem in self.visitedURLs:
                self.menuLastVisited.addItemWithTitle_( menuItem )
        delg.visitedURLs = self.visitedURLs[:]
        delg.newOutlineFromURL_Type_( url, str(self.readAsType) )
        self.close()

    @objc.IBAction
    def Cancel_(self, sender):
        #pdb.set_trace()
        self.close()

