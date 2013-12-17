
# -*- coding: utf-8 -*-


"""A collection of outline related stuff
"""

import sys
import os

import re

import cPickle

import traceback

import time
import datetime

import urllib
import urlparse

import math
import feedparser

import CactusVersion


kwdbg = CactusVersion.developmentversion
kwlog = CactusVersion.developmentversion

import pdb
import pprint
pp = pprint.pprint



import bs4
BeautifulSoup = bs4.BeautifulSoup

import appscript

import CactusOPML

import CactusOutlineTypes
typeOutline = CactusOutlineTypes.typeOutline

import objc


import Foundation
NSObject = Foundation.NSObject
NSAutoreleasePool = Foundation.NSAutoreleasePool
NSMutableDictionary = Foundation.NSMutableDictionary
NSMakeRange = Foundation.NSMakeRange
NSAttributedString = Foundation.NSAttributedString
NSThread = Foundation.NSThread
NSNotificationCenter = Foundation.NSNotificationCenter
NSNotification = Foundation.NSNotification

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
NSOutlineView = AppKit.NSOutlineView
NSWindowController = AppKit.NSWindowController

NSData = AppKit.NSData

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
NSLeftTextMovement = AppKit.NSLeftTextMovement
NSRightTextMovement = AppKit.NSRightTextMovement
NSUpTextMovement = AppKit.NSUpTextMovement
NSDownTextMovement = AppKit.NSDownTextMovement
NSOtherTextMovement = AppKit.NSOtherTextMovement


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

# drag and drop
NSDragOperationNone = AppKit.NSDragOperationNone
NSDragOperationCopy = AppKit.NSDragOperationCopy
NSDragOperationLink = AppKit.NSDragOperationLink
NSDragOperationGeneric = AppKit.NSDragOperationGeneric
NSDragOperationMove = AppKit.NSDragOperationMove
NSDragOperationEvery = AppKit.NSDragOperationEvery
NSDragOperationDelete = AppKit.NSDragOperationDelete

NSDragOperationAll_Obsolete = AppKit.NSDragOperationAll_Obsolete

NSOutlineViewDropOnItemIndex = AppKit.NSOutlineViewDropOnItemIndex

NSStringPboardType = AppKit.NSStringPboardType
NSFilenamesPboardType = AppKit.NSFilenamesPboardType
NSFilesPromisePboardType = AppKit.NSFilesPromisePboardType

# printing
NSPrintOperation = AppKit.NSPrintOperation


import CactusOutlineNode
OutlineNode = CactusOutlineNode.OutlineNode

import CactusTools
NSURL2str = CactusTools.NSURL2str
readURL = CactusTools.readURL
getFileProperties = CactusTools.getFileProperties
setFileProperties = CactusTools.setFileProperties
datestring_nsdate = CactusTools.datestring_nsdate
makeunicode = CactusTools.makeunicode
mergeURLs = CactusTools.mergeURLs
getURLExtension = CactusTools.getURLExtension


import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType

CactusDocumentTypesSet = CactusDocumentTypes.CactusDocumentTypesSet
CactusDocumentXMLBasedTypesSet = CactusDocumentTypes.CactusDocumentXMLBasedTypesSet


import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException


import CactusFileOpeners


DragDropCactusPboardType = "CactusKWOutlineViewPboardType"




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
                        "crw cr2 nef raf orf mrw srf dcr arw pef raw mos "
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
    print "CactusOutline.open_photo( %s )" % repr(url)

    defaults = NSUserDefaults.standardUserDefaults()
    cache = False
    try:
        cache = bool(defaults.objectForKey_( u'optCache'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)

    s = CactusTools.readURL( NSURL.URLWithString_( url ) )

    #
    d = CactusOPML.photo_from_string( s )

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
                None,
                None )


# TODO: change parameter to node!
def open_node( url, nodeType=None, open_=True, supressCache=False ):
    if kwdbg:
        print "CactusOutline.open_node()"
        pp( (url,nodeType,open_, supressCache) )

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

    basename, ext = getURLExtension( url )
    ext = ext.replace( '.', '', 1)
    ext = ext.lower()

    if ' ' in url:
        # url = url.replace(" ", "%20")
        
        nsurl = NSURL.URLWithString_( url.replace(" ", "%20" ))
    else:
        nsurl = NSURL.URLWithString_( url )
    if nodeType == "OPML" or ext == "opml":
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusOPMLType )
    elif nodeType == "RSS" or ext == "rss":
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusRSSType )
    elif nodeType == "XML" or ext == "xml":
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusXMLType )
    elif nodeType == "HTML" or ext == "html":
        if open_:
            appdelg.newOutlineFromURL_Type_( nsurl, CactusHTMLType )
            workspace.openURL_( nsurl )

    elif nodeType == "hook":
        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                [ nsurl ],
                u'com.apple.itunes',
                0,
                None,
                None )
    elif ext in g_qtplayer_extensions or nodeType == "QTPL":
        # qtplayer can do http:
        if cache and not supressCache:
            nsurl = CactusTools.cache_url( nsurl, ext )
        if open_:
            workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                [ nsurl ],
                u'com.apple.quicktimeplayer',
                # u'com.apple.QuickTimePlayerX',
                0,
                None,
                None )

    elif ext in g_preview_extensions:
        if nsurl.isFileURL():
            if open_:
                workspace.openURLs_withAppBundleIdentifier_options_additionalEventParamDescriptor_launchIdentifiers_(
                    [ nsurl ],
                    u'com.apple.Preview',
                    0,
                    None,
                    None )
        else:
            # preview can't do http so open it in the std browser:
            if cache:
                nsurl = CactusTools.cache_url( nsurl, ext )
            if open_:
                workspace.openURL_( nsurl )
    else:
        if cache:
            nsurl = CactusTools.cache_url( nsurl, ext )
        if open_:
            workspace.openURL_( nsurl )

