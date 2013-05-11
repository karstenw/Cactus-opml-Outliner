
# -*- coding: utf-8 -*-


"""A collection of outline related stuff
"""

import sys
import os

import traceback

import time
import datetime

import urllib
import urlparse

import math
import feedparser


kwdbg = False
kwlog = True

import pdb
import pprint
pp = pprint.pprint

# i prefer manual aliasing
import operator
getitem = operator.getitem
setitem = operator.setitem


# debugging; gives nodes a serialnr
import itertools
counter = itertools.count()


import opml

import outlinetypes
typeOutline = outlinetypes.typeOutline

import objc


import CactusTools
NSURL2str = CactusTools.NSURL2str
readURL = CactusTools.readURL
getFileProperties = CactusTools.getFileProperties
setFileProperties = CactusTools.setFileProperties
datestring_nsdate = CactusTools.datestring_nsdate

import CactusVersion

import CactusOutlineDoc

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType

CactusDocumentTypesSet = CactusDocumentTypes.CactusDocumentTypesSet
CactusDocumentXMLBasedTypesSet = CactusDocumentTypes.CactusDocumentXMLBasedTypesSet


import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException



import Foundation
NSObject = Foundation.NSObject
NSAutoreleasePool = Foundation.NSAutoreleasePool
NSMutableDictionary = Foundation.NSMutableDictionary
NSMakeRange = Foundation.NSMakeRange
NSAttributedString = Foundation.NSAttributedString
NSThread = Foundation.NSThread
NSNotificationCenter = Foundation.NSNotificationCenter
NSNotification = Foundation.NSNotification

NSMutableArray = Foundation.NSMutableArray

NSNotFound = Foundation.NSNotFound
NSIndexSet = Foundation.NSIndexSet
NSMutableIndexSet = Foundation.NSMutableIndexSet

NSNumber = Foundation.NSNumber

NSURL = Foundation.NSURL

NSMakePoint = Foundation.NSMakePoint

import AppKit
NSUserDefaults = AppKit.NSUserDefaults
NSApplication = AppKit.NSApplication
NSOpenPanel = AppKit.NSOpenPanel
NSDocumentController = AppKit.NSDocumentController

NSMenu = AppKit.NSMenu

NSPasteboard = AppKit.NSPasteboard
#NSAlert = AppKit.NSAlert
#NSPopUpButtonWillPopUpNotification = AppKit.NSPopUpButtonWillPopUpNotification

NSWorkspace = AppKit.NSWorkspace

#NSWorkspaceDidMountNotification = AppKit.NSWorkspaceDidMountNotification
#NSWorkspaceDidUnmountNotification = AppKit.NSWorkspaceDidUnmountNotification
#NSWorkspaceWillUnmountNotification = AppKit.NSWorkspaceWillUnmountNotification
#NSImage = AppKit.NSImage
#NSFont = AppKit.NSFont
#NSFontAttributeName = AppKit.NSFontAttributeName
#NSForegroundColorAttributeName = AppKit.NSForegroundColorAttributeName
#NSColor = AppKit.NSColor

NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString

#NSBitmapImageRep = AppKit.NSBitmapImageRep
#NSPICTFileType = AppKit.NSPICTFileType
#NSTIFFFileType = AppKit.NSTIFFFileType

NSTableView = AppKit.NSTableView
NSText = AppKit.NSText

# the characters to test against
NSBackspaceCharacter = AppKit.NSBackspaceCharacter
NSDeleteCharacter = AppKit.NSDeleteCharacter
NSCarriageReturnCharacter = AppKit.NSCarriageReturnCharacter
NSEnterCharacter = AppKit.NSEnterCharacter
NSTabCharacter = AppKit.NSTabCharacter
NSBackTabCharacter = AppKit.NSBackTabCharacter

NSDownArrowFunctionKey = AppKit.NSDownArrowFunctionKey
NSLeftArrowFunctionKey = AppKit.NSLeftArrowFunctionKey
NSRightArrowFunctionKey = AppKit.NSRightArrowFunctionKey
NSUpArrowFunctionKey = AppKit.NSUpArrowFunctionKey
NSUpTextMovement = AppKit.NSUpTextMovement


# text movements
NSReturnTextMovement = AppKit.NSReturnTextMovement
NSTabTextMovement = AppKit.NSTabTextMovement
NSBacktabTextMovement = AppKit.NSBacktabTextMovement
NSIllegalTextMovement = AppKit.NSIllegalTextMovement
NSCancelTextMovement = AppKit.NSCancelTextMovement
NSDownTextMovement = AppKit.NSDownTextMovement


# modifiers
# shift lock
NSAlphaShiftKeyMask = AppKit.NSAlphaShiftKeyMask

# shift key
NSShiftKeyMask = AppKit.NSShiftKeyMask

# control
NSControlKeyMask = AppKit.NSControlKeyMask

# alt
NSAlternateKeyMask = AppKit.NSAlternateKeyMask

# cmd
NSCommandKeyMask = AppKit.NSCommandKeyMask

# F
NSFunctionKeyMask = AppKit.NSFunctionKeyMask

NSDeviceIndependentModifierFlagsMask = AppKit.NSDeviceIndependentModifierFlagsMask


# undo manager constants
NSChangeDone = AppKit.NSChangeDone
NSChangeUndone = AppKit.NSChangeUndone
NSChangeCleared = AppKit.NSChangeCleared
NSChangeReadOtherContents = AppKit.NSChangeReadOtherContents
NSChangeAutosaved = AppKit.NSChangeAutosaved

# printing
NSPrintOperation = AppKit.NSPrintOperation



import PyObjCTools
import PyObjCTools.NibClassBuilder
extractClasses = PyObjCTools.NibClassBuilder.extractClasses
AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass


extractClasses("OutlineEditor")
extractClasses("TableEditor")
extractClasses("NodeEditor")


# simple dict for opening outline nodes

# to be used, not now
g_opmplnodetypes = {
    # typename: (urlname, openfunction)
    'blogpost': ('url', ),
    'code': (),
    'howto': (),
    'html': (),
    'include': (),
    'link': (),
    'outline': (),
    'photo': (),
    'redirect': (),
    'river': (),
    'rss': (),
    'scripting2Post': (),
    'thumbList':()
    }

g_preview_extensions = ("pdf ai ps epi eps epsf epsi "
                        "tiff tif "
                         "crw cr2 nef raf orf mrw srf dcr arw pef raw mos"
                         "dng xbm exr bmp gif ico jpg jpeg jpe thm pict pct "
                         "png qtif tga targa sgi psd pntg fpx fax jfx jfax icns jp2 "
                         "pic hdr ")
g_preview_extensions = g_preview_extensions.split()

g_qtplayer_extensions = ("aac aifc aiff aif au ulw snd caf gsm kar mid smf midi "
                         "mp3 swa wav 3gp 3g2 amc avi vfw dif dv fli mp2 m1s m75 "
                         "m15 m2p mpg mpeg mp4 mpg4 mqv qtz mov qt qtl rtsp sd2 "
                         "sdp sml m1a mpa mpm m1v m2v m4a m4p m4b m4v amr cdda "
                         "dvd atr sdv pls qmed ")
g_qtplayer_extensions = g_qtplayer_extensions.split()


