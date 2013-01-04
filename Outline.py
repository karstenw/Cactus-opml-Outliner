
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
messagecount = itertools.count()

import opml

import outlinetypes

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


import AppKit
NSUserDefaults = AppKit.NSUserDefaults
NSApplication = AppKit.NSApplication
NSOpenPanel = AppKit.NSOpenPanel
NSDocumentController = AppKit.NSDocumentController

NSMenu = AppKit.NSMenu

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

#NSMakePoint = AppKit.NSMakePoint
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


def open_photo( url, open_=True, cache=False ):
    f = urllib.FancyURLopener()
    fob = f.open(url)
    s = fob.read()
    fob.close()
    d = opml.photo_from_string( s )
    photolist = []
    fulllist = [ NSURL.URLWithString_( url ) ]
    dl = []
    isFile = False

    for k, v in d.items():
        nsurl = NSURL.URLWithString_( v )
        isFile = nsurl.isFileURL()

        if k.startswith("large"):
            photolist.append( nsurl )
            #if not k.startswith("original"):
            fulllist.append( nsurl )

    if photolist:
        workspace= NSWorkspace.sharedWorkspace()
        # target = u'com.apple.Preview'
        # if 1: #not isFile:
        target = u'com.apple.Safari'
        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                photolist,
                target,
                0,
                None )

    if fulllist and cache:
        for nsurl in fulllist:
            CactusTools.cache_url( nsurl )


# TODO: change parameter to node!
def open_node( url, nodeType=None, open_=True, cache=False ):

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
        workspace.openURL_( nsurl )

    elif surl in g_qtplayer_extensions:
        # qtplayer can do http:
        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                [ nsurl ],
                u'com.apple.quicktimeplayer',
                0,
                None )
        if cache:
            CactusTools.cache_url( nsurl )

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
            if open_:
                workspace.openURL_( nsurl )
            if cache:
                CactusTools.cache_url( nsurl )
    else:
        if open_:
            workspace.openURL_( nsurl )
        if cache:
            CactusTools.cache_url( nsurl )


