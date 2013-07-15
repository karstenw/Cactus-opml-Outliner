# -*- coding: utf-8 -*-

"""
"""



import objc

import Foundation
NSUserDefaults = Foundation.NSUserDefaults


import AppKit
NSApplication = AppKit.NSApplication
NSWindowController = AppKit.NSWindowController

import CactusTools

####

#
# Open Preferences
#
class CactusPreferenceController(NSWindowController):
    butSetCacheFolder = objc.IBOutlet()
    menDoctype = objc.IBOutlet()
    menEncoding = objc.IBOutlet()
    optAlternateLines = objc.IBOutlet()
    optCache = objc.IBOutlet()
    optCommentColumn = objc.IBOutlet()
    optHLines = objc.IBOutlet()
    optHTMLAutodetect = objc.IBOutlet()
    optIMLAutodetect = objc.IBOutlet()
    optIMLImportSystemLibraries = objc.IBOutlet()
    optOPMLAutodetect = objc.IBOutlet()
    optPLISTAutodetect = objc.IBOutlet()
    optRSSAutodetect = objc.IBOutlet()
    optRSSOpenEnclosure = objc.IBOutlet()
    optTypeColumn = objc.IBOutlet()
    optVLines = objc.IBOutlet()
    optValueColumn = objc.IBOutlet()
    optVariableRowHeight = objc.IBOutlet()
    txtCacheFolder = objc.IBOutlet()
    txtIndent = objc.IBOutlet()
    txtNoOfMaxRowLines = objc.IBOutlet()
    txtNoOfRecentURLs = objc.IBOutlet()
    txtUserEmail = objc.IBOutlet()
    txtUserName = objc.IBOutlet()


    """Present a dialog for entering a URL for http document retrieval."""
    def init(self):
        self = self.initWithWindowNibName_("Preferences")

        wnd = self.window()

        wnd.setTitle_( u"Cactus Preferences" )
        wnd.setDelegate_( self )

        defaults = NSUserDefaults.standardUserDefaults()

        self.optCache.setState_( defaults.objectForKey_( u'optCache') )
        self.txtCacheFolder.setStringValue_( defaults.objectForKey_( u'txtCacheFolder') )
        self.txtNoOfMaxRowLines.setStringValue_( defaults.objectForKey_( u'txtNoOfMaxRowLines') )
        self.txtNoOfRecentURLs.setStringValue_( defaults.objectForKey_( u'txtNoOfRecentURLs') )
        self.txtUserEmail.setStringValue_( defaults.objectForKey_( u'txtUserEmail') )
        self.txtUserName.setStringValue_( defaults.objectForKey_( u'txtUserName') )

        self.optAlternateLines.setState_( defaults.objectForKey_( u'optAlternateLines') )
        self.optCommentColumn.setState_( defaults.objectForKey_( u'optCommentColumn') )
        self.optTypeColumn.setState_( defaults.objectForKey_( u'optTypeColumn') )
        self.optValueColumn.setState_( defaults.objectForKey_( u'optValueColumn') )

        self.optHLines.setState_( defaults.objectForKey_( u'optHLines') )
        self.optVLines.setState_( defaults.objectForKey_( u'optVLines') )
        self.optVariableRowHeight.setState_( defaults.objectForKey_( u'optVariableRowHeight') )

        self.menDoctype.setTitle_( defaults.objectForKey_( u'menDoctype') )
        self.menEncoding.setTitle_( defaults.objectForKey_( u'menEncoding') )
        self.txtIndent.setStringValue_( defaults.objectForKey_( u'txtIndent') )

        self.optIMLAutodetect.setState_( defaults.objectForKey_( u'optIMLAutodetect') )

        self.optOPMLAutodetect.setState_( defaults.objectForKey_( u'optOPMLAutodetect') )
        self.optRSSAutodetect.setState_( defaults.objectForKey_( u'optRSSAutodetect') )
        self.optHTMLAutodetect.setState_( defaults.objectForKey_( u'optHTMLAutodetect') )
        self.optPLISTAutodetect.setState_( defaults.objectForKey_( u'optPLISTAutodetect') )

        self.optRSSOpenEnclosure.setState_( defaults.objectForKey_( u'optRSSOpenEnclosure') )

        self.optIMLImportSystemLibraries.setState_( defaults.objectForKey_( u'optIMLImportSystemLibraries') )
        return self

    def windowWillClose_(self, notification):
        defaults = NSUserDefaults.standardUserDefaults()
        defaults.setObject_forKey_(self.optCache.state(),   u'optCache')
        defaults.setObject_forKey_(self.txtCacheFolder.stringValue(),   u'txtCacheFolder')
        defaults.setObject_forKey_(self.txtNoOfMaxRowLines.stringValue(),   u'txtNoOfMaxRowLines')
        defaults.setObject_forKey_(self.txtNoOfRecentURLs.stringValue(),   u'txtNoOfRecentURLs')
        defaults.setObject_forKey_(self.txtUserEmail.stringValue(),   u'txtUserEmail')
        defaults.setObject_forKey_(self.txtUserName.stringValue(),   u'txtUserName')

        defaults.setObject_forKey_(self.optAlternateLines.state(),   u'optAlternateLines')
        defaults.setObject_forKey_(self.optCommentColumn.state(),   u'optCommentColumn')
        defaults.setObject_forKey_(self.optTypeColumn.state(),   u'optTypeColumn')
        defaults.setObject_forKey_(self.optValueColumn.state(),   u'optValueColumn')

        defaults.setObject_forKey_(self.optHLines.state(),   u'optHLines')
        defaults.setObject_forKey_(self.optVLines.state(),   u'optVLines')
        defaults.setObject_forKey_(self.optVariableRowHeight.state(),   u'optVariableRowHeight')

        defaults.setObject_forKey_(self.menDoctype.title(),   u'menDoctype')
        defaults.setObject_forKey_(self.menEncoding.title(),   u'menEncoding')
        defaults.setObject_forKey_(self.txtIndent.stringValue(),   u'txtIndent')

        defaults.setObject_forKey_(self.optIMLAutodetect.state(),   u'optIMLAutodetect')

        defaults.setObject_forKey_(self.optOPMLAutodetect.state(),   u'optOPMLAutodetect')
        defaults.setObject_forKey_(self.optRSSAutodetect.state(),   u'optRSSAutodetect')
        defaults.setObject_forKey_(self.optHTMLAutodetect.state(),   u'optHTMLAutodetect')
        defaults.setObject_forKey_(self.optPLISTAutodetect.state(),   u'optPLISTAutodetect')

        defaults.setObject_forKey_(self.optRSSOpenEnclosure.state(),   u'optRSSOpenEnclosure')

        defaults.setObject_forKey_(self.optIMLImportSystemLibraries.state(),   u'optIMLImportSystemLibraries')

    @objc.IBAction
    def chooseFolder_(self, sender):
        if sender == self.butSetCacheFolder:
            folders = CactusTools.getFolderDialog()
            if folders:
                self.txtCacheFolder.setStringValue_( folders[0] )