def open_photo( url, open_=True ):
    """opens 2nd biggest picture"""
    print "Outline.open_photo( %s )" % repr(url)

    defaults = NSUserDefaults.standardUserDefaults()
    cache = False
    try:
        cache = bool(defaults.objectForKey_( u'optCache'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)

    s = CactusTools.readURL( NSURL.URLWithString_( url ) )

    #
    d = opml.photo_from_string( s )
    
    # sortedSizes contains all picture sizes in descensing order
    # first pict will be max size. size large is usually good but 
    # not always present
    
    # so we pick the second biggest pict, except when there's only
    # one pict, then the first
    if d['sortedSizes']:
        # make a pick
        if len(d['sortedSizes']) > 1:
            s, idx = d['sortedSizes'][1]
        else:
            s, idx = d['sortedSizes'][0]
        # grab the picture record

        picture = d['sizes'][idx]

        workspace= NSWorkspace.sharedWorkspace()

        url = d['urlFolder'] + picture['fname']

        nsurl = NSURL.URLWithString_( url )

        # if opened from cache, open in preview
        # else in safari since preview can't urlopen
        target = u'com.apple.Safari'
        if cache:
            target = u'com.apple.Preview'
            nsurl = CactusTools.cache_url( nsurl, None )
        else:
            target = u'com.apple.Safari'

        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                [ nsurl ],
                target,
                0,
                None )


# TODO: change parameter to node!
def open_node( url, nodeType=None, open_=True, supressCache=False ):
    print "Outline.open_node()"


    # pdb.set_trace()
    defaults = NSUserDefaults.standardUserDefaults()
    cache = False
    try:
        cache = bool(defaults.objectForKey_( u'optCache'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)

    appl = NSApplication.sharedApplication()
    appdelg = appl.delegate()
    workspace= NSWorkspace.sharedWorkspace()
    
    url = cleanupURL( url )
    surl = os.path.splitext( url )[1]
    surl = surl.replace( '.', '', 1)
    surl = surl.lower()
    
    nsurl = NSURL.URLWithString_( url )
    
    if nodeType == "OPML" or url.endswith(".opml"):
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusOPMLType )
    elif nodeType == "RSS" or url.endswith(".rss"):
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusRSSType )
    elif nodeType == "XML" or url.endswith(".xml"):
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusXMLType )
    elif nodeType == "HTML" or url.endswith(".html"):
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusHTMLType )
            workspace.openURL_( nsurl )

        # workspace.openURL_( nsurl )
    elif nodeType == "hook":
        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                [ nsurl ],
                u'com.apple.itunes',
                0,
                None )
    elif surl in g_qtplayer_extensions or nodeType == "QTPL":
        # qtplayer can do http:
        if cache and not supressCache:
            nsurl = CactusTools.cache_url( nsurl, surl )
        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                [ nsurl ],
                u'com.apple.quicktimeplayer',
                0,
                None )

    elif surl in g_preview_extensions:
        if nsurl.isFileURL():
            if open_:
                workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                    [ nsurl ],
                    u'com.apple.Preview',
                    0,
                    None )
        else:
            # preview can't do http so open it in the std browser:
            if cache:
                nsurl = CactusTools.cache_url( nsurl, surl )
            if open_:
                workspace.openURL_( nsurl )
    else:
        if cache:
            nsurl = CactusTools.cache_url( nsurl, surl )
        if open_:
            workspace.openURL_( nsurl )

def handleEventReturnKeyOV_Event_( ov, event ):
    pass