def handleEventReturnKeyOV_Event_( ov, event ):
    pass


class KWOutlineView(NSOutlineView):
    """Subclass of NSOutlineView; to catch keys."""

    lastDrag = []

    def awakeFromNib(self):
        self.editSession = False
        # manual en- & disabling menu items
        #pdb.set_trace()
        self.clipboardRoot = OutlineNode("Clipboard root", "", None, typeOutline, None)
        menu = NSMenu.alloc().initWithTitle_( u"" )
        menu.setDelegate_(self)
        menu.addItemWithTitle_action_keyEquivalent_( u"Include",
                                                      "contextMenuInclude:", u"")
        #
        # deactivated since regular cut, copy and paste have arrived
        #
        #menu.addItemWithTitle_action_keyEquivalent_( u"Python Copy",
        #                                              "copySelectionPython:", u"")
        #menu.addItemWithTitle_action_keyEquivalent_( u"Node Copy",
        #                                              "copySelectionNodes:", u"")
        #menu.addItemWithTitle_action_keyEquivalent_( u"Node paste",
        #                                              "pasteSelectionNodes:", u"")

        menu.addItemWithTitle_action_keyEquivalent_( u"Insert Safari links",
                                                      "insertSafariLinks:", u"")
        # copySelectionPython_
        menu.setAutoenablesItems_(False)
        self.registerForDraggedTypes_([DragDropCactusPboardType])
        self.setVerticalMotionCanBeginDrag_( False )
        #self.setDraggingSourceOperationMask_forLocal_( NSDragOperationEvery, True )
        #self.setDraggingSourceOperationMask_forLocal_( NSDragOperationAll_Obsolete, False )
        
        self.setMenu_(menu)

    #
    # context menu handlers
    #
    # The initial and currently static context menu is defined in awakeFromNib
    #
    
    def menuForEvent_(self, theEvent):
        """This makes the selection include the right-click row"""
        row = self.rowAtPoint_( self.convertPoint_fromView_(
                                theEvent.locationInWindow(),
                                None ))
        if row != -1:
            s = NSIndexSet.indexSetWithIndex_( row )
            self.selectRowIndexes_byExtendingSelection_(s, True)
            # self.selectRow_byExtendingSelection_(row, True)
        return super( KWOutlineView, self).menuForEvent_(theEvent)

    def validateMenuItem_(self, sender):
        # row = self.selectedRow()
        if kwlog:
            print "KWOutlineView.validateMenuItem_( %s )" % repr(sender)
        return True

    def menuNeedsUpdate_(self, sender):
        if 0: #kwlog:
            print "KWOutlineView.menuNeedsUpdate_( %s )" % repr(sender)

    def insertSafariLinks_(self, sender):
        if kwlog:
            print "KWOutlineView.insertSafariLinks_()"
        row = self.clickedRow()
        selection = self.getSelectionItems()
        if not selection:
            return
        result = []

        item = selection[0]
        idx = item.siblingIndex()

        parent = item.parent

        safari = appscript.app("Safari.app")
        if not safari.isrunning():
            return

        src = ""
        try:
            src = safari.windows[1].current_tab.source()
            url = safari.windows[1].current_tab.URL()
        except Exception, err:
            print err
        if not src:
            return
        soup = BeautifulSoup( src )
        links = soup.find_all( 'a' )

        purl = urlparse.urlparse( url )

        listroot = OutlineNode(url, "", parent, typeOutline, item.rootNode)
        parent.addChild_atIndex_( listroot, idx+1 )

        for link in links:
            d = { 'type': 'link' }
            dest = link.get('href', False)
            if not dest:
                continue
            name = link.text
            d['name'] = name
            pdest = urlparse.urlparse( dest )
            target = mergeURLs( url, dest )
            d['url'] = target

            node = OutlineNode(name, d, listroot, typeOutline, item.rootNode)
            listroot.addChild_( node )
        self.reloadData()
        self.setNeedsDisplay_( True )


    def copySelectionPython_(self, sender):
        if kwlog:
            print "KWOutlineView.copySelectionPython_()"
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
        selection = self.getSelectionItems()
        result = []
        for contextItem in selection:
            self.clipboardRoot.addChild_(
                    contextItem.copyNodesWithRoot_(self.clipboardRoot) )

    def pasteSelectionNodes_(self, sender):
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
        if kwlog:
            print "KWOutlineView.contextMenuInclude_()"

        # TBD: check selection
        # if right-click in selection:
        #   use selection
        # else
        #   use clicked row only

        row = self.clickedRow()
        selection = self.getSelectionItems()

        importedNodes = 0
        for contextItem in selection:

            if not contextItem:
                continue

            if contextItem.noOfChildren() > 1:
                continue

            attributes = contextItem.getValueDict()
            theType = attributes.get("type", "")
            url = attributes.get("url", "")
            url = cleanupURL( url )
            if theType in ( 'include', 'outline', 'thumbList', 'code',
                             'thumbListVarCol', 'thumbList', 'blogpost', 'link'):

                d = None
                try:
                    d = CactusOPML.opml_from_string(
                                readURL( NSURL.URLWithString_( url ),
                                         CactusOPMLType ) )

                except OPMLParseErrorException, err:
                    print traceback.format_exc()
                    print err

                if d:
                    #
                    # TBD: import here to circumvent circular import
                    #
                    
                    root, type_ = CactusFileOpeners.openOPML_( d )
                    for node in root.children:
                        if node.name == u"body":
                            for i in node.children:
                                contextItem.addChild_(i)
                                node.removeChild_(i)
                                importedNodes += 1
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
        if importedNodes > 0:
            self.delegate().markDirty()

        self.reloadData()
        self.setNeedsDisplay_( True )
    
    #
    # drag and drop
    #

    #
    # drag destination
    #

    def XdraggingEntered_( self, dragInfo ):
        print "draggingEntered_"
        pboard = dragInfo.draggingPasteboard()
        mask = dragInfo.draggingSourceOperationMask()
        types = pboard.types()
        opType = NSDragOperationNone
        self.setDraggingDestinationFeedbackStyle_(1)
        if DragDropCactusPboardType in types:
            opType = NSDragOperationMove
            
            return NSDragOperationMove

        elif NSFilenamesPboardType in types:
            print "NSFilenamesPboardType entered"
            return NSDragOperationNone

            if mask & NSDragOperationLink:
                return  NSDragOperationLink

            elif mask & NSDragOperationCopy:
                return  NSDragOperationCopy
        self.setNeedsDisplay_(True)
        return NSDragOperationNone

    
    def XdraggingUpdated_( self, dragInfo ):
        #print "draggingUpdated_",
        if dragInfo.draggingSource():
            pp(dragInfo)
            return NSDragOperationMove
        else:
            print "external"
            return NSDragOperationCopy
    
    @objc.IBAction
    def XdraggingExited_( self, dragInfo ):
        print "draggingExited_"
        super(KWOutlineView, self).draggingExited_(dragInfo)

    def XprepareForDragOperation_( self, dragInfo ):
        print "KWOutlineView.prepareForDragOperation_"
        self.currentDragItems = self.getSelectionItems()
        pp( self.currentDragItems )
        # self.setNeedsDisplay_(True)
        return 1
    
    def XperformDragOperation_( self, dragInfo ):
        print "KWOutlineView.performDragOperation_"
        pboard = dragInfo.draggingPasteboard()
        successful = 0
        types = pboard.types()
        sender = dragInfo.draggingSource()
        pp(dragInfo)
        return successful

    @objc.IBAction
    def XconcludeDragOPeration_( self, dragInfo ):
        print "concludeDragOPeration_", repr(dragInfo)
        self.setNeedsDisplay_(True)


    def XsetDropItem_dropChildIndex_(self, item, index):
        print "KWOutlineView.setDropItem_dropChildIndex_(%s), %s" % (repr(item), repr(index))
        # get's called if updateDrop_ is not defined
        
        

    
    #def wantsPeriodicDraggingUpdates(self):
    #    # if present crashes at startup
    #    # perhaps try it when methods are fleshed out
    #    return False
    
    #
    # drag source
    #
    
    def XmouseDragged_(self, event):
        # from hillegass book
        pass
    
    @objc.IBAction
    def cut_(self, sender):
        self.copy_(sender)
        deleteNodes(self, selection=True)
        self.deselectAll_( None )
    
    @objc.IBAction
    def copy_(self, sender):
        pb = NSPasteboard.generalPasteboard()
        self.copyNodesToPasteboard_( pb )

    @objc.IBAction
    def paste_(self, sender):
        pb = NSPasteboard.generalPasteboard()
        pastedItems = self.readNodesFromPasteboard_parent_index_( pb, False, False )
        if pastedItems:
            self.reloadData()
            self.selectItems_(pastedItems)
    
    def copyNodesToPasteboard_( self, pb ):
        print "KWOutlineView.copyNodesToPasteboard_"
        #pdb.set_trace()
        pb.declareTypes_owner_( [DragDropCactusPboardType,
                                 NSStringPboardType],
                                 # NSFilenamesPboardType],
                                self)

        items = self.getSelectionItems()

        # pack items
        result = []
        names = []
        noduplicates = set(items)
        for item in items:
            ancestors = set(item.pathFromRoot())
            if ancestors.isdisjoint(noduplicates):
                result.append( item.copyPython())
            row = self.rowForItem_( item )
            level = self.levelForRow_( row )
            indent = u"\t" * level
            s = u"%s%s" % (indent, item.name)
            names.append( s )
        data = cPickle.dumps( result )
        l = len(data)
        nsdata = NSData.dataWithBytes_length_(data, l)

        pb.setData_forType_( nsdata, DragDropCactusPboardType)

        t = u"\n".join( names )
        s = NSString.stringWithCharacters_length_(t, len(t))
        pb.setString_forType_( s, NSStringPboardType)


    def readNodesFromPasteboard_parent_index_(self, pb, insertParent, afterIndex):
        """Insert NSData(pickle) nodes from a pasteboard.
        
        if insertParent:
            make children of parent (append)
        if afterIndex:
            insert after index
            
        - deletion of original nodes (d&d) should occur after insertion to get the
        selection right.
        
        return a set of inserted items.
        """
        if kwlog:
            print "KWOutlineView.readNodesFromPasteboard_parent_index_"
        types = pb.types()
        t = None
        mystringtype = "public.utf8-plain-text"
        if mystringtype in types:
            t = mystringtype

        if DragDropCactusPboardType in types:
            t = DragDropCactusPboardType

        if not t:
            return False

        delg = self.delegate()
        typ = delg.typ
        root = delg.root

        data = pb.dataForType_(t)
        if t == DragDropCactusPboardType:
            nodes = cPickle.loads( data.bytes().tobytes() )


        elif t == mystringtype:
            nodes = []
            s = makeunicode(data.bytes().tobytes())
            if u"\r" in s:
                r = s.split( u"\r" )
            else:
                r = s.split( u"\n" )

            for i in r:
                i = i.strip(u"\r\n\t ")
                nodes.append( { 
                    'name': i,
                    'value': u"",
                    'typ': CactusOutlineTypes.typeOutline,
                    'children': [] } )

        if not insertParent:
            selection = self.getSelectionItems()
            if selection:
                item = selection[-1]
                pasteParent = item.parent
                afterIndex = item.siblingIndex() + 1
            else:
                # append to root.children
                pasteParent = root
        else:
            pasteParent = insertParent

        itemsPasted = 0

        def doChildren( item, children ):
            for node in children:
                n = OutlineNode(node['name'], node['value'], item, node['typ'], root)
                item.addChild_( n )
                doChildren( n, node['children'])

        pastedItems = set()
        
        for node in nodes:
            # a dict per node
            n = OutlineNode(node['name'], node['value'], pasteParent, node['typ'], root)

            if afterIndex >= 0:
                pasteParent.addChild_atIndex_( n, afterIndex )
                afterIndex += 1
            elif afterIndex == -1:
                pasteParent.addChild_( n )
            elif afterIndex == False:
                pasteParent.addChild_( n )

            doChildren( n, node['children'])
            itemsPasted += 1
            pastedItems.add( n )

        self.expandItem_( pasteParent )
        self.deselectAll_( None )

        if itemsPasted > 0:
            delg.markDirty()
        return pastedItems


    def draggingSourceOperationMaskForLocal_(self, isLocal):
        print "KWoutlineView.draggingSourceOperationMaskForLocal_(%s)" % repr(isLocal)
        if isLocal:
            return NSDragOperationMove
        else:
            return NSDragOperationCopy

    def draggedImage_endedAt_operation_( self, theImage, theLocation, theOperation):
        print "KWoutlineView.draggedImage_endedAt_operation_(%s)" % theOperation
        if theOperation in (NSDragOperationDelete, NSDragOperationMove):
            # print "lastDrag:"
            # pp(KWOutlineView.lastDrag)
            #deleteNodes(self, nodes=KWOutlineView.lastDrag)
            pass
        # KWOutlineView.lastDrag = []

    #
    # cell editor notifications
    #
    def textDidBeginEditing_(self, aNotification):
        print "KWOutlineView.textDidBeginEditing_()"
        """Notification."""
        self.editSession = True

        userInfo = aNotification.userInfo()
        if userInfo:
            pp(userInfo)
        super( KWOutlineView, self).textDidBeginEditing_(aNotification)
        #self.window().makeFirstResponder_(self)


    def textDidChange_(self, aNotification):
        print "KWOutlineView.textDidChange_()"
        """Notification."""
        self.editSession = True
        userInfo = aNotification.userInfo()
        if userInfo:
            textMovement = userInfo.valueForKey_( u"NSTextMovement" ).intValue()

            # NSCancelTextMovement
            if textMovement == NSReturnTextMovement:
                print "RETURN MOVEMENT"
            elif textMovement == NSCancelTextMovement:
                print "CANCEL MOVEMENT"
            elif textMovement == NSTabTextMovement:
                print "NSTabTextMovement"
            elif textMovement == NSBacktabTextMovement:
                print "NSBacktabTextMovement"
            elif textMovement == NSLeftTextMovement:
                print "NSLeftTextMovement"
            elif textMovement == NSRightTextMovement:
                print "NSRightTextMovement"
            elif textMovement == NSUpTextMovement:
                print "NSUpTextMovement"
            elif textMovement == NSDownTextMovement:
                print "NSDownTextMovement"
            elif textMovement == NSOtherTextMovement:
                print "NSOtherTextMovement"
            elif textMovement == NSIllegalTextMovement:
                print "NSIllegalTextMovement"

        super( KWOutlineView, self).textDidChange_(aNotification)
        #self.window().makeFirstResponder_(self)


    def textDidEndEditing_(self, aNotification):
        """Notification. Text editing ended."""

        print "KWOutlineView.textDidEndEditing_()"

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

        print "TextMovement: %i" % textMovement,

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

        elif textMovement == NSTabTextMovement:
            print "NSTabTextMovement"
        elif textMovement == NSBacktabTextMovement:
            print "NSBacktabTextMovement"
        elif textMovement == NSLeftTextMovement:
            print "NSLeftTextMovement"
        elif textMovement == NSRightTextMovement:
            print "NSRightTextMovement"
        elif textMovement == NSUpTextMovement:
            print "NSUpTextMovement"
        elif textMovement == NSDownTextMovement:
            print "NSDownTextMovement"
        elif textMovement == NSOtherTextMovement:
            print "NSOtherTextMovement"
        elif textMovement == NSIllegalTextMovement:
            print "NSIllegalTextMovement"
        else:
            print "UNHANDLED MOVEMENT"

        # finish current cell
        super( KWOutlineView, self).textDidEndEditing_(aNotification)

        if returnContinue:
            self.window().makeFirstResponder_(self)
            selRow = self.getSelectedRowIndex()
            item = self.itemAtRow_(selRow)

            if item:
                last = item.isLast()
                if last:
                    # we are at the end of the outline
                    createNode(self, item, startEditing=True)
                else:
                    row = self.rowForItem_( item.next() )
                    self.reloadData()
                    self.editColumn_row_withEvent_select_(0, row, None, True)
                return
        if cancelled:
            self.editSession = False
            self.reloadData()
            self.window().makeFirstResponder_(self)

    def cancelOperation_(self, sender):
        print "KWOutlineView.cancelOperation_()"
        if self.currentEditor():
            # self.abortEditing()
            self.validateEditing()
        # We lose focus so re-establish
        self.window().makeFirstResponder_(self)

    def setWindowStatus_(self, status):
        ctrl = self.delegate().controller
        ctrl.txtWindowStatus.setStringValue_( unicode(status) )


    #
    # event capture
    #
    def keyDown_(self, theEvent):
        """Catch events for the outline and tableviews. """

        eventCharacters = theEvent.characters()
        eventCharacter = ""
        if eventCharacters:
            eventCharacter = eventCharacters[0]
        eventModifiers = int(theEvent.modifierFlags())
        eventCharNum = ord(eventCharacters)

        mykeys = (ord(NSBackspaceCharacter),
                  ord(NSDeleteCharacter),

                  ord(NSCarriageReturnCharacter),
                  ord(NSEnterCharacter),

                  ord(NSTabCharacter),
                  ord(NSBackTabCharacter),

                  ord(NSUpArrowFunctionKey),
                  ord(NSDownArrowFunctionKey),
                  ord(NSLeftArrowFunctionKey),
                  ord(NSRightArrowFunctionKey) )

        if 0: #eventCharNum in mykeys:
            # pass
            print "mykeys"
            pp(mykeys)
            print "Event characters:", repr(eventCharacters), eventCharNum


        # tab has       0x09/0x00100
        # shift tab has 0x19/0x20102
        # alt   tab has 0x09/0x80120

        # shftalttab    0x19/0xa0122 10.4
        # shftalttab    0x19/0x20102 10.4
        
        # ctrl up 0xf700 0xa40101

        # ctrl opt enter 0x3 0x2c0121
        # enter 0x3 0x200100

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
            # NSCarriageReturnCharacter + SHIFT | ALT | CTRL
            # make a key consisting of char+modifiers
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

        editor = self.currentEditor()
        if editor:
            print "EDITOR:", editor
        
        if 0:
            print "eventCharNum", eventCharNum

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

        if kwlog and 0: #kwdbg:
            print "Key: ", hex(eventCharNum), hex(eventModifiers)

        ###########################################################################
        #
        # Deleting
        if eventCharacter in (NSBackspaceCharacter, NSDeleteCharacter):
            if kwlog and kwdbg:
                print "DELETE KEY HANDLED"

            # while editing, will be handled elsewhere
            # outline: delete selection (saving to a pasteboard stack) TBD
            # table: delete selection (saving to a pasteboard stack) Tables will be
            #        deleted in the future
            deleteNodes(self, selection=True)

            # deselect all or find a good way to select the next item
            delg.markDirty()
            self.deselectAll_( None )

        ###########################################################################
        #
        # Create new node
        elif eventCharacter == NSCarriageReturnCharacter:
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
        elif eventCharacter == NSEnterCharacter:
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

                                if not url.startswith( 'http' ):
                                    # get base url via controller
                                    root = item.rootNode
                                    ctrl = root.controller
                                    urlbase = False
                                    if ctrl != None:
                                        urlbase = ctrl.nsurl()
                                        if urlbase:
                                            target = NSURL2str(urlbase.absoluteString())
                                            url = mergeURLs( target, url )
                                open_node( url, nodetype )

                            elif name in ('script'):
                                d = item.getValueDict()
                                href = d.get('src', '')
                                url = cleanupURL( href )

                                # code duplication
                                if not url.startswith( 'http' ):
                                    # get base url via controller
                                    root = item.rootNode
                                    ctrl = root.controller
                                    urlbase = False
                                    if ctrl != None:
                                        urlbase = ctrl.nsurl()
                                        if urlbase:
                                            target = NSURL2str(urlbase.absoluteString())
                                            url = mergeURLs( target, url )
                                open_node(url)

                            elif name in ('a', 'img'):
                                d = item.getValueDict()
                                href = d.get('href', '')
                                if name == 'img':
                                    href = d.get('src', '')
                                url = cleanupURL( href )

                                # code duplication
                                if not url.startswith( 'http' ):
                                    # get base url via controller
                                    root = item.rootNode
                                    ctrl = root.controller
                                    urlbase = False
                                    if ctrl != None:
                                        urlbase = ctrl.nsurl()
                                        if urlbase:
                                            target = NSURL2str(urlbase.absoluteString())
                                            url = mergeURLs( target, url )

                                basename, extension = getURLExtension(url)
                                if extension:
                                    extension = extension.replace('.', '')
                                if extension in g_qtplayer_extensions:
                                    open_node(url, 'QTPL')
                                elif  extension in g_preview_extensions:
                                    open_node(url)
                                else:
                                    open_node(url, 'HTML')
                            
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
                                    open_node( url,
                                               "hook",
                                               open_=True,
                                               supressCache=True)

                                elif theType == "photo":
                                    url = v.get("xmlUrl", "")
                                    open_photo( url )

                                elif theType == "rssentry":
                                
                                    # find pref for opening enclosures
                                    defaults = NSUserDefaults.standardUserDefaults()
                                    openAttach = False
                                    try:
                                        openAttach = bool(defaults.objectForKey_( u'optRSSOpenEnclosure'))
                                    except Exception ,err:
                                        print "Error reading defaults:", err

                                    # extract enclosure URL
                                    enc = v.get("enclosure", "")
                                    url1 = ""
                                    if enc:
                                        url1, rest = enc.split('<<<')

                                    # extract webpage url
                                    url2 = v.get("link", "")
                                    url2 = cleanupURL( url2 )

                                    # open the stuff
                                    if url1 and openAttach:
                                        open_node( url1 )
                                    if url2:
                                        open_node( url2, nodeType="HTML" )

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
                                if item.typ not in CactusOutlineTypes.hierarchicalTypes:
                                    continue

                                # build a new document from current attributes
                                root = OutlineNode(u"__root__", u"", None,
                                                   CactusOutlineTypes.typeOutline, None)
                                for t in item.value:
                                    if isinstance(t, tuple):
                                        name, value = t
                                    elif isinstance(t, str):
                                        name = u"value"
                                        value = t
                                    node = OutlineNode(name, value, root, CactusOutlineTypes.typeTable, root)
                                    root.addChild_(node)

                                #
                                # TBD: eliminate tables, move to outlines, reactivate next line
                                #
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
                        consumed = True
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
        elif eventCharacter == NSBackTabCharacter:
            # shift tab has it's own character
            if eventModifiers & NSShiftKeyMask:
                consumed = self.outdentSelection()

        ###########################################################################
        #
        # Indenting
        elif eventCharacter == NSTabCharacter:
            # indent selection
            consumed = self.indentSelection()

        ###########################################################################
        #
        # Move selection up
        elif eventCharacter == NSUpArrowFunctionKey:
            if eventModifiers & NSControlKeyMask:
                consumed = self.moveSelectionUp()

        ###########################################################################
        #
        # Move selection down
        elif eventCharacter == NSDownArrowFunctionKey:
            if eventModifiers & NSControlKeyMask:
                consumed = self.moveSelectionDown()

        ###########################################################################
        # ctrl-left
        # select parent node
        #
        # ctrl-alt-left
        # select parent node and colapse all
        #
        elif eventCharacter == NSLeftArrowFunctionKey:
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
        elif eventCharacter == NSRightArrowFunctionKey:
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
    # key event handlers
    #
    def moveSelectionDown(self):
        delegate = self.delegate()
        # get selected rows
        items = self.getSelectionItems()
        if not items:
            return False
        #
        moveSelectionDown(self, items)
        delegate.markDirty()
        self.reloadData()

        selection = [self.rowForItem_(i) for i in items]
        if selection:
            self.selectItemRows_( selection )

        self.setNeedsDisplay_( True )
        return True

    def moveSelectionUp(self):
        delegate = self.delegate()
        # get selected rows
        items = self.getSelectionItems()
        if not items:
            return False
        moveSelectionUp(self, items)
        #
        delegate.markDirty()
        self.reloadData()

        selection = [self.rowForItem_(i) for i in items]
        if selection:
            self.selectItemRows_( selection )

        self.setNeedsDisplay_( True )
        return True
        


    def indentSelection(self):

        delegate = self.delegate()

        # get selected rows
        consumed = False
        if delegate.typ in CactusOutlineTypes.hierarchicalTypes:
            sel = self.getSelectionItems()
            # indent each row one level
            postselect = set()
            for item in sel:
                if not item:
                    continue
                parent = item.parent
                previous = item.previous()

                # ignore command if item is first Child
                if previous != -1:
                    item.retain()
                    previous.addChild_( item )
                    parent.removeChild_(item)
                    item.release()
                    postselect.add(item)
                    self.reloadItem_reloadChildren_( previous, True )
                    self.expandItem_( previous )
                    self.reloadItem_reloadChildren_( parent, True )

            # restore selection
            postselect = [self.rowForItem_(i) for i in postselect]
            if postselect:
                self.selectItemRows_( postselect )
                delegate.markDirty()
                consumed = True
            self.reloadData()
            return consumed

    def outdentSelection(self):
        if kwlog:
            print "SHIFT Tab"

        delegate = self.delegate()

        consumed = False
        if delegate.typ in CactusOutlineTypes.hierarchicalTypes:
            # get selected rows
            sel = self.getSelectionItems()
            if not sel:
                return

            # working from the end
            sel.reverse()

            # dedent each row one level
            for item in sel:
                item.moveLeft()

            self.reloadData()

            # restore selection
            postselect = [self.rowForItem_(i) for i in sel]
            if postselect:
                self.selectItemRows_( postselect )

            consumed = True
            delegate.markDirty()
            # self.reloadData()
        return consumed
    #
    # utilities
    #
    def getSelectionItems(self):
        if kwlog:
            print "getSelectionItems"
        """The actual nodes of the current selection are returned."""
        sel = self.selectedRowIndexes()
        result = []
        n = 0
        if sel:
            n = sel.count()
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
        return self.selectedRow()

    def selectItemRows_( self, itemIndices ):
        s = NSMutableIndexSet.indexSet()
        for i in itemIndices:
            if i >= 0:
                s.addIndex_( i )
        self.selectRowIndexes_byExtendingSelection_(s, False)

    def selectItems_(self, items):
        self.deselectAll_( None )
        indexes = NSMutableIndexSet.alloc().init()
        for item in items:
            idx = self.rowForItem_( item )
            if idx != -1:
                indexes.addIndex_( idx )
        self.selectRowIndexes_byExtendingSelection_(indexes, False)


    def selectRowItem_(self, item):
        index = self.rowForItem_( item )
        s = NSIndexSet.indexSetWithIndex_( index )
        self.selectRowIndexes_byExtendingSelection_(s, False)

    @objc.IBAction
    def expandSelection_(self, sender):
        items = self.getSelectionItems()
        for item in items:
            self.expandItem_(item)

    @objc.IBAction
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
    #   document
    #   outlineView
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
        self.outlineView = None

        # not yet used; it's an idea for rss documents to constrain node movements.
        self.restricted = False
        return self

    def dealloc(self):
        print "OutlineViewDelegateDatasource.dealloc()"
        #if self.parentNode:
        #    self.parentNode.release()
        if self.root:
            # this is evil and does not work
            n = self.root.retainCount()
            for i in range(n):
                self.root.release()
            self.root=None
        if self.controller:
            print "TODO OutlineViewDelegateDatasource.controller.release()", self.controller.retainCount()

        #    self.controller.release()
        if self.document:
            print "TODO OutlineViewDelegateDatasource.document.release()", self.document.retainCount()
        #    self.document.release()
        super(OutlineViewDelegateDatasource, self).dealloc()

    def initWithObject_type_parentNode_(self, obj, typ, parentNode):
        self = self.init()

        if not self:
            return None

        self.typ = typ
        self.parentNode = parentNode

        if not isinstance(obj, OutlineNode):
            obj = OutlineNode(unicode(obj), "", None, CactusOutlineTypes.typeOutline, None)
        self.root = obj

        return self

    def setOutlineView_(self, ov):
        if self.outlineView:
            self.outlineView.release()
        self.outlineView = ov

    def markDirty(self):
        doc = self.controller.document()
        if doc:
            doc.updateChangeCount_( NSChangeDone )


    def setController_(self, controller):
        self.controller = controller

    def reloadData_(self, item):
        if self.controller:
            self.controller.reloadData_(item)
        else:
            if kwlog:
                print "FAILED: reloadData_(%s)" % repr(item)

    def isSubEditor(self):
        return self.parentNode != None

    def appendToRoot_Value_(self, name, value):
        node = OutlineNode(name, value, self.root, self.typ, self.root)
        self.root.addChild_( node )
        # need to reload all so the new node gets recognized
        self.reloadData_( node )
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
            return item.type
        elif c == u"value":
            return item.displayValue
        elif c == u"name":
            return item.name
        elif c == u"comment":
            return item.comment


    def numberOfRowsInTableView_(self, tv):
        print "numberOfRowsInTableView_"
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
        if not self.typ in CactusOutlineTypes.hierarchicalTypes:
            return False
        return item.noOfChildren() > 0

    def outlineView_objectValueForTableColumn_byItem_(self, view, col, item):
        c = col.identifier()
        if not item:
            item = self.root
        if c == u"type":
            return item.type
        elif c == u"value":
            return item.displayValue
        elif c == u"name":
            return item.name
        elif c == u"comment":
            return item.comment


    def outlineView_setObjectValue_forTableColumn_byItem_(self, view, value, col, item):
        columnName = col.identifier()

        if not item:
            return

        if columnName == u"type":
            pass

        elif columnName == u"value":
            if value != item.displayValue:
                # if it has a parentNode it's edited attributes
                if self.parentNode != None:
                    name = item.name
                    self.parentNode.updateValue_( (name, unicode(value)) )
                item.setValue_( value )
                self.markDirty()

        elif columnName == u"name":
            if value != item.name:
                item.setName_(value)
                self.markDirty()

        elif columnName == u"comment":
            if value != item.comment:
                item.setComment_(value)
                self.markDirty()


    #
    # drag and drop
    #
    def outlineView_acceptDrop_item_childIndex_(self, ov, info, targetItem, index):
        print "DELG.outlineView_acceptDrop_item_childIndex_"
        parent = targetItem.parent
        targetIndex = targetItem.siblingIndex()
        pb = info.draggingPasteboard()

        print "targetItem:", targetItem
        print "index", index
        print "info", info

        if targetItem:
            # drop on item
            if index >= 0:
                pass
            else:
                pass
        else:
            # drop in view
            # append to last
            if index >= 0:
                pass
            else:
                pass
        insertedItems = ov.readNodesFromPasteboard_parent_index_(pb, targetItem, index)

        # delete origin - feels hackish accessing a class variable
        # originals must be deleted after insertion
        # 
        deleteNodes(ov, nodes=KWOutlineView.lastDrag)
        KWOutlineView.lastDrag = []
        ov.selectItems_( insertedItems )

        if 0:
            for item in insertedItems:
                index = ov.rowForItem_( item )
                print "selectionIndex:", index, item
                if index != -1:
                    s = NSIndexSet.indexSetWithIndex_( index )
                    ov.selectRowIndexes_byExtendingSelection_(s, True)

        ov.reloadData()
        ov.setNeedsDisplay_( True )
        ov.reloadItem_reloadChildren_(None, True)


        return True


    def outlineView_validateDrop_proposedItem_proposedChildIndex_(self, ov, dragInfo, item, index):
        if kwdbg:
            print "DELG.outlineView_validateDrop_proposedItem_proposedChildIndex_"
        if dragInfo.draggingSource() == self.outlineView:
            # print "drag in outlineView()!"
            # print item
            # pp(dragInfo)
            #if index == NSOutlineViewDropOnItemIndex:
            #    return NSDragOperationMove
            #else:
            #    return NSDragOperationNone

            #if not item:
            #    pass
            # self.setDropItem_dropChildIndex_(item, NSOutlineViewDropOnItemIndex)
            return NSDragOperationMove
        else:
            # external drop - not now
            print "souce:", dragInfo.draggingSource()
            return NSDragOperationLink

        return NSDragOperationNone


    def outlineView_writeItems_toPasteboard_(self, ov, items, pb):
        if kwdbg:
            print "DELG.outlineView_writeItems_toPasteboard_"
        #pdb.set_trace()
        pb.declareTypes_owner_( [DragDropCactusPboardType],
                                self)
        # items = ov.getSelectionItems()

        # pack items
        result = []
        names = []
        for item in items:
            result.append( item.copyPython())
            names.append( item.name )

        data = cPickle.dumps( result )
        l = len(data)
        nsdata = NSData.dataWithBytes_length_(data, l)
        pb.setData_forType_(
            nsdata,
            DragDropCactusPboardType)
        KWOutlineView.lastDrag = list(items)
        #pb.setString_forType_(
        #    u"\n".join(names),
        #    NSStringPboardType)
        
        return True


    # delegate method

    def outlineView_heightOfRowByItem_(self, ov, item):
        lineheight = 14
        maxLines = self.controller.rowLines

        if not self.controller.variableRowHeight:
            return lineheight

        lines = min( maxLines, int(item.maxHeight))
        lines = max(1, lines)
        return lines * lineheight

    def outlineView_shouldEditTableColumn_item_(self, ov, col, item):
        columnName = col.identifier()
        if columnName == u"type":
            return False
        return True

    # UNUSED
    def ovUpdateItem_Key_Value_(self, item, key, value):
        # update a single key value pair in the value dict
        pass

    def outlineViewSelectionDidChange_( self, aNotification ):
        if kwdbg:
            print "outlineViewSelectionDidChange_()"
        ov = None
        if aNotification:
            #print aNotification
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
                name = item.name
                if len(name) > 33:
                    name = name[:30] + "..."
                s = "Lev: %i  height: %i %s" % (level, item.maxHeight, name)
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