class KWOutlineView(AutoBaseClass):
    """Subclass of NSOutlineView; to catch keys."""

    def awakeFromNib(self):
        # manual en- & disabling menu items
        #pdb.set_trace()
        self.menu = NSMenu.alloc().initWithTitle_( u"" )
        self.menu.setDelegate_(self)
        self.menu.addItemWithTitle_action_keyEquivalent_( u"Include", "contextMenuInclude:", u"")
        self.menu.setAutoenablesItems_(False)
        self.setMenu_(self.menu)
        
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
        print "contextrow:", row        
        return True

    def menuNeedsUpdate_(self, sender):
        print "Menu(%s) needs update." % repr(sender)

    def contextMenuInclude_(self, sender):
        print "Contextaction"

        # check selection; if right-click in selectio: use selection
        # else use clicked row only
        row = self.clickedRow()
        #print "CLICKED ROW:", repr(row)
        #return
        #if row >=0 and not self.isRowSelected_(row):
        #    selection = [ self.itemAtRow_(row) ]
        #else:
        selection = self.getSelectionItems()

        # pdb.set_trace()

        for contextItem in selection:

            if not contextItem:
                continue

            if contextItem.noOfChildren < 1:
                continue

            attributes = contextItem.getValueDict()
            theType = attributes.get("type", "")
            url = attributes.get("url", "")
            url = cleanupURL( url )
            if theType in ( 'include', 'outline', 'thumbList', 'code', 'thumbListVarCol',
                            'thumbList'):
    
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
                    del d
        self.reloadData()
        self.setNeedsDisplay_( True )


    #
    # cell editor notifications
    #
    def textDidBeginEditing_(self, aNotification):
        """Notification."""
        userInfo = aNotification.userInfo()

        # textMovement = userInfo.valueForKey_( str("NSTextMovement") ).intValue()
        super( KWOutlineView, self).textDidBeginEditing_(aNotification)
        #self.window().makeFirstResponder_(self)


    def textDidChange_(self, aNotification):
        """Notification."""
        userInfo = aNotification.userInfo()

        # pp(userInfo)
        super( KWOutlineView, self).textDidChange_(aNotification)
        #self.window().makeFirstResponder_(self)
        

    def textDidEndEditing_(self, aNotification):
        """Notification."""
        # pdb.set_trace()
        if kwlog and kwdbg:
            print "Edit END"
        userInfo = aNotification.userInfo()
        if kwlog and kwdbg:
            pp(userInfo)
            # pdb.set_trace()
        #textMovement = userInfo.valueForKey_( str("NSTextMovement") ).intValue()

        cancelled = False

        # hm, i want to continue editing with a new node if a return is pressed
        # it looks like the cell editor handles return and enter as the same.

        # check for table/outline editing modes here
        if userInfo.valueForKey_( u"NSTextMovement" ).intValue() == NSReturnTextMovement:
            cancelled = True
            newInfo = NSMutableDictionary.dictionaryWithDictionary_(userInfo)
            newTextActionCode = NSNumber.numberWithInt_(NSCancelTextMovement)
            newInfo.setObject_forKey_( newTextActionCode, str("NSTextMovement"))
            aNotification = NSNotification.notificationWithName_object_userInfo_(
                        aNotification.name(),
                        aNotification.object(),
                        newInfo)
        super( KWOutlineView, self).textDidEndEditing_(aNotification)
        if cancelled:
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

        if kwlog and kwdbg:
            print "Key: ", hex(eventCharNum), hex(eventModifiers)

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
            self.deselectAll_( None )

        ###########################################################################
        #
        # Create new node
        elif eventCharNum == NSCarriageReturnCharacter:
            #pdb.set_trace()
            if eventModifiers & NSShiftKeyMask:
                if kwlog and kwdbg:
                    print "SHIFT Return"
            else:
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

            # pdb.set_trace()

            if eventModifiers & (cmdShiftAlt | NSControlKeyMask):

                # dive down or up
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
                            
                            # in a table
                            if name in ('url', 'htmlUrl', 'xmlUrl', 'xmlurl', 'link'):
                                #
                                # FIXING HACK
                                # url = item.value
                                # pdb.set_trace()
                                url = item.displayValue
                                url = cleanupURL( url )
                                open_node( url )

                            # in an outline
                            else:
                                #
                                v = item.getValueDict()
                                theType = v.get("type", "")
                                url = v.get("url", "")
                                url = cleanupURL( url )

                                if theType == "blogpost":
                                    if not url:
                                        url = v.get("urlTemplate", "")
                                        url = cleanupURL( urlTemplate )
                                    if url:
                                        open_node( url )

                                elif theType in ( 'howto', 'html', 'include', 'outline',
                                                  'redirect', 'thumbList',
                                                  'thumbListVarCol', 'link', 'code'):
                                    open_node( url )

                                elif theType == "photo":
                                    url = v.get("xmlUrl", "")
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
                        # pdb.set_trace()
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
                                                   outlinetypes.typeOutline)
                                for t in item.value:
                                    if isinstance(t, tuple):
                                        name, value = t
                                    elif isinstance(t, str):
                                        name = u"value"
                                        value = t
                                    node = OutlineNode(name, value, root, outlinetypes.typeTable)
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
                        previous.addChild_( item )
                        parent.removeChild_(item)
                        postselect.add(item)
                        self.expandItem_( previous )
                        self.reloadItem_reloadChildren_( previous, True )
                postselect = [self.rowForItem_(i) for i in postselect]
                self.selectItemRows_( postselect )
                
                consumed = True
                self.reloadData()


        ###########################################################################
        #
        # Move selection up
        elif eventCharNum == ord(NSUpArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:
                # pdb.set_trace()
                # get selected rows
                items = self.getSelectionItems()
                moveSelectionUp(self, items)
                #
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
                # pdb.set_trace()
                # get selected rows
                items = self.getSelectionItems()
                moveSelectionDown(self, items)
                #
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
            
                self.setNeedsDisplay_( True )
                consumed = True

        if 1: # do always
            sel = self.selectedRowIndexes()
            n = sel.count()
            id_ = messagecount.next()
            c = 0
            if consumed:
                c = 1
            if n == 1:
                # show node info
                next = sel.firstIndex()
                item = self.itemAtRow_(next)
                level = self.levelForRow_( next )
                s = "%i  %s  rowHeight: %i msg: %i cons: %i" % (level, item.name, item.maxHeight, id_, c)
            else:
                # show selection info
                s = u"%i nodes selected msg: %i cons: %i" % (n, id_, c)
            self.setWindowStatus_( s )
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
        # pdb.set_trace()
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


class NiceError:
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
    # pdb.set_trace()
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
    #   dirty
    #   restricted


    def init(self):
        self = super(OutlineViewDelegateDatasource, self).init()
        if not self:
            return None
        self.typ = None
        self.parentNode = None
        self.root = None
        self.controller = None
        self.dirty = 0

        # not yet used; it's an idea for rss documents to constrain node movements.
        self.restricted = False
        return self


    def initWithObject_type_parentNode_(self, obj, typ, parentNode):

        self = self.init()

        if not self:
            return None

        self.typ = typ
        self.parentNode = parentNode

        if not isinstance(obj, OutlineNode):
            obj = OutlineNode(unicode(obj), "", None, outlinetypes.typeOutline)
        self.root = obj
        return self


    def release():
        if kwdbg:
            print "MODEL_release"
        self.root.release()
        super(OutlineViewDelegateDatasource, self).release()


    def setController_(self, controller):
        self.controller = controller

    def reloadData_(self, item):
        if self.controller:
            self.controller.reloadData_(item)

    def isSubEditor(self):
        return self.parentNode != None

    def appendToRoot_Value_(self, name, value):
        n = OutlineNode(name, value, self.root, self.typ)
        self.root.addChild_( n )
        self.reloadData_( None )
        idx = self.controller.outlineView.rowForItem_(n)
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
        # pdb.set_trace()
        c = col.identifier()
        if not item:
            item = self.root
        if c == u"type":
            pass #return item.displayType
        elif c == u"value":
            # if it has a parentNode it's edited attributes
            if self.parentNode != None:
                name = item.name
                self.parentNode.updateValue_( (name, unicode(value)) )
                
            item.setValue_( value )
            self.dirty += 1
        elif c == u"name":
            item.setName_(value)
            self.dirty += 1
        elif c == u"comment":
            item.setComment_(value)
            self.dirty += 1


    # delegate method
    def outlineView_shouldEditTableColumn_item_(self, view, col, item):
        return item.editable


    def outlineView_heightOfRowByItem_(self, ov, item):
        lineheight = 14
        maxLines = self.controller.rowLines

        if not self.controller.variableRowHeight:
            return lineheight

        lines = min( maxLines, int(item.maxHeight))
        lines = max(1, lines)
        return lines * lineheight

    # UNUSED
    def ovUpdateItem_Key_Value_(self, item, key, value):
        # update a single key value pair in the value dict
        pass

    #def outlineView_didClickTableColumn_(self, view, tablecolumn):
    #    pass

    # interresting delegate methods:
    # Delegate
    # outlineView:dataCellForTableColumn:item:
    # outlineView:didClickTableColumn:
    # outlineView:heightOfRowByItem:
    # outlineView:isGroupItem: 10.5
    # outlineView:shouldCollapseItem:
    # outlineView:shouldEditTableColumn:item:
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
        # pdb.set_trace()
        if type(value) != list:
            if type(value) in (str, unicode, NSString, bool, int,
                               NSMutableString, objc.pyobjc_unicode):
                value = self.listFromDisplayValue( value )
            elif isinstance(value, dict):
                # pdb.set_trace()
                value = self.listFromDictionary( value )
            else:
                print "BOGATIVE VALUETYPE:", type(value)
                
        if type(value) != list:
            # pdb.set_trace()
            print "VALUE is not list"

        self.value = value
        self.typ = len(value) > 1

    def displayValue(self):
        # maxlen = max([len(k) for k in self.value.keys()])
        l = []
        if not isinstance(self.value, list):
            # pdb.set_trace()
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
            # pdb.set_trace()
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

class NodeAttributes(object):
    """Hold the attributes associated with an outline node.
    
    Will replace Nodevalue
    """
    def __init__(self):
        self.attributes = {}

    def fromNameValues(self, nameValueList):
        for t in nameValueList:
            k, v = t
            self.attributes[k] = v

    def asstring(self):
        """Return the attributes as a string.
        
        key:\tvalue\n
        """
        l = []
        keys = self.attributes.keys()
        keys.sort()
        for key in keys:
            k, v = key, self.attributes[key]
            l.append(u"%s:\t%s" % (k, v) )
        s = u'\n'.join( l )
        return s

    def astuplelist(self):
        """Return the attributes as a list of tuples.
        
        [ (k,v), (k,v), ...]
        """
        l = []
        keys = self.attributes.keys()
        keys.sort()
        for key in keys:
            k, v = key, self.attributes[key]
            l.append( (k,v) )
        return l

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
        # "Pythonic" constructor
        # print "OutlineNode.__new__() called"
        return cls.alloc().init()

    def __repr__(self):
        return "<OutlineNode(%i, name='%s')" % (self.nodenr, self.name)

    def __init__(self, name, obj, parent, typ, rootNode=None):
        # pdb.set_trace()

        # this is outlinetype, not valueType
        self.typ = typ
        self.setParent_(parent)
        self.maxHeight = 1
        # debugging
        self.nodenr = counter.next()

        self.setName_( name )
        self.setValue_( obj )

        # self.setNodeAttributes( obj )

        self.rootNode = rootNode

        self.setAttributes_( obj )
        self.setComment_( "" )

        self.children = NSMutableArray.arrayWithCapacity_( 10 )
        self.editable = True

        self.maxHeight = self.setMaxLineHeight()

        # leave this here or bad things will happen
        self.retain()

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
        lines = 0
        if t in (str, unicode, NSString, bool, int, long,
                 NSMutableString, objc.pyobjc_unicode):
            # stringtype
            d[ u"" ] = unicode(attrs)
            lines = 1
        elif t in (list, tuple):
            #listtype
            for item in attrs:
                key, val = item
                key = unicode(key)
                val = unicode(val)
                d[ key ] = val
                lines += self.lineHeight( val )
        elif t in (dict, feedparser.FeedParserDict):
            for key in attrs:
                val = unicode(attrs[key])
                key = unicode(key)
                d[ key ] = val
                lines += self.lineHeight( val )
        else:
            # ???
            pass
        self.attributes = d
        return lines

    def lineHeight(self, val):
        lines = 0
        try:
            lines += val.count( u"\r" )
            lines += val.count( u"\n" )
        except Exception, err:
            print "\n\nERROR in lineHeight()"
            tb = unicode(traceback.format_exc())
            # pdb.set_trace()
            print err
            print
            print tb
            print
        vallength = len( val )
        if vallength > 100:
            # pdb.set_trace()
            pass
        lines += int(math.ceil(vallength / 40.0))
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

    # switched off
    def setNodeAttributes(self, nameValueList):
        """Create new node attributes from [ (k,v), ]
        """
        self.nodeAttributes = NodeAttributes()
        if type(nameValueList) in (list,):
            self.nodeAttributes.fromNameValues( nameValueList )

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
        # pdb.set_trace()
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
        # pdb.set_trace()
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

    # UNUSED
    def compare_(self, other):
        return cmp(self.name, other.name)

    #
    def noOfChildren(self):
        return self.children.count()
    
    #
    def addChild_(self, child):
        if isinstance(child, OutlineNode):
            if kwdbg:
                print "addChild_setParent", child
            child.setParent_(self)
            self.children.addObject_( child )

    def addChild_atIndex_(self, child, index):
        # child.retain()
        self.children.insertObject_atIndex_( child, index)
        if kwdbg:
            print "addChild_atIndex_setParent", child
        child.setParent_(self)

    def childAtIndex_( self, index ):
        # delegeate child getter
        if index <= self.children.count():
            return self.children.objectAtIndex_( index )
        return None

    def removeChild_(self, child):
        # perhaps this should return the orphan

        # root is always outlineType
        index = self.children.indexOfObject_(child)
        if index != NSNotFound:
            c = self.children.objectAtIndex_( index )
            self.children.removeObjectAtIndex_( index )
            if kwdbg:
                print "removeChild_RELEASE:", c
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
        if self.rootNode:
            return self.rootNode
        s = self
        while True:
            if s.parent == None:
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
            delg.dirty += 1
    ov.reloadData()

def createNode(ov, selection, startEditing=True):
    #pdb.set_trace()
    # create node at selection and start editing
    
    # open new line and start editing
    # if already editing, start new line, continue editing
    delg = ov.delegate()
    typ = delg.typ
    if selection == -1:
        rowIndex = ov.delegate().appendToRoot_Value_(u"", u"")
    else:
        # pdb.set_trace()
        p = selection.parent
        node = OutlineNode(u"", "", selection.parent, typ)
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
    delg.dirty += 1

def moveSelectionUp(ov, items):
    delg = ov.delegate()
    for item in items:
        # move item before previous
        #  get grandparent
        #  insert at index of previous
        previous = item.previous()
        if previous == -1:
            return
        parent = item.parent
        if parent == None:
            return
        previousIndex = previous.siblingIndex()
        parent.removeChild_( item )
        parent.addChild_atIndex_(item, previousIndex)
        delg.dirty += 1

def moveSelectionDown(ov, items):
    #

    # this really needs to be sorted down; use indices
    # otherwise there will be overlapping moves destroying
    # sortorder
    delg = ov.delegate()
    items.reverse()
    # pdb.set_trace()
    for item in items:

        parent = item.parent
        if parent == None:
            return
        next = item.next()
        if next == -1:
            return
        parent.removeChild_( item )
        # pdb.set_trace()
        # after removal of item, nexitndex changes
        nextIndex = next.nextIndex()
        if nextIndex == -1:
            parent.addChild_( item )
        else:
            parent.addChild_atIndex_(item, nextIndex)
        delg.dirty += 1

def moveSelectionLeft(ov, selection):
    pass

def moveSelectionRight(ov, selection):
    pass

def cleanupURL( url ):
    # lots of URLs contain spaces, &, '

    # pdb.set_trace()
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