class KWOutlineView(AutoBaseClass):
    """Subclass of NSOutlineView; to catch keys."""

    def awakeFromNib(self):
        self.editSession = False
        # manual en- & disabling menu items
        #pdb.set_trace()
        self.clipboardRoot = OutlineNode("Clipboard root", "", None, typeOutline, None)
        menu = NSMenu.alloc().initWithTitle_( u"" )
        menu.setDelegate_(self)
        menu.addItemWithTitle_action_keyEquivalent_( u"Include", "contextMenuInclude:", u"")
        menu.addItemWithTitle_action_keyEquivalent_( u"Python Copy", "copySelectionPython:", u"")
        menu.addItemWithTitle_action_keyEquivalent_( u"Node Copy", "copySelectionNodes:", u"")
        menu.addItemWithTitle_action_keyEquivalent_( u"Node paste", "pasteSelectionNodes:", u"")

        # copySelectionPython_
        menu.setAutoenablesItems_(False)
        self.setMenu_(menu)
        
    #
    # context menu
    #
    def menuForEvent_(self, theEvent):
        """This makes the selection include the right-click row"""
        row = self.rowAtPoint_( self.convertPoint_fromView_(theEvent.locationInWindow(), None ))
        if row != -1:
            self.selectRow_byExtendingSelection_(row, True)
        return super( KWOutlineView, self).menuForEvent_(theEvent)

    def validateMenuItem_(self, sender):
        row = self.selectedRow()
        print "KWOutlineView.validateMenuItem_( %s )   row(%s)" % (repr(sender), repr(row))
        return True

    def menuNeedsUpdate_(self, sender):
        print "KWOutlineView.menuNeedsUpdate_()" % repr(sender)

    def copySelectionPython_(self, sender):
        print "KWOutlineView.copySelectionPython_()"
        # pdb.set_trace()
        row = self.clickedRow()
        selection = self.getSelectionItems()
        result = []
        for contextItem in selection:
            result.append( contextItem.copyPython() )
        s = pprint.pformat(result)
        pb = NSPasteboard.generalPasteboard()
        pb.declareTypes_owner_( [AppKit.NSStringPboardType,], self )
        pb.setString_forType_(s, AppKit.NSStringPboardType)
        
    def copySelectionNodes_(self, sender):
        print "KWOutlineView.copySelectionPython_()"
        # pdb.set_trace()
        selection = self.getSelectionItems()
        result = []
        for contextItem in selection:
            self.clipboardRoot.addChild_( contextItem.copyNodesWithRoot_(self.clipboardRoot) )
    
    def pasteSelectionNodes_(self, sender):
        # pdb.set_trace()
        selection = self.getSelectionItems()
        if not selection:
            return
        item = selection[0]
        idx = item.siblingIndex()
        parent = item.parent
        
        def setRoot(item, root):
            item.rootNode = root
            for child in item.children:
                child.rootNode = root
                setRoot(child, root)

        def addChildren( item, target):
            pass

        for child in self.clipboardRoot.children:
            idx += 1
            parent.addChild_atIndex_(child, idx)
            setRoot( child, parent.rootNode)
        self.clipboardRoot.children.removeAllObjects()
        self.reloadData()
        self.setNeedsDisplay_( True )


    def contextMenuInclude_(self, sender):
        print "KWOutlineView.contextMenuInclude_()"
        # check selection; if right-click in selectio: use selection
        # else use clicked row only
        row = self.clickedRow()
        #print "CLICKED ROW:", repr(row)
        #return
        #if row >=0 and not self.isRowSelected_(row):
        #    selection = [ self.itemAtRow_(row) ]
        #else:
        selection = self.getSelectionItems()

        for contextItem in selection:

            if not contextItem:
                continue

            if contextItem.noOfChildren() > 1:
                continue

            attributes = contextItem.getValueDict()
            theType = attributes.get("type", "")
            url = attributes.get("url", "")
            url = cleanupURL( url )
            if theType in ( 'include', 'outline', 'thumbList', 'code', 'thumbListVarCol',
                            'thumbList', 'blogpost', 'link'):
    
                d = None
                try:
                    d = opml.opml_from_string( readURL( NSURL.URLWithString_( url ), CactusOPMLType ) )
                except OPMLParseErrorException, err:
                    print traceback.format_exc()
                    print err
    
                if d:
                    root = CactusOutlineDoc.openOPML_( d )
                    for node in root.children:
                        if node.name == u"body":
                            for i in node.children:
                                contextItem.addChild_(i)
                                node.removeChild_(i)
                            break
                    # do I really need to kill the link?
                    #
                    # attrs = contextItem.getValueDict()
                    # attrs.pop( u"url" )
                    # attrs.pop( u"type" )
                    # contextItem.setValue_( attrs )
                    #
                    del root
                    del d
        self.reloadData()
        self.setNeedsDisplay_( True )


    #
    # cell editor notifications
    #
    def textDidBeginEditing_(self, aNotification):
        print "KWOutlineView.textDidBeginEditing_()"
        """Notification."""
        self.editSession = True

        userInfo = aNotification.userInfo()

        # textMovement = userInfo.valueForKey_( str("NSTextMovement") ).intValue()
        super( KWOutlineView, self).textDidBeginEditing_(aNotification)
        #self.window().makeFirstResponder_(self)


    def textDidChange_(self, aNotification):
        # print "KWOutlineView.textDidChange_()"
        """Notification."""
        self.editSession = True
        userInfo = aNotification.userInfo()
        # print "EDITOR:", self.currentEditor()
        #textMovement = userInfo.valueForKey_( u"NSTextMovement" ).intValue()
        #print "TextMovement: '%i'" % textMovement
        
        # pp(aNotification)
        super( KWOutlineView, self).textDidChange_(aNotification)
        #self.window().makeFirstResponder_(self)
        

    def textDidEndEditing_(self, aNotification):
        """Notification. Text editing ended."""

        # print "KWOutlineView.textDidEndEditing_()"

        if kwlog and kwdbg:
            print "Edit END"
        userInfo = aNotification.userInfo()
        if kwlog and kwdbg:
            pp(userInfo)
        #textMovement = userInfo.valueForKey_( str("NSTextMovement") ).intValue()

        cancelled = False
        returnContinue = False

        # hm, i want to continue editing with a new node if a return is pressed
        # it looks like the cell editor handles return and enter as the same.

        textMovement = userInfo.valueForKey_( u"NSTextMovement" ).intValue()
        print "TextMovement: '%i'" % textMovement, 

        # check for table/outline editing modes here
        
        returnInfo = NSMutableDictionary.dictionaryWithDictionary_(userInfo)

        # NSCancelTextMovement
        if textMovement == NSReturnTextMovement:
            print "RETURN MOVEMENT"
            returnContinue = True
            newTextActionCode = NSNumber.numberWithInt_(NSDownTextMovement)
            returnInfo.setObject_forKey_( newTextActionCode, str("NSTextMovement"))
            aNotification = NSNotification.notificationWithName_object_userInfo_(
                        aNotification.name(),
                        aNotification.object(),
                        returnInfo)

        elif textMovement == NSCancelTextMovement:
            print "CANCEL MOVEMENT"
            cancelled = True
            newTextActionCode = NSNumber.numberWithInt_(NSOtherTextMovement)
            returnInfo.setObject_forKey_( newTextActionCode, str("NSTextMovement"))
            aNotification = NSNotification.notificationWithName_object_userInfo_(
                        aNotification.name(),
                        aNotification.object(),
                        returnInfo)
        else:
            print "UNHANDLED MOVEMENT"
        # finish current cell
        super( KWOutlineView, self).textDidEndEditing_(aNotification)

        if returnContinue:
            self.window().makeFirstResponder_(self)
            # pdb.set_trace()
            selRow = self.getSelectedRowIndex()
            item = self.itemAtRow_(selRow)
            
            if item:
                last = item.isLast()
                if last:
                    # we are at the end of the outline
                    createNode(self, item, startEditing=True)
                else:
                    row = self.rowForItem_( item.next() )
                    # s = NSIndexSet.indexSetWithIndex_( row )
                    #self.selectRowIndexes_byExtendingSelection_(s, False)
                    self.reloadData()
                    self.editColumn_row_withEvent_select_(0, row, None, True)
                return 
        if cancelled:
            self.editSession = False
            self.reloadData()
            self.window().makeFirstResponder_(self)

    def cancelOperation_(self, sender):
        if self.currentEditor():
            # self.abortEditing()
            self.validateEditing()
        # We lose focus so re-establish
        self.window().makeFirstResponder_(self)

    def setWindowStatus_(self, status):
        model = self.delegate().controller
        model.txtWindowStatus.setStringValue_( unicode(status) )
        

    #
    # event capture
    #
    def keyDown_(self, theEvent):
        """Catch events for the outline and tableviews. """

        eventCharacters = theEvent.characters()
        eventModifiers = int(theEvent.modifierFlags())
        eventCharNum = ord(eventCharacters)

        mykeys = (NSBackspaceCharacter,
                  NSDeleteCharacter,

                  NSCarriageReturnCharacter,
                  NSEnterCharacter,

                  NSTabCharacter,
                  NSBackTabCharacter,

                  ord(NSUpArrowFunctionKey),
                  ord(NSDownArrowFunctionKey),
                  ord(NSLeftArrowFunctionKey),
                  ord(NSRightArrowFunctionKey) )

        # tab has       0x09/0x00100
        # shift tab has 0x19/0x20102
        # alt   tab has 0x09/0x80120
        # shftalttab    0x19/0xa0122
        # ctrl up 0xf700 0xa40101
        # NSDownArrowFunctionKey
        # NSLeftArrowFunctionKey
        # NSRightArrowFunctionKey
        # NSUpArrowFunctionKey
        # NSUpTextMovement
        #
        # NSBacktabTextMovement
        # NSCancelTextMovement
        # NSDownTextMovement
        # NSIllegalTextMovement
        # NSLeftTextMovement
        # NSOtherTextMovement
        # NSReturnTextMovement
        # NSRightTextMovement
        # NSTabTextMovement
        # NSUpTextMovement

        # unused, just a scribbled idea
        dispatch ={

            None: {
                NSBackspaceCharacter: (),
                NSDeleteCharacter: (),
                NSCarriageReturnCharacter: ()
            },

            NSCommandKeyMask: {},
            NSShiftKeyMask: {},
            NSAlternateKeyMask: {},
            NSControlKeyMask: {}
        }

        if kwlog and 0: #kwdbg:
            print "Key: ", hex(eventCharNum), hex(eventModifiers)

        editor = self.currentEditor()
        if editor:
            print "EDITOR:", editor

        if eventCharNum not in mykeys:
            super(KWOutlineView, self).keyDown_( theEvent )
            return None

        delg = self.delegate()
        # did we swallow the event or does it need propagation?
        consumed = False

        #
        cmdShiftAlt = NSCommandKeyMask | NSShiftKeyMask | NSAlternateKeyMask

        # filter out other stuff
        eventModifiers &= NSDeviceIndependentModifierFlagsMask

        ###########################################################################
        #
        # Deleting
        if eventCharNum in (NSBackspaceCharacter, NSDeleteCharacter):
            if kwlog and kwdbg:
                print "DELETE KEY HANDLED"

            # while editing, will be handled elsewhere
            # outline: delete selection (saving to a pasteboard stack) TBD
            # table: delete selection (saving to a pasteboard stack) Tables will be deleted in the future
            deleteNodes(self, selection=True)

            # deselect all or find a good way to select the next item
            delg.markDirty()
            self.deselectAll_( None )

        ###########################################################################
        #
        # Create new node
        elif eventCharNum == NSCarriageReturnCharacter:
            if eventModifiers & NSShiftKeyMask:
                if kwlog and kwdbg:
                    print "SHIFT Return"
            else:
                if kwlog and kwdbg:
                    print "KEY: Return"
                # open new line and start editing

                # TODO: if already editing, start new line, continue editing

                #
                sel = self.getSelectedRow()
                createNode(self, sel)
                consumed = True

        ###########################################################################
        #
        # Enter
        elif eventCharNum == NSEnterCharacter:
            # cmd+alt enter
            # cmd enter
            # cmd shift enter
            # cmd alt shift enter

            if eventModifiers & (cmdShiftAlt | NSControlKeyMask):

                appl = NSApplication.sharedApplication()
                appdelg = appl.delegate()
                workspace= NSWorkspace.sharedWorkspace()

                ###################################################################
                #
                # Control (Alt) Enter
                if eventModifiers & NSControlKeyMask:


                    ###############################################################
                    #
                    # Control Alt Enter
                    #
                    # open a node
                    #
                    #
                    # This stuff needs serious refactoring. Opening nodes was and still
                    # is a great idea but this ad hoc implementation has too many
                    # repetitions and logic holes.
                    #
                    # A separate function that analyses the node, perhaps sets a menu,
                    # and opens it should do the trick.
                    #
                    if eventModifiers & NSAlternateKeyMask:

                        # get node selection
                        items = self.getSelectionItems()

                        # do the selection
                        for item in items:
                            name = item.name

                            url = u""

                            #
                            # make a handler here
                            #
                            # opml, html, rss, js, xml(generic)
                            #
                            # for generic xml make getOPML a getXML with params
                            #
                            
                            # in a table or in html

                            if name == 'link':
                                d = item.getValueDict()
                                type = d.get('type', '')
                                href = d.get('href', '')
                                url = cleanupURL( href )
                                nodetype = None
                                # some of the mediatypes listed at en.wikipedia.org
                                if type == u"application/rss+xml":
                                    nodetype = "RSS"
                                elif type == u"application/opml+xml":
                                    nodetype = "RSS"
                                elif type == u"application/atom+xml":
                                    nodetype = "RSS"
                                elif type == u"application/xhtml+xml":
                                    nodetype = "HTML"
                                elif type == u"application/xml":
                                    # perhaps xml, perhaps opml, perhaps rss
                                    if "rss" in title.lower():
                                        nodetype = "RSS"
                                    elif "outline" in title.lower():
                                        nodetype = "OPML"
                                    else:
                                        nodetype = "XML"
                                if not url.startswith( 'http' ) :
                                    root = item.rootNode
                                    ctrl = root.controller
                                    urlbase = "NONE"
                                    if ctrl != None:
                                        urlbase = ctrl.nsurl.baseURL()
                                        if not urlbase:
                                            urlbase = ctrl.nsurl.absoluteString()
                                        else:
                                            urlbase = urlbase.absoluteString()
                                        urlbase = urlbase + url
                                        url = urlbase
                                    print repr(urlbase)
                                open_node( url, nodetype )

                            elif name in ('url', 'htmlUrl', 'xmlUrl', 'xmlurl'):
                                #
                                # FIXING HACK
                                # url = item.value
                                url = item.displayValue
                                url = cleanupURL( url )
                                open_node( url )

                            # in an outline
                            else:
                                #
                                v = item.getValueDict()
                                theType = v.get("type", "")
                                url = ""
                                if 'url' in v:
                                    url = v.get("url", "")
                                elif 'link' in v:
                                    url = v.get("link", "")
                                elif 'URL' in v:
                                    url = v.get("URL", "")
                                
                                url = cleanupURL( url )
                                if theType == "blogpost":
                                    if not url:
                                        url = v.get("urlTemplate", "")
                                        url = cleanupURL( url )
                                    if url:
                                        open_node( url )
                                elif theType in ( 'redirect', ):
                                    open_node( url, "HTML" )

                                elif theType in ( 'howto', 'html', 'include', 'outline',
                                                  'redirect', 'thumbList',
                                                  'thumbListVarCol', 'code'):
                                    open_node( url )

                                elif theType in ('link', ):
                                    nodeType=None
                                    if "opml.radiotime.com" in url:
                                        nodeType = "OPML"
                                    open_node( url, nodeType )

                                elif theType in ('audio', ):
                                    # pdb.set_trace()

                                    # 
                                    # make this it's own function
                                    #
                                    # see urllib._urlopener, 
                                    #
                                    # sometimes the stream is indirected several layers...

                                    audiourl, info = urllib.urlretrieve( url )
                                    faudio = open(audiourl)
                                    url = faudio.read()
                                    url = url.strip('\r\n')
                                    faudio.close()
                                    # baseurl, ext = os.path.splitext(url)
                                    if '\n' in url:
                                        url = url.split('\n')[0]
                                    open_node( url, "hook", supressCache=True)

                                elif theType == "photo":
                                    url = v.get("xmlUrl", "")
                                    # pdb.set_trace()
                                    open_photo( url )

                                elif theType == "rssentry":
                                    enc = v.get("enclosure", "")
                                    url1 = ""
                                    if enc:
                                        url1, rest = enc.split('<<<')

                                    url2 = v.get("link", "")
                                    url2 = cleanupURL( url2 )
                                    if url1:
                                        open_node( url1 )
                                    if url2:
                                        open_node( url2 )

                                elif theType == "river":
                                    opmlUrl = v.get("opmlUrl", "")
                                    if opmlUrl:
                                        opmlUrl = cleanupURL( opmlUrl )
                                        appdelg.newOutlineFromURL_Type_( opmlUrl,
                                                                         CactusOPMLType )

                                elif theType == "rss":
                                    # open website
                                    htmlUrl = v.get("htmlUrl", "")
                                    htmlUrl = cleanupURL( htmlUrl )
                                    if htmlUrl:
                                        open_node( htmlUrl, nodeType="HTML")

                                    # open rss
                                    xmlUrl = v.get("xmlUrl", "")
                                    xmlUrl = cleanupURL( xmlUrl )
                                    if xmlUrl:
                                        open_node( xmlUrl, nodeType="RSS")

                                elif theType == "scripting2Post":
                                    open_node( url, nodeType="HTML")
                                else:
                                    print "Unhandled Node open\ntype: '%s'\nurl: '%s'" %(repr(theType), repr(url))

                            consumed = True

                    ###############################################################
                    #
                    # Control Enter
                    else:
                        # ctrl enter
                        items = self.getSelectionItems()
                        for item in items:
                            if item.value:
                                title = item.name

                                # stop it if we are in a table
                                if item.typ not in outlinetypes.hierarchicalTypes:
                                    continue

                                # build a new document from current attributes
                                root = OutlineNode(u"__root__", u"", None,
                                                   outlinetypes.typeOutline, None)
                                for t in item.value:
                                    if isinstance(t, tuple):
                                        name, value = t
                                    elif isinstance(t, str):
                                        name = u"value"
                                        value = t
                                    node = OutlineNode(name, value, root, outlinetypes.typeTable, root)
                                    root.addChild_(node)

                                appdelg.newTableWithRoot_fromNode_(root, item)
                        consumed = True

                ###################################################################
                #
                # not control but some combination of cmdShiftAlt
                else:
                    pass

                ###################################################################
                #
                #
                if eventModifiers & NSShiftKeyMask:
                    if eventModifiers & NSAlternateKeyMask:
                        if kwlog and kwdbg:
                            print "SHIFT ALT Enter"
                    else:
                        if kwlog and kwdbg:
                            print "SHIFT Enter"
                        
                        nodes = visitOutline(delg.root)
                        consumed = True
            
            #######################################################################
            #
            # Enter
            else:
                # start editing

                # current row
                index = self.getSelectedRowIndex()

                #
                edited = self.editedRow()
                if edited == -1:
                    if index != -1:
                        #start editing
                        if kwdbg:
                            print "Edit START"
                        self.editColumn_row_withEvent_select_(0, index, None, True)
                    else:
                        # empty selection
                        pass
                else:
                    # editing in progreess with row 'edited'
                    # how to stop?
                    pass
        
        ###########################################################################
        #
        # Outdenting
        elif eventCharNum == NSBackTabCharacter:
            # shift tab has it's own character
            if eventModifiers & NSShiftKeyMask:
                if kwdbg:
                    print "SHIFT Tab"
                # dedent selection
                
                if delg.typ in outlinetypes.hierarchicalTypes:
                    # get selected rows
                    sel = self.getSelectionItems()
                    
                    # working from the end
                    sel.reverse()
                    
                    # dedent each row one level
                    for item in sel:
                        item.moveLeft()
                    consumed = True
                    delg.markDirty()
                    self.reloadData()
        
        ###########################################################################
        #
        # Indenting
        elif eventCharNum == NSTabCharacter:
            # indent selection

            # get selected rows
            if delg.typ in outlinetypes.hierarchicalTypes:
                sel = self.getSelectionItems()
                # indent each row one level
                postselect = set()
                for item in sel:
                    parent = item.parent
                    previous = item.previous()

                    # ignore command if item is first Child
                    if previous != -1:
                        item.retain()
                        previous.addChild_( item )
                        parent.removeChild_(item)
                        item.release()
                        postselect.add(item)
                        self.expandItem_( previous )
                        self.reloadItem_reloadChildren_( previous, True )
                        self.reloadItem_reloadChildren_( parent, True )
                postselect = [self.rowForItem_(i) for i in postselect]
                self.selectItemRows_( postselect )
                
                consumed = True
                delg.markDirty()
                self.reloadData()


        ###########################################################################
        #
        # Move selection up
        elif eventCharNum == ord(NSUpArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:
                # get selected rows
                items = self.getSelectionItems()
                moveSelectionUp(self, items)
                #
                delg.markDirty()
                self.reloadData()

                selection = [self.rowForItem_(i) for i in items]
                if selection:
                    self.selectItemRows_( selection )
            
                self.setNeedsDisplay_( True )
                consumed = True


        ###########################################################################
        #
        # Move selection up
        elif eventCharNum == ord(NSDownArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:
                # get selected rows
                items = self.getSelectionItems()
                moveSelectionDown(self, items)
                #
                delg.markDirty()
                self.reloadData()
                
                selection = [self.rowForItem_(i) for i in items]
                if selection:
                    self.selectItemRows_( selection )
            
                self.setNeedsDisplay_( True )
                consumed = True

        ###########################################################################
        # ctrl-left
        # select parent node
        #
        # ctrl-alt-left
        # select parent node and colapse all
        #
        elif eventCharNum == ord(NSLeftArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:

                # get selected rows
                items = self.getSelectionItems()
                selection = []
                collapse = eventModifiers & NSAlternateKeyMask
                for item in items:
                    parent = item.parent
                    if parent:
                        selection.append( parent )
                if selection:
                    if collapse:
                        for item in selection:
                            self.collapseItem_collapseChildren_(item, True)
                    selection = [self.rowForItem_(i) for i in selection]
                    self.selectItemRows_( selection )

                    # make first selection item visible
                    if selection:
                        first = selection[0]
                        rowRect = self.rectOfRow_( first )
                        self.scrollRowToVisible_( first )

                self.setNeedsDisplay_( True )
                consumed = True

        ###########################################################################
        # ctrl-right
        # select children
        #
        # ctrl-alt-right
        # select children and expand
        #
        elif eventCharNum == ord(NSRightArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:

                # get selected rows
                items = self.getSelectionItems()

                selection = []

                expandChildren = eventModifiers & NSAlternateKeyMask

                for item in items:
                    children = item.children
                    if children:
                        self.expandItem_( item )
                        selection.extend( children )
                if len(selection) > 0:
                    if expandChildren:
                        for child in selection:
                            if self.isExpandable_( child ):
                                self.expandItem_expandChildren_(child, False)
                    # convert items back to indices
                    selection = [self.rowForItem_(i) for i in selection]
                    self.selectItemRows_( selection )

                    # make first selection item visible
                    if selection:
                        first = selection[0]
                        rowRect = self.rectOfRow_( first )
                        ##
                        # an attempt to scroll top selection 
                        #
                        # x, y = rowRect.origin.x, rowRect.origin.y
                        # selfRect = self.bounds()
                        # deltaH = selfRect.size.height / 2
                        # y += deltaH
                        # pdb.set_trace()
                        # print "ScrollTo_( %s, %s )" % (repr(x), repr(y))
                        # self.superview().scrollToPoint_( NSMakePoint( x, y ) )
                        self.scrollRowToVisible_( first )
            
                self.setNeedsDisplay_( True )
                consumed = True
        if not consumed:
            super(KWOutlineView, self).keyDown_( theEvent )


    #
    # utilities
    #
    def getSelectionItems(self):
        """The actual nodes of the current selection are returned."""
        sel = self.selectedRowIndexes()
        n = sel.count()
        result = []
        if not n:
            return result
        next = sel.firstIndex()
        result.append( self.itemAtRow_(next) )

        for i in range(1, n):
            next = sel.indexGreaterThanIndex_(next)
            result.append( self.itemAtRow_(next) )
        return result

    def getSelectedRow(self):
        sel = self.getSelectedRowIndex()
        if sel == -1:
            return sel
        item = self.itemAtRow_(sel)
        return item

    def getSelectedRowIndex(self):
        sel = self.selectedRow()
        return sel

    def selectItemRows_( self, itemIndices ):
        s = NSMutableIndexSet.indexSet()
        for i in itemIndices:
            if i >= 0:
                s.addIndex_( i )
        self.selectRowIndexes_byExtendingSelection_(s, False)

    def selectRowItem_(self, item):
        index = self.rowForItem_( item )
        s = NSIndexSet.indexSetWithIndex_( index )
        self.selectRowIndexes_byExtendingSelection_(s, False)

    def expandSelection_(self, sender):
        items = self.getSelectionItems()
        for item in items:
            self.expandItem_(item)

    def expandAllSelection_(self, sender):
        items = self.getSelectionItems()
        for item in items:
            self.expandItem_expandChildren_(item, True)

    def collapseSelection_(self, sender):
        items = self.getSelectionItems()
        for item in items:
            self.collapse_(item)

    def collapseAllSelection_(self, sender):
        items = self.getSelectionItems()
        for item in items:
            self.collapseItem_collapseChildren_(item, True)

    def collapseToParent_(self, sender):
        items = self.getSelectionItems()
        parents = []
        for item in items:
            parents.append( item.parent )
            self.collapseItem_collapseChildren_(item, True)
        for parent in parents:
            self.collapseItem_collapseChildren_(parent, True)
        postselect = [self.rowForItem_(item) for item in parents]
        self.selectItemRows_( postselect )


class NiceError(object):
    """Wrapper for an exception so we can display it nicely in the browser."""

    def __init__(self, exc_info):
        self.exc_info = exc_info

    def __repr__(self):
        from traceback import format_exception_only
        lines = format_exception_only(*self.exc_info[:2])
        assert len(lines) == 1
        error = lines[0].strip()
        return "*** error *** %s" %error

#
# Nodewalk
#
def stdAction( node, level ):
    # Debugging HACK
    s = "  " * level
    s = s + unicode(node)
    n = str(node.retainCount())
    n = n.ljust(4)
    s = n + s
    print s.encode("utf-8")
    

def visitOutline(startnode, startlevel=0, depthFirst=False, action=stdAction):
    # Debugging HACK
    action(startnode, startlevel)
    if len(startnode.children) > 0:
        for p in startnode.children:
            visitOutline(p, startlevel+1, depthFirst, action)
    return

# UNUSED
def dfid(T,children,callback=stdAction):
    # some ActiveState snippet
    def visit(node,i):
        if i == 0:
            callback(node, i)
        else:
            for c in node.children:
                visit(c,i-1)
    i = 0
    while 1:
        visit(T,i)
        i += 1


#
# Outline Document Model
#
class OutlineViewDelegateDatasource(NSObject):

    """This is a delegate as well as a data source for NSOutlineViews."""
    #
    # instantiated from AppDelegate
    #
    # no bindings
    #
    # ivars
    #
    #   typ
    #   parentNode
    #   root
    #   controller
    #   restricted
    
    def init(self):
        self = super(OutlineViewDelegateDatasource, self).init()
        if not self:
            return None
        self.typ = None
        self.parentNode = None
        self.root = None
        self.controller = None
        self.document = None
        
        # not yet used; it's an idea for rss documents to constrain node movements.
        self.restricted = False
        return self

    def dealloc(self):
        if kwdbg:
            print "MODEL_release"
        #if self.parentNode:
        #    self.parentNode.release()
        if self.root:
            self.root.release()
        #if self.controller:
        #    self.controller.release()
        #if self.document:
        #    self.document.release()
        super(OutlineViewDelegateDatasource, self).dealloc()

    def initWithObject_type_parentNode_(self, obj, typ, parentNode):
        self = self.init()

        if not self:
            return None

        self.typ = typ
        self.parentNode = parentNode

        if not isinstance(obj, OutlineNode):
            obj = OutlineNode(unicode(obj), "", None, outlinetypes.typeOutline, None)
        self.root = obj
        return self


    def markDirty(self):
        if self.document != None:
            self.document.updateChangeCount_( NSChangeDone )

    def setController_(self, controller):
        self.controller = controller

    def reloadData_(self, item):
        if self.controller:
            self.controller.reloadData_(item)

    def isSubEditor(self):
        return self.parentNode != None

    def appendToRoot_Value_(self, name, value):
        node = OutlineNode(name, value, self.root, self.typ, self.root)
        self.root.addChild_( node )
        self.reloadData_( node )
        # need to reload all so the new node gets recognized
        idx = self.controller.outlineView.rowForItem_( node )
        return idx

    #
    # tableview delegate
    #
    # numberOfRowsInTableView:
    def tableView_objectValueForTableColumn_row_(self, tv, column, row):
        c = col.identifier()
        item = self.root.childAtIndex_( row )
        if c == u"type":
            # return item.displayType
            return item.displayType
        elif c == u"value":
            return item.displayValue
        elif c == u"name":
            return item.displayName
        elif c == u"comment":
            return item.displayComment


    def numberOfRowsInTableView_(self, tv):
        return self.root.children.count()


    def outlineViewColumnDidResize_(self, aNotification):
        userInfo = aNotification.userInfo()
        column = userInfo.valueForKey_( u"NSTableColumn" )
        oldWidth = userInfo.valueForKey_( u"NSOldWidth" ).intValue()
        newWidth = column.width()
        # print "COL: '%s' changed from: %i  to  %i" % (column.identifier(),
        #                                               oldWidth, newWidth)
    
    def tableViewColumnDidResize_(self, aNotification):
        # for some reaon only th outlineView delegate is called. Even for tables
        pass
    
    #
    # NSOutlineViewDataSource  methods
    #
    def outlineView_numberOfChildrenOfItem_(self, view, item):
        if not item:
            item = self.root
        return item.noOfChildren()
    
    def outlineView_child_ofItem_(self, view, child, item):
        if not item:
            item = self.root
        return item.childAtIndex_( child )
    
    def outlineView_isItemExpandable_(self, view, item):
        if not self.typ in outlinetypes.hierarchicalTypes:
            return False
        return item.noOfChildren() > 0

    def outlineView_objectValueForTableColumn_byItem_(self, view, col, item):
        c = col.identifier()
        if not item:
            item = self.root
        if c == u"type":
            # return item.displayType
            return item.type
        elif c == u"value":
            return item.displayValue
        elif c == u"name":
            # return item.displayName
            return item.name
        elif c == u"comment":
            # return item.displayComment
            return item.comment


    def outlineView_setObjectValue_forTableColumn_byItem_(self, view, value, col, item):
        c = col.identifier()
        if not item:
            # item = self.root
            return
        if c == u"type":
            pass #return item.displayType
        elif c == u"value":
            if value != item.displayValue:
                # if it has a parentNode it's edited attributes
                if self.parentNode != None:
                    name = item.name
                    self.parentNode.updateValue_( (name, unicode(value)) )
                item.setValue_( value )
                self.markDirty()
        elif c == u"name":
            if value != item.name:
                item.setName_(value)
                self.markDirty()
        elif c == u"comment":
            if value != item.comment:
                item.setComment_(value)
                self.markDirty()


    # delegate method

    # see below
    def XXXXoutlineView_shouldEditTableColumn_item_(self, view, col, item):
        return item.editable


    def outlineView_heightOfRowByItem_(self, ov, item):
        lineheight = 14
        maxLines = self.controller.rowLines

        if not self.controller.variableRowHeight:
            return lineheight

        lines = min( maxLines, int(item.maxHeight))
        lines = max(1, lines)
        return lines * lineheight

    def outlineView_shouldEditTableColumn_item_(self, ov, col, item):
        c = col.identifier()
        if c == u"type":
            return False
        return True

    # UNUSED
    def ovUpdateItem_Key_Value_(self, item, key, value):
        # update a single key value pair in the value dict
        pass

    def outlineViewSelectionDidChange_( self, aNotification ):
        # print "outlineViewSelectionDidChange_()"

        if aNotification:
            ov = aNotification.object()
            if not isinstance(ov, KWOutlineView):
                ov = False
        if ov:
            sel = ov.selectedRowIndexes()
            n = sel.count()

            if n == 1:
                # show node info
                next = sel.firstIndex()
                item = ov.itemAtRow_(next)
                level = ov.levelForRow_( next )
                s = "%i  %s  rowHeight: %i" % (level, item.name, item.maxHeight)
            else:
                # show selection info
                s = u"%i nodes selected" % (n,)
            ov.setWindowStatus_( s )


    #def outlineView_didClickTableColumn_(self, view, tablecolumn):
    #    pass

    # interresting delegate methods:
    # Delegate
    # outlineView:dataCellForTableColumn:item:
    # outlineView:didClickTableColumn:
    # outlineView:heightOfRowByItem:
    # outlineView:isGroupItem: 10.5
    # outlineView:shouldCollapseItem:
    # outlineView:shouldExpandItem:
    # outlineView:shouldSelectItem:
    # outlineView:shouldSelectTableColumn:
    # outlineView:shouldShowCellExpansionForTableColumn:item: 10.5
    # outlineView:shouldTrackCell:forTableColumn:item: 10.5
    # outlineView:toolTipForCell:rect:tableColumn:item:mouseLocation:
    # outlineView:willDisplayCell:forTableColumn:item:
    # outlineView:willDisplayOutlineCell:forTableColumn:item:
    # outlineViewColumnDidMove:
    # outlineViewColumnDidResize:
    # outlineViewItemDidCollapse:
    # outlineViewItemDidExpand:
    # outlineViewItemWillCollapse:
    # outlineViewItemWillExpand:
    # outlineViewSelectionDidChange:
    # outlineViewSelectionIsChanging:
    # selectionShouldChangeInOutlineView:

    # Notifications
    # NSOutlineViewColumnDidMoveNotification
    # NSOutlineViewColumnDidResizeNotification
    # NSOutlineViewItemDidCollapseNotification
    # NSOutlineViewItemDidExpandNotification
    # NSOutlineViewItemWillCollapseNotification
    # NSOutlineViewItemWillExpandNotification
    # NSOutlineViewSelectionDidChangeNotification
    # NSOutlineViewSelectionIsChangingNotification

class NodeValue(object):
    """NodeValue is a helper with the value column which in some cases has
    a dual existence as a string or as a table.
    """

    def __init__(self, value):
        if type(value) != list:
            if type(value) in (str, unicode, NSString, bool, int,
                               NSMutableString, objc.pyobjc_unicode):
                value = self.listFromDisplayValue( value )
            elif isinstance(value, dict):
                value = self.listFromDictionary( value )
            else:
                print "BOGATIVE VALUETYPE:", type(value)
                
        if type(value) != list:
            print "VALUE is not list"

        self.value = value
        self.typ = len(value) > 1

    def displayValue(self):
        # maxlen = max([len(k) for k in self.value.keys()])
        l = []
        if not isinstance(self.value, list):
            print "VALUE is not list"
            print repr(self.value)
        for t in self.value:
            k, v = t
            if k != "":
                l.append(u"%s:\t%s" % (k, v) )
            else:
                l.append(u"%s" % (v,))
        return '\n'. join(l)

    def listFromDisplayValue(self, displayValue):
        try:
            lines = displayValue.split('\n')
        except AttributeError,err:
            print err
            lines = [ unicode(displayValue) ]

        l = []
        for line in lines:
            if line.count(':\t') == 0:
                k = u""
                v = line
            else:
                k, v = line.split(':\t', 1)
            l.append( (k, v) )
            d = {}
            for item in l:
                k, v = item
                if k in d:
                    d[k] = d[k] + u'\n' + v
                else:
                    d[k] = v
            l = d.items()
        return l

    def listFromDictionary(self, value):
        l = []
        for k, v in value.items():
            l.append( (k,v) )
        return l

    def isSingleValue(self):
        if len(self.value) == 1:
            if self.value[0][0] in (u"", u"value"):
                return True
        return False

    def isMultiValue(self):
        return not self.isSingleValue()

#
# Outline
#

class OutlineNode(NSObject):

    """Wrapper class for items to be displayed in the outline view."""

    # We keep references to all child items (once created). This is
    # neccesary because NSOutlineView holds on to OutlineNode instances
    # without retaining them. If we don't make sure they don't get
    # garbage collected, the app will crash. For the same reason this
    # class _must_ derive from NSObject, since otherwise autoreleased
    # proxies will be fed to NSOutlineView, which will go away too soon.

    # attributes of OutlineNode:
    # name
    # value
    # comment
    # type
    # parent
    # children
    #
    # displayName
    # displayValue
    # displayComment
    # displayType
    #
    
    #
    # to be added
    #
    # nodeAttributes

    # that's the deal
    def __new__(cls, *args, **kwargs):
        return cls.alloc().init()

    def __init__(self, name, obj, parent, typ, rootNode):

        # this is outlinetype, not valueType
        self.typ = typ

        self.maxHeight = 1
        self.setParent_(parent)
        self.rootNode = rootNode

        # debugging
        self.nodenr = counter.next()

        self.setName_( name )
        self.setValue_( obj )

        self.setAttributes_( obj )
        self.setComment_( "" )

        self.children = NSMutableArray.arrayWithCapacity_( 0 )
        self.editable = True

        self.maxHeight = self.setMaxLineHeight()

        self.controller = None
        if rootNode != None:
            self.controller = rootNode.controller

        # leave this here or bad things will happen
        self.retain()

    def __repr__(self):
        return "<OutlineNode(%i, name='%s')" % (self.nodenr, self.name)

    def dealloc(self):
        print "NODE DEALLOC:", self.nodenr
        pp(self.__dict__)
        self.children.release()
        #self.root.release()
        self.root = None
        #self.rootNode.release()
        super(OutlineNode, self).dealloc()

        
    def setMaxLineHeight(self):
        maxVal = self.calcAttributesHeight()
        l = self.lineHeight( self.name )
        if l > maxVal:
            maxVal = l
        l = self.lineHeight( self.comment )
        if l > maxVal:
            maxVal = l
        return maxVal

    def setAttributes_(self, attrs):
        d = {}
        t = type(attrs)
        if t in (str, unicode, NSString, bool, int, long,
                 NSMutableString, objc.pyobjc_unicode):
            # stringtype
            d[ u"" ] = unicode(attrs)
        elif t in (list, tuple):
            #listtype
            for item in attrs:
                key, val = item
                key = unicode(key)
                val = unicode(val)
                d[ key ] = val
        elif t in (dict, feedparser.FeedParserDict):
            for key in attrs:
                val = unicode(attrs[key])
                key = unicode(key)
                d[ key ] = val
        else:
            # ???
            pass
        self.attributes = d


    def lineHeight(self, val):
        lines = 0
        try:
            lines += val.count( u"\r" )
            lines += val.count( u"\n" )
        except Exception, err:
            print "\n\nERROR in lineHeight()"
            tb = unicode(traceback.format_exc())
            print err
            print
            print tb
            print
        vallength = len( val )
        if vallength > 100:
            pass
        lines += int(math.ceil(vallength / 55.0))
        return max(1, lines)

    def calcAttributesHeight(self):
        lineheight = 0
        for key in self.attributes:
            lineheight += self.lineHeight( self.attributes[ key ] )
        return lineheight


    def setParent_(self, parent):
        self.parent = parent

    #
    def setName_(self, value):
        self.name = value
        s = unicode(value)
        if kwdbg:
            self.displayName = u"(%i)  - %s" % (self.nodenr, s)
        else:
            self.displayName = u"%s" % (s,)

    def setValue_(self, value):
        if value in (u"", {}, [], None, False):
            self.value = [(u"",u"")]
            self.displayValue = u""
            self.type = u"String"
        else:
            nv = NodeValue( value )
            self.value = nv.value
            
            if nv.isMultiValue():
                self.type = u"Attributes"
            else:
                self.type = u"String"
            self.displayValue = nv.displayValue()
        self.displayType = self.type

    # UNUSED
    def addValue_(self, nameValue):
        self.value.append( nameValue )
        self.setValue_( self.value )
        r = self.findRoot()
        m = r.model
        m.reloadData_(self)

    # used in attribute editor
    def removeValue_(self, nameValue):
        # repeated myself; copied from updateValue_ ...
        newname, newvalue = nameValue
        updated = idx = False
        for i,t in enumerate(self.value):
            k, v = t
            if k == newname:
                idx = i
                break
        if idx >= 0:
            self.value.pop(idx)
            updated = True

        if updated:
            self.setValue_( self.value )
            r = self.findRoot()
            m = r.model
            m.reloadData_(self)
        return updated

    # used in attribute editor
    def updateValue_(self, nameValue):
        newname, newvalue = nameValue
        updated = idx = None
        for i,t in enumerate(self.value):
            k, v = t
            if k == newname:
                idx = i
                break

        if idx != None:
            self.value.pop(idx)
            self.value.insert(idx, nameValue)
            updated = True

        if not updated:
            self.value.append( nameValue )
        self.setValue_( self.value )

        r = self.findRoot()
        m = r.model
        m.reloadData_(self)

    # essential
    def getValueDict(self):
        """Create a dictionary from the value."""
        if len(self.value) == 0:
            return {}
        elif len(self.value) == 1:
            if self.value[0][0] == "":
                if self.value[0][1] != "":
                    return {'value': self.value[0][1] }
                else:
                    return {}
            else:
                return {self.value[0][0]: self.value[0][1] }
        else:
            d = {}
            for t in self.value:
                k, v = t
                d[k] = v
            return d

    def setComment_(self, comment):
        self.comment = comment
        self.displayComment = unicode( self.comment )
        self.maxHeight = self.setMaxLineHeight()

    #
    def noOfChildren(self):
        return self.children.count()
    
    #
    def addChild_(self, child):
        # retain: child+1
        if isinstance(child, OutlineNode):
            if kwlog and False:
                print "OutlineNode.addChild_", child
            child.setParent_(self)
            self.children.addObject_( child )
            # child.release()

    def addChild_atIndex_(self, child, index):
        # retain: child+1
        self.children.insertObject_atIndex_( child, index)
        if kwdbg:
            print "addChild_atIndex_setParent", child
        child.setParent_(self)
        # child.release()

    def childAtIndex_( self, index ):
        # delegeate child getter
        if index <= self.children.count():
            return self.children.objectAtIndex_( index )
        return None

    def removeChild_(self, child):
        # retain: child-1
        # perhaps this should return the orphan

        # root is always outlineType
        index = self.children.indexOfObject_(child)
        if index != NSNotFound:
            self.children.removeObjectAtIndex_( index )
            return index
        return False

    def isEditable(self):
        return self.editable

    def isExpandable(self):
        return self.children.count() > 0

    def isRoot(self):
        return self.parent == None

    # this is used too excessively, make it a var
    def findRoot(self):
        if self.rootNode != None:
            return self.rootNode
        s = self
        while True:
            if s.parent == None:
                if s != self:
                    self.rootNode = s
                return s
            s = s.parent

    def pathFromRoot(self):
        l = []
        s = self
        while True:
            if s.parent == None:
                return l
            s = s.parent
            l.append( s.name )

    #
    # node math
    #
    def siblingCount(self):
        """How many are there me and my siblings?"""
        if self.parent == None:
            # i am root
            return -1
        p = self.parent
        # should work for tables too since root node is outline type
        l = p.children.count()
        return l

    def siblingIndex(self):
        """What is my index in this sibling group?"""
        if self.parent == None:
            # i am root
            return -1
        p = self.parent
        index = p.children.indexOfObject_(self)
        if index == NSNotFound:
            return -1
        return index

    def previousIndex(self):
        """The index of the sibling before me."""
        n = self.siblingIndex()
        if n >= 0:
            if n > 0:
                # not first, so there's one before me
                return n-1

            # is first
            return -1

        # no parent
        return -1

    def nextIndex(self):
        """The index of the sibling after me."""
        n = self.siblingIndex()
        if n >= 0:
            l = self.siblingCount()
            if n < l - 1:
                # last index is allowed since it will be appended to the array
                return n+1
            # is last
            # perhaps left here
            return -1
        # no parent
        return n

    def isFirst(self):
        """Am I the first sibling."""
        n = self.siblingIndex()
        return n == 0

    def isLast(self):
        """Am I the last sibling."""
        n = self.siblingIndex()
        l = self.siblingCount()
        return n == (l - 1)

    def next(self):
        """Return my immediate next sibling or -1."""
        n = self.nextIndex()
        if n >= 0:
            return self.parent.children.objectAtIndex_(n)
        return -1
            
    def previous(self):
        """Return my immediate previous sibling or -1."""
        n = self.previousIndex()
        if n >= 0:
            return self.parent.children.objectAtIndex_(n)
        return -1

    def isChildOf_(self, other):
        p = self
        i = 0
        while not p.isRoot():
            p = p.parent
            i += 1
            if p == other:
                return i
        return -1

    def findFirstChildWithName_(self, name):
        for child in self.children:
            if child.name == name:
                return child

    #
    # node movements
    #
    def makeChildOf_(self, other):
        """Move self to be last child of other."""

        # parent needs to be saved since it's lost in addChild_
        parent = self.parent
        if parent == None:
            return -1
        other.addChild_(self)
        parent.removeChild_(self)

    def moveLeft(self):
        # noveAfterParent
        """For dedenting."""
        if not self.typ in outlinetypes.hierarchicalTypes:
            return
        parent = self.parent
        if parent == None:
            return -1

        grandparent = parent.parent
        if parent.isLast():
            # append after parent
            self.makeChildOf_(grandparent)
            #grandparent.addChild_(self)
            #parent.removeChild_(self)

        else:
            # insert after parent
            parentIndex = parent.siblingIndex()
            grandparent.addChild_atIndex_(self, parentIndex+1)
            parent.removeChild_(self)

    def moveRight(self):
        # make self child of previous
        if not self.typ in outlinetypes.hierarchicalTypes:
            return

        previous = self.previous()
        if previous != -1:
            self.makeChildOf_(previous)

    def copyPython(self):
        result = []
        start = {
            'name': self.name,
            'value': self.getValueDict(),
            'comment': self.comment,
            'children': result}
        for i in self.children:
            result.append( i.copyPython() )
        return start

    def copyNodesWithRoot_(self, root):
        # pdb.set_trace()
        result = []
        # pdb.set_trace()
        node = OutlineNode(self.name, self.getValueDict(), root, typeOutline, None)
        node.setComment_( self.comment )
        for i in self.children:
            node.addChild_( i.copyNodesWithRoot_(root) )
        return node


#
# node editing
#
# TODO: deleting does not update correctly.
# line stays visible in parent view. needsRedraw_?
#
def deleteNodes(ov, nodes=(), selection=False):
    if selection:
        sel = ov.getSelectionItems()
    else:
        sel = nodes
    delg = ov.delegate()
    parentNode = delg.parentNode
    for item in sel:
        p = item.parent
        deleted = True
        if parentNode:
            deleted = parentNode.removeValue_( (item.name, item.value) )
        if deleted:
            p.removeChild_( item )
            delg.markDirty()
    ov.reloadData()

def createNode(ov, selection, startEditing=True):
    # pdb.set_trace()
    # create node at selection and start editing
    
    # open new line and start editing
    # if already editing, start new line, continue editing
    delg = ov.delegate()
    typ = delg.typ
    if selection == -1:
        rowIndex = ov.delegate().appendToRoot_Value_(u"", u"")
    else:
        p = selection.parent
        root = p.rootNode
        node = OutlineNode(u"", "", p, typ, root)
        targetIdx = selection.nextIndex()
        if targetIdx == -1:
            p.addChild_( node )
        else:
            p.addChild_atIndex_( node, targetIdx )
        ov.reloadData()
        ov.selectRowItem_( node )
        rowIndex = ov.rowForItem_( node )
        consumed = True
    
    if startEditing:
        s = NSIndexSet.indexSetWithIndex_( rowIndex )
        ov.selectRowIndexes_byExtendingSelection_(s, False)
        ov.reloadData()
        ov.editColumn_row_withEvent_select_(0, rowIndex, None, True)
    delg.markDirty()


def moveSelectionUp(ov, items):
    delg = ov.delegate()
    for item in items:
        # move item before previous
        #  get grandparent
        #  insert at index of previous
        # pdb.set_trace()
        previous = item.previous()
        if previous == -1:
            return
        parent = item.parent
        if parent == None:
            return
        previousIndex = previous.siblingIndex()
        item.retain()

        # don't swap these two
        parent.removeChild_( item )
        parent.addChild_atIndex_(item, previousIndex)

        delg.markDirty()


def moveSelectionDown(ov, items):
    #
    # this really needs to be sorted down; use indices
    # otherwise there will be overlapping moves destroying
    # sortorder
    delg = ov.delegate()
    items.reverse()
    for item in items:
        # retain item 0
        parent = item.parent
        if parent == None:
            return
        next = item.next()
        if next == -1:
            return

        item.retain()
        parent.removeChild_( item )

        # after removal of item, nexitndex changes
        nextIndex = next.nextIndex()
        if nextIndex == -1:
            parent.addChild_( item )
        else:
            parent.addChild_atIndex_(item, nextIndex)
        item.release()
        delg.markDirty()


def moveSelectionLeft(ov, selection):
    pass

def moveSelectionRight(ov, selection):
    pass

def cleanupURL( url ):
    # lots of URLs contain spaces, &, '

    url = NSURL2str(url)

    purl = urlparse.urlparse( url )
    purl = list(purl)
    path = purl[2]
    path = urllib.unquote( 'http://' + path )
    try:
        path = urllib.quote( path )
    except KeyError, err:
        print "ERROR"
        print repr(path)
        print err
    path = path[9:]
    purl[2] = path
    purl = urlparse.urlunparse( purl )
    purl = unicode(purl)
    return purl