#
# node editing
#
# TODO: deleting does not update correctly.
# line stays visible in parent view. needsRedraw_?
#
def deleteNodes(ov, nodes=(), selection=False):
    if kwdbg:
        print "CactusOutline.deleteNodes()"
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
    if kwdbg:
        print "CactusOutline.createNode()"
    # create node at selection and start editing

    # open new line and start editing
    # if already editing, start new line, continue editing
    delg = ov.delegate()
    typ = delg.typ
    root = delg.root

    # no selection - make new node at end
    if selection == -1:
        node = OutlineNode( u"", u"", root, typ, root)
        root.addChild_( node )
        # need to reload all so the new node gets recognized
        ov.reloadData()
        rowIndex = ov.rowForItem_( node )

    else:
        p = selection.parent
        # root = p.rootNode
        node = OutlineNode(u"", "", p, typ, root)
        targetIdx = selection.nextIndex()
        if targetIdx == -1:
            p.addChild_( node )
        else:
            p.addChild_atIndex_( node, targetIdx )
        ov.reloadData()
        ov.selectRowItem_( node )
        rowIndex = ov.rowForItem_( node )

    if startEditing:
        s = NSIndexSet.indexSetWithIndex_( rowIndex )
        ov.selectRowIndexes_byExtendingSelection_(s, False)
        ov.reloadData()
        ov.editColumn_row_withEvent_select_(0, rowIndex, None, True)
    delg.markDirty()


def moveSelectionUp(ov, items):
    if kwdbg:
        print "CactusOutline.moveSelectionUp()"
    delg = ov.delegate()
    for item in items:
        # move item before previous
        #  get grandparent
        #  insert at index of previous

        if not item:
            continue
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
    if kwdbg:
        print "CactusOutline.moveSelectionDown()"
    #
    # this really needs to be sorted down; use indices
    # otherwise there will be overlapping moves destroying
    # sortorder
    delg = ov.delegate()
    items.reverse()
    for item in items:
        # retain item 0
        if not item:
            continue
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
    if kwdbg:
        print "EMPTY: CactusOutline.moveSelectionLeft()"
    pass

def moveSelectionRight(ov, selection):
    if kwdbg:
        print "EMPTY: CactusOutline.moveSelectionRight()"
    pass


def unmangleFSSPecURL( url ):
    orgurl = url
    # clean up fsspec mangled names in URLs

    if '#' in url:
        # escape OS9 mangled filenames; Frontier produces such links
        os9namepart = re.compile( r"^(.+)#([0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F][0-9A-F]\....)$" )
        m = os9namepart.match( url )
        if m:
            pre, post = m.groups()
            pre = urllib.quote( pre, "/:?" )
            post = urllib.quote( post, "/:?" )
            url = "%s%%23%s" % (pre, post)
    if kwdbg:
        print "CactusOutline.unmangleFSSpecURL(%s) -> %s" % (orgurl, url)
    return url


def cleanupURL( url ):
    if kwdbg:
        print "CactusOutline.cleanupURL()"
    # lots of URLs contain spaces, &, '
    return unmangleFSSPecURL( url )

    mangled = False
    url = NSURL2str(url)
    if '#' in url:
        # escape OS9 mangled filenames; Frontier produces such links
        os9namepart = re.compile( r"(.*)#([0-9A-F]{7,7}\.{3,3}]*)" )
        m = os9namepart.match( url )
        if m:
            mangled = True
            l = m.groups()
            url = "%s%%23%s" % l
            # url = re.sub(os9namepart, "\1%23\2.\3", url)
        if mangled:
            return url

    if not mangled:
        # what did i smoke when i wrote that?
        #
        # this mess needs serious cleaning
        #

        # purl = urlparse.urlparse( url )
        purl = urlparse.urlsplit( url, allow_fragments=False )
        path = purl.path
        purl = list( purl )

        path = urllib.unquote( 'http://' + path )
        try:
            path = urllib.quote( path )
        except KeyError, err:
            print "ERROR"
            print repr(path)
            print err
        path = path[9:]
        purl[2] = path
        #
        purl.append("")
        purl = urlparse.urlunparse( purl )
        purl = unicode(purl)
        return purl
