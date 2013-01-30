
# -*- coding: utf-8 -*-


"""
"""

import sys
import os
import traceback

import time
import datetime
import urllib
import binascii
import struct

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import cStringIO

import pdb
import pprint
pp = pprint.pprint
kwdbg = False
kwlog = True

import feedparser

import opml

import CactusVersion

import CactusTools
readURL = CactusTools.readURL
errorDialog = CactusTools.errorDialog
NSURL2str = CactusTools.NSURL2str
makeunicode = CactusTools.makeunicode

import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException
XMLParseErrorException = CactusExceptions.XMLParseErrorException
HTMLParseErrorException = CactusExceptions.HTMLParseErrorException
PLISTParseErrorException = CactusExceptions.PLISTParseErrorException

import objc

import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL
NSMakeRect = Foundation.NSMakeRect

# NSDate, NSNumber, NSArray, or NSDictionary
NSData = Foundation.NSData
NSDate = Foundation.NSDate

NSNumber = Foundation.NSNumber
NSArray = Foundation.NSArray
NSDictionary = Foundation.NSDictionary
NSUserDefaults = Foundation.NSUserDefaults
NSMutableData = Foundation.NSMutableData
NSKeyedArchiver = Foundation.NSKeyedArchiver

import AppKit
NSDocument = AppKit.NSDocument
NSDocumentController = AppKit.NSDocumentController
NSWorkspace = AppKit.NSWorkspace
NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString

# grid styles
NSTableViewGridNone = AppKit.NSTableViewGridNone
NSTableViewSolidVerticalGridLineMask = AppKit.NSTableViewSolidVerticalGridLineMask
NSTableViewSolidHorizontalGridLineMask = AppKit.NSTableViewSolidHorizontalGridLineMask

# undo manager constants
NSChangeDone = AppKit.NSChangeDone
NSChangeUndone = AppKit.NSChangeUndone
NSChangeCleared = AppKit.NSChangeCleared
NSChangeReadOtherContents = AppKit.NSChangeReadOtherContents
NSChangeAutosaved = AppKit.NSChangeAutosaved


import PyObjCTools
import PyObjCTools.NibClassBuilder
extractClasses = PyObjCTools.NibClassBuilder.extractClasses
AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass


import outlinetypes
typeOutline = outlinetypes.typeOutline
typeTable = outlinetypes.typeTable
typeBrowser = outlinetypes.typeBrowser


import Outline
OutlineViewDelegateDatasource = Outline.OutlineViewDelegateDatasource
OutlineNode = Outline.OutlineNode

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType
CactusPLISTType = CactusDocumentTypes.CactusPLISTType
CactusIMLType = CactusDocumentTypes.CactusIMLType

extractClasses("OutlineEditor")


def boilerplateOPML( rootNode ):
    """Creates the minimal outline nodes for the OPML structure.

    rootNode - the node under which the structure will be created

    """

    ZERO = datetime.timedelta(0)
    HOUR = datetime.timedelta(hours=1)
    class UTC(datetime.tzinfo):
        """UTC - from python library examples."""
    
        def utcoffset(self, dt):
            return ZERO
    
        def tzname(self, dt):
            return "UTC"
    
        def dst(self, dt):
            return ZERO
        
    now = datetime.datetime.now( UTC() )
    s = now.strftime("%a, %d %b %Y %H:%M:%S %Z")

    root = rootNode.findRoot()
    head = OutlineNode("head", "", rootNode, typeOutline, root)
    rootNode.addChild_( head )

    defaults = NSUserDefaults.standardUserDefaults()
    uname = uemail = ""
    try:
        uname = unicode(defaults.objectForKey_( u'txtUserName'))
        uemail = unicode(defaults.objectForKey_( u'txtUserEmail'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)

    head.addChild_(OutlineNode("dateCreated", s, head, typeOutline, root))
    head.addChild_(OutlineNode("dateModified", s, head, typeOutline, root))
    head.addChild_(OutlineNode("ownerName", uname, head, typeOutline, root))
    head.addChild_(OutlineNode("ownerEmail", uemail, head, typeOutline, root))
    head.addChild_(OutlineNode("expansionState", "", head, typeOutline, root))
    head.addChild_(OutlineNode("vertScrollState", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowTop", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowLeft", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowBottom", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowRight", "", head, typeOutline, root))

    body = OutlineNode("body", "", rootNode, typeOutline, root)
    rootNode.addChild_( body )

    body.addChild_( OutlineNode("", "", body, typeOutline, root) )
    #head.release()
    #body.release()
    print "root:", root.retainCount()
    print "head:", head.retainCount()
    print "body:", body.retainCount()
    return


# a cocoa NSDocument subclass
class CactusOutlineDocument(AutoBaseClass):
    #
    # outlets:
    #  parentNode
    #  rootNode
    #  url
    # parentclass(NSDocument) outlets:
    #   window
    #
    """
    """

    def init(self):
        if kwlog:
            print "CactusOutlineDocument.init()"
        self = super( CactusOutlineDocument, self).init()

        # outline specific
        # parentNode is used to determine if only an aspect of the outline is edited
        self.parentNode = None

        # outline root node; invisible and not editable
        self.rootNode = None

        #
        self.url = None

        #
        self.title = "Untitled Outline"

        self.outlineView = None

        # TBD
        self.setHasUndoManager_( False )
        return self

    def dealloc(self):
        print "CactusOutlineDocument.dealloc()"
        super(CactusOutlineDocument, self).dealloc()


    def autosavingFileType(self):
        """2012-12-12 KW created to disable autosaving."""
        return None

    def readFromURL_ofType_error_(self, url, theType):
        if kwlog:
            print ("CactusOutlineDocument.readFromURL_ofType_error_( %s, %s )\n"
                   % (repr(url), repr(theType),))

        OK = True
        s = None
        err = None
        self.url = url

        # read opml content
        if theType == CactusOPMLType:
            # pdb.set_trace()
            d = None
            try:
                d = opml.opml_from_string( readURL( url, CactusOPMLType ) )
            except OPMLParseErrorException, v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            if d:
                root, theType = openOPML_( d, urltag=NSURL2str(url) )
                del d
                if not root:
                    if kwlog:
                        print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                    return (False, "Error creating the outline.")
                else:
                    self.rootNode = root
                    if not url.isFileURL():
                        self.updateChangeCount_( NSChangeReadOtherContents )
                    else:
                        self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                return (False, None)

        # read rss content
        elif theType == CactusRSSType:
            root, theType = openRSS_( url )
            if root:
                self.rootNode = root
                if not url.isFileURL():
                    self.updateChangeCount_( NSChangeReadOtherContents )
                else:
                    self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                return (False, None)

        # read xml content
        elif theType == CactusXMLType:
            d = None
            try:
                d = opml.xml_from_string( readURL( url, CactusXMLType ) )
            except XMLParseErrorException, v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            root, theType = openXML_( d )
            del d

            if root:
                self.rootNode = root
                if not url.isFileURL():
                    # mark internet document dirty
                    self.updateChangeCount_( NSChangeReadOtherContents )
                else:
                    # mark local document clean
                    self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                return (False, None)

        # read html content
        elif theType == CactusHTMLType:
            d = None
            try:
                d = opml.html_from_url( url )
            except HTMLParseErrorException, v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            # don't read type here, HTML is terminal type
            root, dummy = openXML_( d )
            del d

            if root:
                self.rootNode = root
                if not url.isFileURL():
                    self.updateChangeCount_( NSChangeReadOtherContents )
                else:
                    self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                return (False, None)
        
        # read plist content
        elif theType == CactusPLISTType:
            d = None
            try:
                d = opml.parse_plist( url )
            except PLISTParseErrorException, v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            # may return ttheType=CactusPLISTType
            root, theType = openPLIST_( d )
            del d

            if root:
                self.rootNode = root
                if not url.isFileURL():
                    self.updateChangeCount_( NSChangeReadOtherContents )
                else:
                    self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                return (False, None)

        # read itunes music xml
        elif theType == CactusIMLType:
            d = None
            # pdb.set_trace()
            try:
                d = opml.parse_plist( url )
            except PLISTParseErrorException, v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            # don't read type here, HTML is terminal type
            root, dummy = openIML_( d )
            del d

            if root:
                self.rootNode = root
                if not url.isFileURL():
                    self.updateChangeCount_( NSChangeReadOtherContents )
                else:
                    self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                return (False, None)
        else:
            OK = False

        if OK:
            self.setFileURL_( url )
            self.setFileType_( theType )

        print "OK CactusOutlineDocument.readFromURL_ofType_error_()"
        return (OK, None)
    
    
    def initWithContentsOfURL_ofType_error_(self, url, theType):
        """Main entry point for opening documents."""

        self, err = self.initWithType_error_( theType )

        if not self:
            return( None, None)

        if kwlog:
            print "\nCactusOutlineDocument.initWithContentsOfURL_ofType_error_( %s )" % (
                                                                        repr(theType),)
            print repr(url); print
        
        OK, err = self.readFromURL_ofType_error_( url, theType )

        if OK:
            if not url.isFileURL():
                #
                # evil hack, because NSDocumentController doesn't open window if
                # document is loaded with http: scheme
                #
                docc = NSDocumentController.sharedDocumentController()
                added = docc.addDocument_(self)
                
                # this is source of trouble ( double or none call to makeWindowControllers)
                # 
                self.makeWindowControllers()
                self.showWindows()

            # check opml file metadata
            if theType == CactusOPMLType:
                pass
            return (self, err)

        # could not create document
        return (None, err)


    def initWithType_error_(self, theType):
        # pdb.set_trace()
        if kwlog:
            print "CactusOutlineDocument.initWithType_error_( %s )" % (repr(theType),)

        self = self.init()
        if not self:
            return (None, None)

        self.setFileType_( theType )

        self.rootNode = OutlineNode("__ROOT__", "", None, typeOutline, None)
        if kwlog:
            print "    .initWithType_error_ rootRetaines %i " % (self.rootNode.retainCount(),)
        boilerplateOPML( self.rootNode )
        if kwlog:
            print "    .initWithType_error_ boilerplate rootRetaines %i " % (self.rootNode.retainCount(),)
        self.updateChangeCount_( NSChangeCleared )

        self.variableRowHeight = True
        return (self, None)


    def displayName(self):
        
        if kwlog:
            print "CactusOutlineDocument.displayName() ->",

        title = self.title
        fullpath = self.fileURL()
        if fullpath:
            fullpath = fullpath.path()

        if not fullpath:
            fullpath = self.url
        else:
            self.url = fullpath

        fullpath = NSURL2str(fullpath)

        try:
            t = os.path.split( fullpath )[1]
            if t:
                title = t
        except Exception, err:
            print
            print "displayName CRASHED!"
            print err
            print
        finally:
            pass

        if kwlog:
            print repr(title)
        self.title = title
        return self.title


    def awakeFromNib(self):
        if kwlog:
            print "CactusOutlineDocument.awakeFromNib()"


    def XXwindowNibName(self):
        # deactivated
        if kwlog:
            print "CactusOutlineDocument.windowNibName()"
        return u"OutlineEditor"


    def fileURL( self ):
        # do nothing the superclass wouldn't do
        if kwlog:
            print "SUPER CactusOutlineDocument.fileURL()"
        return super( CactusOutlineDocument, self).fileURL()


    def setFileURL_( self, theURL ):
        # print "URLType:", type(theURL)
        if not isinstance( theURL, NSURL ):
            theURL = NSURL.URLWithString_( theURL )
        # do nothing the superclass wouldn't do
        if kwlog:
            print "SUPER CactusOutlineDocument.setFileURL()"
        super( CactusOutlineDocument, self).setFileURL_( theURL )


    def windowControllerWillLoadNib_( self, aController):
        # do nothing the superclass wouldn't do
        if kwlog:
            print "SUPER CactusOutlineDocument.windowControllerWillLoadNib_( %s )" % repr(aController)
        super( CactusOutlineDocument, self).windowControllerWillLoadNib_(aController)


    def windowControllerDidLoadNib_( self, aController):
        # do nothing the superclass wouldn't do
        if kwlog:
            print "SUPER CactusOutlineDocument.windowControllerDidLoadNib_()"
        super( CactusOutlineDocument, self).windowControllerDidLoadNib_(aController)


    def calculateExpansionState_( self, rootNode ):
        # for expansionstate
        # pdb.set_trace()
        # controllers = self.windowControllers()
        n = self.windowControllers().count()
        
        for i in range(n):
            controller = self.windowControllers().objectAtIndex_(i)
            print controller, controller.retainCount()
            winframe = {}
            rootNode = controller.rootNode
            ov = controller.outlineView
            win = ov.window()
            frame = win.frame()
            if frame:
                winframe = {
                    'windowLeft': int(frame.origin.x),
                    'windowTop': int(frame.origin.y),
                    'windowRight': int(frame.origin.x + frame.size.width),
                    'windowBottom': int(frame.origin.y + frame.size.height)
                }                    

            # parse root down to head
            children = rootNode.children
            head = body = False
            for child in children:
                if child.name == u"head":
                    head = child
                if child.name == u"body":
                    body = child
            #if head:
            #    ov.collapseItem_collapseChildren_( head, True )

            # start at first child of body
            if body:
                if len(body.children) > 0:
                    expanded = []
                    item = body.children[0]
                    # expandable item 1
                    idx = 1
                    # is at row
                    row = ov.rowForItem_( item )

                    if ov.isItemExpanded_( item ):
                        expanded.append( idx )
                    
                    while True:
                        idx += 1
                        row += 1
                        item = ov.itemAtRow_( row )
                        if not item:
                            break
                        if ov.isItemExpanded_( item ):
                            expanded.append( idx )
                        if idx % 1000 == 0:
                            print "idx, items", idx, len(expanded)

                    expanded = [str(i) for i in expanded]
                    expanded = ', '.join( expanded )
                    if expanded == "":
                        expanded = "1"
                    if kwlog:
                        print "CactusOutlineDocument.calculateExpansionState_()"
                        print "'%s'" % expanded
                        print 
                    winframe['expansionState'] = expanded
                    return winframe

            # scavenge document metadata
            searchKeys = ( 'dateCreated dateModified ownerName ownerEmail '
                           'expansionState windowTop windowLeft windowBottom '
                           'windowRight'.split() )
            meta = {}

            if len(children) == 1:
                ov.expandItem_expandChildren_(children[0], False)

            if head and body: # ;-)
                children = head.children

                for child in children:
                    k = child.name
                    v = child.displayValue
                    if k in searchKeys:
                        if v:
                            meta[k] = v

                # start - collapse head - expand body
                ov.collapseItem_collapseChildren_(head, True)
                ov.collapseItem_collapseChildren_(body, True)
                ov.expandItem_expandChildren_(body, False)

                # first row is 2
                rows = False
                if "expansionState" in meta:
                    rows = meta[ 'expansionState' ]


    def dataRepresentationOfType_( self, theType ):
        if kwlog:
            print "CactusOutlineDocument.dataRepresentationOfType_( %s )" % repr(theType)

        defaults = NSUserDefaults.standardUserDefaults()

        # future scaffolding
        if theType == CactusOPMLType:

            expansionState = self.calculateExpansionState_( self.rootNode )
            rootOPML = opml.generateOPML( self.rootNode, indent=1, expansion=expansionState )

            e = etree.ElementTree( rootOPML )

            fob = cStringIO.StringIO()
            e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
            t = fob.getvalue()
            fob.close()
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusRSSType:
            t = opml.generateRSS( self.rootNode, indent=1 )
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusXMLType:
            # closed after finding the trailing text bug/misconception
            # return None
            rootXML = opml.generateXML( self.rootNode) #, indent=1 )

            e = etree.ElementTree( rootXML )

            fob = cStringIO.StringIO()
            # e.write(fob, pretty_print=True, encoding="utf-8", xml_declaration=True, method="xml" )
            e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
            t = fob.getvalue()
            fob.close()
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusHTMLType:
            # closed after finding the trailing text bug/misconception
            # return None
            doctype = encoding = ""
            indent = 0
            try:
                doctype = unicode(defaults.objectForKey_( u'menDoctype'))
                encoding = unicode(defaults.objectForKey_( u'menEncoding'))
                indent = unicode(defaults.objectForKey_( u'txtIndent'))
                indent = int(indent)

            except StandardError, err:
                print "ERROR reading defaults.", repr(err)

            etHTML = opml.generateHTML( self.rootNode, doctype, encoding, indent )

            if etHTML:
                # e = etree.ElementTree( rootHTML )
    
                #fob = cStringIO.StringIO()
                ## e.write(fob, pretty_print=True, encoding="utf-8", xml_declaration=True, method="xml" )
                #etHTML.write(fob) # , encoding="utf-8", xml_declaration=False, method="html" )
                #t = fob.getvalue()
                #fob.close()
                #return NSData.dataWithBytes_length_(t, len(t))
                return NSData.dataWithBytes_length_(etHTML, len(etHTML))

        elif theType == CactusDocumentTypes.CactusPLISTType:
            return opml.serializePLISTOutline_( self.rootNode )

        # these are just ideas
        elif theType == CactusDocumentTypes.CactusTEXTType:
            pass
        elif theType == CactusDocumentTypes.CactusSQLITEType:
            pass
        elif theType == CactusDocumentTypes.CactusXOXOType:
            pass
        elif theType == CactusDocumentTypes.CactusEMACSORGType:
            pass
        elif theType == CactusDocumentTypes.CactusTABLEType:
            pass

        else:
            print
            print "ERROR! Bogus filetype for writing: '%s'" % repr(theType)
            print

        # Insert code here to write your document from the given data.
        # You can also choose to override -fileWrapperRepresentationOfType:
        # or -writeToFile:ofType: instead.
        
        # For applications targeted for Tiger or later systems, you should
        # use the new Tiger API -dataOfType:error:.  In this case you can
        # also choose to override -writeToURL:ofType:error:,
        # -fileWrapperOfType:error:,
        # or -writeToURL:ofType:forSaveOperation:originalContentsURL:error:
        # instead.

        if kwlog:
            print "CactusOutlineDocument.dataRepresentationOfType_( %s ) RETURNED NONE" % repr(theType)
        return None


    def loadDataRepresentation_ofType_(data, aType):
        if kwlog:
            print
            print "------ TBD ----- CactusOutlineDocument.loadDataRepresentation_ofType_()"
            print
        # Insert code here to read your document from the given data.  You can
        # also choose to override -loadFileWrapperRepresentation:ofType: or
        # -readFromFile:ofType: instead.
    
        # For applications targeted for Tiger or later systems, you should use
        # the new Tiger API readFromData:ofType:error:.  In this case you can
        # also choose to override -readFromURL:ofType:error: or
        # -readFromFileWrapper:ofType:error: instead.
    
        return True


    def readFromData_ofType_error_(self, data, typeName):
        if kwlog:
            print "X" * 80
            print "CactusOutlineDocument.readFromData_ofType_error_()"
            print "X" * 80

        outError = None
        readSuccess = False

        s = str(data.bytes())
        if typeName == CactusOPMLType:
            d = opml.opml_from_string( s )
            if d:
                root, typeName = openOPML_( d )
                if self.rootNode:
                    pass
                    # release here
                self.rootNode = root
                readSuccess = True

        elif theType == CactusDocumentTypes.CactusRSSType:
            d = feedparser.parse( s, agent=CactusVersion.user_agent )
            if d:
                root, typeName = openRSS_( d )
                if self.rootNode:
                    pass
                    # release here
                self.rootNode = root
                readSuccess = True
        else:
            print "ERROR: Wrong type requested: ", repr(typename)
        return (readSuccess, outError)


    def showWindows( self ):
        if kwlog:
            print "CactusOutlineDocument.showWindows()"
        super( CactusOutlineDocument, self).showWindows()
        #
        # for expansionstate
        controllers = self.windowControllers()
        for controller in controllers:
            print controller, controller.retainCount()
            rootNode = controller.rootNode
            outlineView = controller.outlineView
            # parse root down to head
            children = rootNode.children
            head = body = False
            for child in children:
                if child.name == u"head":
                    head = child
                if child.name == u"body":
                    body = child
            # scavenge document metadata
            #
            # not used for now
            #
            # 'dateCreated dateModified ownerName ownerEmail '
            # 
            searchKeys = ('expansionState windowTop windowLeft '
                          'windowBottom windowRight'.split() )
            meta = {}

            if len(children) == 1:
                outlineView.expandItem_expandChildren_(children[0], False)

            if head and body: # ;-)
                children = head.children

                for child in children:
                    k = child.name
                    v = child.displayValue
                    if k in searchKeys:
                        if v:
                            meta[k] = v

                # start - collapse head - expand body
                outlineView.collapseItem_collapseChildren_(head, True)
                outlineView.collapseItem_collapseChildren_(body, True)
                outlineView.expandItem_expandChildren_(body, False)

                # first row is 2
                rows = meta.get("expansionState", [])
                # pdb.set_trace()
                if rows:
                    try:
                        rows = rows.split(',')
                        rows = [int(i)+1 for i in rows if i]
                    except Exception, err:
                        print "\nERROR: expansionState reading failed.\n", err
                        print
                    if rows:
                        for row in rows:
                            item = outlineView.itemAtRow_( row )
                            outlineView.expandItem_expandChildren_(item, False)
                keys = 'windowLeft windowTop windowRight windowBottom'.split()
                coords = []
                # pdb.set_trace()
                try:
                    for key in keys:
                        coords.append( float( meta[key] ))
                    window = outlineView.window()
                    s = NSMakeRect(coords[0], coords[1], coords[2] - coords[0], coords[3] - coords[1])
                    window.setFrame_display_animate_(s, True, True)
                except StandardError, err:
                    print err
                    print "No window setting for you."
                break

        outlineView.setNeedsDisplay_( True )

    def makeWindowControllers(self):
        c = CactusOutlineWindowController.alloc().initWithObject_( self )
        if kwlog:
            print "CactusOutlineDocument.makeWindowControllers()", c.retainCount()
        self.addWindowController_( CactusOutlineWindowController.alloc().initWithObject_( self ) )


    def printShowingPrintPanel_(self, show):
        printInfo = self.printInfo()
        printOp =NSPrintOperation.printOperationWithView_printInfo_(self, printInfo )
        printOp.setShowPanel_(show)
        self.runModalPrintOperation_delegate_didRunSelector_contextInfo_( printOp, None, None, None, None)


class CactusOutlineWindowController(AutoBaseClass):
    """the actual base class is NSWindowController

    menRowLines
    outlineView
    optAlterLines
    optCommentVisible
    optHLines
    optNameVisible
    optTypeVisible
    optValueVisible
    optVariableRow
    optVLines
    txtOutlineType
    window
    """

    def dealloc(self):
        #if self.rootNode:
        #    self.rootNode.release()
        #if self.parentNode:
        #    self.parentNode.release()
        self.model.release()
        super(CactusOutlineWindowController, self).dealloc()


    def initWithObject_(self, document):
        """This controller is used for outline and table windows.
        
        document is a CactusOutlineDocument
        
        """
        if kwlog:
            print "CactusOutlineWindowController.initWithObject_()"

        self = self.initWithWindowNibName_("OutlineEditor")
        title = u"Unnamed Outline"

        # self.path = ""
        self.rootNode = None
        self.parentNode = None
        self.variableRowHeight = True
        self.rowLines = 2
        self.nsurl = None
        self.url = None

        # check if needed
        self.document = document

        if not isinstance(document, CactusOutlineDocument):
            print "FAKE document"
            # pdb.set_trace()
            print "FAKE document"

        if document.url:
            self.nsurl = document.url
            if document.url.isFileURL():
                self.url = unicode(document.url.path())
            else:
                self.url = NSURL2str(document.url)
        # path is a string or False now

        self.rootNode = document.rootNode
        if self.rootNode:
            # all nodes can access the document
            self.rootNode.controller = self

        self.parentNode = document.parentNode
        title = document.title

        # get window name from url or path
        if self.nsurl:
            if os.path.exists( self.url ):
                fld, fle = os.path.split( self.url )
                title = fle
            else:
                title = self.url
        else:
            # keep unnamed title
            pass

        self.window().setTitle_( title )

        self.model = OutlineViewDelegateDatasource.alloc().initWithObject_type_parentNode_(
                                                self.rootNode,
                                                typeOutline,
                                                self.parentNode )

        # this is evil, and doesn't work
        # self.rootNode.model = self.model

        self.model.document = document

        self.model.setController_( self )

        # this will become very dangerous when a document gets more than 1 window
        self.document.outlineView = self.outlineView

        self.outlineView.setDataSource_(self.model)
        self.outlineView.setDelegate_(self.model)

        self.outlineView.setTarget_(self)
        self.outlineView.setDoubleAction_("doubleClick:")

        self.window().makeFirstResponder_(self.outlineView)
        
        # store them columns
        self.nameColumn = self.outlineView.tableColumnWithIdentifier_( "name" )
        self.typeColumn = self.outlineView.tableColumnWithIdentifier_( "type" )
        self.valueColumn = self.outlineView.tableColumnWithIdentifier_( "value" )
        self.commentColumn = self.outlineView.tableColumnWithIdentifier_( "comment" )

        # set name column to wrap
        self.nameColumn.dataCell().setWraps_( True )
        self.commentColumn.dataCell().setWraps_( True )
        self.valueColumn.dataCell().setWraps_( True )

        defaults = NSUserDefaults.standardUserDefaults()
        self.rowLines = 2
        self.optValueVisible.setState_( True )
        try:
            self.rowLines = int(defaults.objectForKey_( u'txtNoOfMaxRowLines'))
            self.menRowLines.setTitle_( str(self.rowLines) )
            self.optValueVisible.setState_( defaults.objectForKey_( u'optValueColumn') )
            self.optCommentVisible.setState_( defaults.objectForKey_( u'optCommentColumn') )
            self.optTypeVisible.setState_( defaults.objectForKey_( u'optTypeColumn') )

            self.optAlterLines.setState_( defaults.objectForKey_( u'optAlternateLines') )
            self.optVariableRow.setState_( defaults.objectForKey_( u'optVariableRowHeight') )
            self.optVLines.setState_( defaults.objectForKey_( u'optVLines') )
            self.optHLines.setState_( defaults.objectForKey_( u'optHLines') )

        except StandardError, err:
            print "ERROR reading defaults.", repr(err)

        if document.fileType() in (CactusPLISTType,):
            # disable value column for plist (for now)
            self.optValueVisible.setState_( False )

        if document.fileType() in (CactusXMLType, CactusHTMLType, CactusPLISTType):
            # enable comment column
            self.optCommentVisible.setState_( True )

        self.applySettings_(None)

        self.retain()
        return self


    def windowWillClose_(self, notification):
        if kwlog:
            print "CactusOutlineWindowController.windowWillClose_()"
        # see comment in self.initWithObject_()
        #
        # TBD: check model.dirty
        #
        self.autorelease()


    def doubleClick_(self, sender):
        if kwlog:
            print "CactusOutlineWindowController.doubleClick_()"


    def reloadData_(self, item=None, children=False):
        if kwlog:
            print "CactusOutlineWindowController.reloadData_()"
        if item == None:
            self.outlineView.reloadData()
        else:
            self.outlineView.reloadItem_reloadChildren_( item, children )


    def loadFile_(self, sender):
        if kwlog:
            print "EMPTY CactusOutlineWindowController.loadFile_()"
            

    def applySettings_(self, sender):
        """target of the document check boxes. sets some tableview settings.
        """

        if kwlog:
            print "CactusOutlineWindowController.applySettings_()"

        # rowHeight
        self.variableRowHeight = self.optVariableRow.state()

        # alterLines
        alterLines = self.optAlterLines.state()
        self.outlineView.setUsesAlternatingRowBackgroundColors_( alterLines )

        # columns
        tableColumns = self.outlineView.tableColumns()
        
        if self.optNameVisible.state():
            if not self.nameColumn in tableColumns:
                self.outlineView.addTableColumn_(self.nameColumn)
        else:
            if self.nameColumn in tableColumns:
                self.outlineView.removeTableColumn_(self.nameColumn)

        if self.optTypeVisible.state():
            if not self.typeColumn in tableColumns:
                self.outlineView.addTableColumn_(self.typeColumn)
        else:
            if self.typeColumn in tableColumns:
                self.outlineView.removeTableColumn_(self.typeColumn)

        if self.optValueVisible.state():
            if not self.valueColumn in tableColumns:
                self.outlineView.addTableColumn_(self.valueColumn)
        else:
            if self.valueColumn in tableColumns:
                self.outlineView.removeTableColumn_(self.valueColumn)

        if self.optCommentVisible.state():
            if not self.commentColumn in tableColumns:
                self.outlineView.addTableColumn_(self.commentColumn)
        else:
            if self.commentColumn in tableColumns:
                self.outlineView.removeTableColumn_(self.commentColumn)

        if self.txtOutlineType:
            self.txtOutlineType.setStringValue_( unicode( self.document.fileType() ) )

        # lines per row menu
        try:
            l = self.menRowLines.title()
            l = int(l)
            self.rowLines = l
        except StandardError, err:
            print "\nERROR  ---  Menu Row lines '%'" % repr(l)
            self.rowLines = 4
            self.menRowLines.setTitle_( u"4" )
        
        # grid style
        gridStyleMask = self.outlineView.gridStyleMask()
        newStyle = NSTableViewGridNone
        if self.optVLines.state():
            newStyle |= NSTableViewSolidVerticalGridLineMask
        if self.optHLines.state():
            newStyle |= NSTableViewSolidHorizontalGridLineMask
        self.outlineView.setGridStyleMask_(newStyle)

        #
        self.outlineView.reloadData()
        self.outlineView.setNeedsDisplay_( True )


def openOPML_(rootOPML, urltag=None):
    if kwlog:
        print "openOPML_()"
    """This builds the node tree and returns the root node."""
    #
    #  Split this up.
    def getChildrenforNode(node, children, root):
        for c in children:
            name = c.get('name', '')
            childs = c.get('children', [])
            content = c.get('attributes', "")
            comment = ""
            if content == "":
                content = {u'value': ""}
            content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    if k == "comment":
                        comment = v
                    else:
                        l.append( (k, v) )
                content = l
            else:
                content = u""

            newnode = OutlineNode(name, content, node, typeOutline, root)
            if comment:
                newnode.setComment_( comment )
            node.addChild_( newnode )
            if len(childs) > 0:
                getChildrenforNode(newnode, childs, root)

    ######

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)
    
    # get opml head section
    if rootOPML['head']:
        
        # the outline head node
        head = OutlineNode("head", "", root, typeOutline, root)
        root.addChild_( head )
        headtags = set()
        for headnode in rootOPML['head']:
            k, v = headnode
            headtags.add( k )
            head.addChild_( OutlineNode(k, v, head, typeOutline, root) )

        if urltag:
            if 'cactusUrl' not in headtags:
                # add this url only once, not for every open
                head.addChild_(OutlineNode('cactusUrl', unicode(urltag), head, typeOutline, root))
    # fill in missing opml attributes here
    # created, modified
    #
    # how to propagate expansionstate, windowState?
    # make a document object and pass that to docdelegate?
    #
    # get opml body section
    if rootOPML['body']:
        # pdb.set_trace()
        # the outline body node
        body = OutlineNode("body", "", root, typeOutline, root)
        root.addChild_( body )

        for item in rootOPML['body']:
            name = item['name']
            children = item['children']
            comment = ""


            # make table here
            content = item.get('attributes', "")
            content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    if k == "comment":
                        comment = v
                    else:
                        l.append( (k, v) )
                content = l
            else:
                content = u""

            node = OutlineNode(name, content, body, typeOutline, root)
            if comment:
                node.setComment_( comment )
            # node.setValue_(content)
            body.addChild_( node )
            if len(children) > 0:
                try:
                    getChildrenforNode( node, children, root )
                except Exception, err:
                    print err
                    # pdb.set_trace()
                    pp(children)
                    pp(item)
    #title = os
    return root, CactusOPMLType

def openXML_( rootXML):

    if kwlog:
        s = repr(rootXML)
        if len(s) > 90:
            s = s[:91]
        print "openXML_( %s )" % s

    """This builds the node tree and returns the root node."""

    #
    #  Split this up.
    def getChildrenforNode(node, children, root):
        for c in children:
            name = c.get('name', '')
            tail = c.get('tail', '')
            childs = c.get('children', [])
            content = c.get('attributes', "")
            txt = c.get('text', "")

            if content == "":
                content = {u'': ""}

            if content or tail:
                l = []
                for k, v in content.items():
                    l.append( (k, v) )
                if tail != u"":
                    l.append( (u'tail', tail) )
                content = l
            else:
                content = u""

            try:
                newnode = OutlineNode(name, content, node, typeOutline, root)
            except Exception, err:
                print "\n\nERROR in openXML_()"
                tb = unicode(traceback.format_exc())
                print err
                print
                print tb
                print

            if txt != "":
                newnode.setComment_( txt )

            node.addChild_( newnode )
            try:
                n = len(childs)
            except Exception, err:
                print 
                # pdb.set_trace()
                print err
            if len(childs) > 0:
                getChildrenforNode(newnode, childs, root)

    ######

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    rootXML = rootXML
    name = rootXML['name']
    children = rootXML['children']
    content = rootXML.get('attributes', "")
    txt = rootXML.get('text', "")

    if content:
        l = []
        for k, v in content.items():
            l.append( (k, v) )
        content = l
    else:
        content = u""

    node = OutlineNode(name, content, root, typeOutline, root)
    if txt:
        node.setComment_( txt )

    root.addChild_( node )

    try:
        n = len(children)
    except Exception, err:
        print type(children)
        # pdb.set_trace()
        print err
        

    if n > 0:
        try:
            getChildrenforNode( node, children, root )
        except Exception, err:
            print "\n\nERROR in openXML_()"
            tb = unicode(traceback.format_exc())
            print err
            print
            print tb
            print
            # pp(children)
    #title = os
    return root, CactusXMLType

def openRSS_(url):

    url = NSURL2str(url)

    if kwlog:
        s = repr(url)
        if len(s) > 90:
            s = s[:91]
        print "openRSS_( %s )" % repr(s)
    d = feedparser.parse( url, agent=CactusVersion.user_agent )

    # make basic nodes
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    head = OutlineNode("head", "", root, typeOutline, root)
    root.addChild_( head )

    body = OutlineNode("body", "", root, typeOutline, root)
    root.addChild_( body )

    #
    # head
    #
    
    # feed = docs, generator, language, link, microblog_archive,
    # microblog_endday, microblog_filename, microblog_startday, microblog_url,
    # published, subtitle, title, updated, cloud
    if d.feed:
        keys = """author authors category comments cloud description docs enclosure generator
                  generator_detail guid image language link links microblog_archive
                  microblog_endday microblog_filename microblog_startday
                  microblog_url published pubDate source subtitle subtitle_detail
                  sy_updatefrequency sy_updateperiod title title_detail updated
                  updated_parsed""".split()

        feedkeys = d.feed.keys()
        feedkeys.sort()

        for k in feedkeys:

            if k in ('links', 'tags', 'updated_parsed', 'authors'):
                continue

            v = d.feed[k]
            if type(v) in (list,):
                if len(v) > 1:
                    print "Large header list"
                    print k
                    print repr(v)
                elif len(v) == 1:
                    v = v[0]

            if type(v) not in (str, unicode, NSString,
                               NSMutableString, objc.pyobjc_unicode):
                if isinstance(v, dict):
                    l = []
                    for key, val in v.items():
                        l.append( (key,val) )
                    v = l
                elif type(v) == time.struct_time:
                    v = time.asctime(v)
                else:
                    # if k in ('',)
                    if 1:
                        print "ATTENTION RSS Head values"
                        print "KEY:", k
                        print "TYPE:", type(v)
                        print "REPR:", repr(v)
                        print
                    v = repr(v)
            node = OutlineNode(k, v, head, typeOutline, root)
            head.addChild_( node )

    otherkeys = d.keys()

    if 'feed' in otherkeys:
        otherkeys.remove("feed")

    if 'entries' in otherkeys:
        otherkeys.remove("entries")

    otherkeys.sort()
    for k in otherkeys:
        v = d[k]
        if type(v) not in (str, unicode, NSString, NSMutableString,
                           objc.pyobjc_unicode,
                           dict, feedparser.FeedParserDict):
            v = repr(v)
        node = OutlineNode(k, v, head, typeOutline, root)
        head.addChild_( node )
        
    if 0:
        # encoding
        if 'encoding' in d:
            node = OutlineNode('encoding', d.encoding, head, typeOutline, root)
            head.addChild_( node )

        # bozo
        if 'bozo' in d:
            node = OutlineNode('bozo', str(d.bozo), head, typeOutline, root)
            head.addChild_( node )

        # etag
        if 'etag' in d:
            node = OutlineNode('etag', d.etag, head, typeOutline, root)
            head.addChild_( node )

        # headers dict
        if 'headers' in d:
            node = OutlineNode('headers', d.headers, head, typeOutline, root)
            head.addChild_( node )

        # href
        if 'href' in d:
            node = OutlineNode('href', d.href, head, typeOutline, root)
            head.addChild_( node )
        
        # namespaces
        if 'namespaces' in d:
            # pdb.set_trace()
            node = OutlineNode('namespaces', d.namespaces, head, typeOutline, root)
            head.addChild_( node )
        
        # version
        if 'version' in d:
            node = OutlineNode('version', d.version, head, typeOutline, root)
            head.addChild_( node )
    
    #
    # body
    #
    for entry in d.entries:
        name = ""
        if 'title' in entry:
            # name = entry.title + "\n\n"
            name = entry.title
        elif 'summary' in entry:
            name = entry.summary

        #if 'summary' in entry:
        #    name = name + entry.summary
        value = entry
        killkeys = ['links', 'authors', 'tags']
        value['type'] = "rssentry"
        #
        # killing items which have a dictionary as value
        #
        # too much detail for now
        for k, v in value.items():
            if isinstance(v, dict) or isinstance(v, list) :
                killkeys.append(k)
            if k.endswith('_parsed'):
                killkeys.append(k)

        # extract enclosure
        if 'links' in value:
            links = value['links']
            for link in links:
                rel = link.get('rel', False)
                if rel == 'enclosure':
                    s = "%s<<<%s;%s" % (link.get('url',''),
                                        str(link.get('length','')),
                                        link.get('type', ""))
                    value['enclosure'] = s
        for k in killkeys:
            value.pop( k, None )

        node = OutlineNode(name, value, body, typeOutline, root)
        body.addChild_( node )
    return root, CactusRSSType


def getPLISTValue(nsvalue):
    valueType = type(nsvalue)
    value = ""
    valueTypeName = ""
    if valueType == bool:
        # print "BOOLVALUE: '%s' --> '%s'" % (repr(nsvalue), repr(bool(nsvalue)) )
        value = repr(bool(nsvalue))
        valueTypeName = [ ('cactusNodeType', "bool") ]
    
    # number
    elif hasattr(nsvalue, "descriptionWithLocale_"):
        value = unicode(nsvalue.descriptionWithLocale_( None ))
        valueTypeName = [ ('cactusNodeType', "number") ]
    
    # data
    elif hasattr(nsvalue, "bytes"):
        value = unicode( binascii.hexlify(nsvalue.bytes()) )
        valueTypeName = [ ('cactusNodeType', "data") ]
    
    # anything else
    elif hasattr(nsvalue, "description"):
        value = unicode(nsvalue.description())
        valueTypeName = [ ('cactusNodeType', "string") ]
    else:
        print "BOGATIVE VALUE TYPE:", repr(valueType)
        #pdb.set_trace()
        print
    return value, valueTypeName


# 
cactusBool = [ ('cactusNodeType', "bool") ]
cactusString = [ ('cactusNodeType', "string") ]
cactusNumber = [ ('cactusNodeType', "number") ]
cactusDictionary = [ ('cactusNodeType', "dictionary") ]
cactusData = [ ('cactusNodeType', "data") ]


def openIML_( nsdict ):
    if kwlog:
        s = repr(nsdict)
        if len(s) > 90:
            s = s[:91]
        print "openPLIST_( %s )" % s

    """This builds the node tree and returns the root node."""

    ######

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    progressCount = 0

    def getTracks( nsdict, parent ):
        # pdb.set_trace()
        i = 0
        id_trackname = {}
        for trackItem in nsdict:
            trackData = nsdict.objectForKey_( trackItem )
            trackNode = OutlineNode("", "", parent, typeOutline, root)
            trackAttributes = []
            trackName = ""
            trackAlbum = ""
            trackArtist = ""
            trackID = ""
            for trackAttribute in trackData:
                nsvalue = trackData.objectForKey_( trackAttribute )
                value, valueType = getPLISTValue( nsvalue)

                if trackAttribute == u"Track ID":
                    trackID = value

                elif trackAttribute == u"Name":
                    trackName = value

                elif trackAttribute == u"Album":
                    trackAlbum = value

                elif trackAttribute in (u"File Creator", u"File Type"):
                    value = num2ostype( long(value) )

                elif trackAttribute == u"Total Time":
                    # formatted duration hack
                    secondsTotal = int(value) / 1000.0
                    minutes = secondsTotal // 60
                    seconds = round(secondsTotal % 60, 1)
                    seconds = "0%.1f" % seconds
                    value = u"%i:%s" % (minutes, seconds[-4:])

                trackAttributes.append( (trackAttribute, value) )
                id_trackname[ trackID ] = trackName

            # itemName = u"%s - %s" % (trackAlbum, trackName)
            itemName = trackName

            # print repr(itemName)
            trackNode.setName_( itemName )
            trackNode.setValue_( trackAttributes )
            trackNode.setMaxLineHeight()
            parent.addChild_( trackNode )
            i += 1
            if i % 1000 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
                if i % 100000 == 0:
                    sys.stdout.write('\n')
                    sys.stdout.flush()
        print
        print "%i Tracks." % i
        return id_trackname

    def makePlaylistNode( name, curPlaylist, value, parent, root, type_):
        if name in curPlaylist:
                
            if type_ == cactusData:
                value = unicode( binascii.hexlify(value.bytes()) )
            elif type_ == cactusBool:
                value = repr(bool(value))
            elif type_ == cactusNumber:
                value = unicode(value.descriptionWithLocale_( None ))
            # elif type_ == cactusDictionary:

            node = OutlineNode( name,
                                type_,
                                parent,
                                typeOutline,
                                root)
            if value != "":
                node.setComment_( unicode(value) )
            parent.addChild_( node )
            return node

    def getPlaylists( nsdict, parent, id_track_dict ):
        # pdb.set_trace()

        defaults = NSUserDefaults.standardUserDefaults()
        optIMLImportSystemLibraries = defaults.objectForKey_( u'optIMLImportSystemLibraries')
        systemLibraries = (
            u"Library",
            u"Music",
            u"Movies",
            u"Podcasts",
            u"iTunes U",
            u"Books")

        root = parent.rootNode
        # add the standard playlist attributes
        i = 0
        for playlist in nsdict:

            #
            # check for keys not listed here
            #

            playlistName = playlist.get( u"Name", "")

            playlistNode = OutlineNode( playlistName, "", parent, typeOutline, root)
            parent.addChild_( playlistNode )

            # drop out if AllItems pref is false
            if playlistName in systemLibraries:
                if not optIMLImportSystemLibraries:
                    continue

            makePlaylistNode( u"Name", playlist,
                              playlistName,
                              playlistNode, root, cactusString)

            makePlaylistNode( u"Master", playlist,
                              playlist.get( u"Master", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Playlist ID", playlist,
                              playlist.get( u"Playlist ID", "0"),
                              playlistNode, root, cactusNumber)

            makePlaylistNode( u"Playlist Persistent ID", playlist,
                              playlist.get( u"Playlist Persistent ID", ""),
                              playlistNode, root, cactusString)

            makePlaylistNode( u"Parent Persistent ID", playlist,
                              playlist.get( u"Playlist Persistent ID", ""),
                              playlistNode, root, cactusString)

            makePlaylistNode( u"Distinguished Kind", playlist,
                              playlist.get( u"Distinguished Kind", 0),
                              playlistNode, root, cactusNumber)

            makePlaylistNode( u"Movies", playlist,
                              playlist.get( u"Movies", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Podcasts", playlist,
                              playlist.get( u"Podcasts", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"iTunesU", playlist,
                              playlist.get( u"iTunesU", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Audiobooks", playlist,
                              playlist.get( u"Audiobooks", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Smart Info", playlist,
                              playlist.get( u"Smart Info", ""),
                              playlistNode, root, cactusData)

            makePlaylistNode( u"Smart Criteria", playlist,
                              playlist.get( u"Smart Criteria", ""),
                              playlistNode, root, cactusData)

            makePlaylistNode( u"Visible", playlist,
                              playlist.get( u"Visible", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"All Items", playlist,
                              playlist.get( u"All Items", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Folder", playlist,
                              playlist.get( u"Folder", "False"),
                              playlistNode, root, cactusBool)

            plnode = makePlaylistNode( u"Playlist Items", playlist,
                                       "",
                                       playlistNode, root, cactusDictionary)

            i += 7
            j = 0

            if not u"Playlist Items" in playlist:
                continue

            for item in playlist[ u"Playlist Items" ]:
                id_ = item[u"Track ID"]
                attrs = {
                    u"Track ID": id_
                }
                
                name = id_track_dict.get(unicode(id_), "###Noname###")
    
                node = OutlineNode( name, attrs, plnode, typeOutline, root)
                plnode.addChild_( node )
    
                i += 1
                j += 1
                if i % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    if i % 100000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
            print
            print "%s has %i Playlist Items." % (repr(playlistName), j)
        print
        print "A total of %i Playlist Items." % i


    def dispatchLevel( nsdict, parent, root, progressCount ):
        # array or dict
        i = 0
        selfTypeName = "None"
        if hasattr(nsdict, "objectForKey_"):
            selfTypeName = "dictionary"
        elif hasattr(nsdict, "objectAtIndex_"):
            selfTypeName = "list"

        selfType = [ ('cactusNodeType', selfTypeName) ]

        parent.setValue_( selfType )

        id_track_dict = {}
        for key in nsdict:
            i += 1

            typeAttribute = ""
            value = ""

            if selfTypeName == "list":
                itemName = str(i)
                nsvalue = nsdict.objectAtIndex_( i-1 )
            else:
                itemName = unicode(key)
                nsvalue = nsdict.objectForKey_(key)

            valueType = type(nsvalue)

            node = OutlineNode(itemName, "", parent, typeOutline, root)

            if itemName == u"Tracks":
                id_track_dict = getTracks( nsvalue, node )
            elif itemName == u"Playlists":
                getPlaylists( nsvalue, node, id_track_dict )
            else:
                # dict
                if hasattr(nsvalue, "objectForKey_"):
                    progressCount = dispatchLevel(nsvalue, node, root, progressCount)
    
                # list
                elif hasattr(nsvalue, "objectAtIndex_"):
                    progressCount = dispatchLevel(nsvalue, node, root, progressCount)
    
                else:
                    value, valueType = getPLISTValue( nsvalue )
                    node.setValue_( valueType )
            node.setComment_( value )
            parent.addChild_(node)
            progressCount += 1
            if kwlog:
                if progressCount % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    if progressCount % 100000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
        return progressCount

    dispatchLevel(nsdict, root, root, progressCount)
    return root, CactusIMLType

###
#
# plist tools
#
###

def num2ostype( num ):
    return struct.pack(">I", num)

def ostype2num( ostype ):
    return struct.pack('BBBB', list(ostype))


def openPLIST_( nsdict ):

    if kwlog:
        s = repr(nsdict)
        if len(s) > 90:
            s = s[:91]
        print "openPLIST_( %s )" % s

    """This builds the node tree and returns the root node."""

    ######

    # check for itunes xml file
    defaults = NSUserDefaults.standardUserDefaults()
    optIMLAutodetect = defaults.objectForKey_( u'optIMLAutodetect')

    if optIMLAutodetect:
        isIML = True
        for key in (u"Music Folder", u"Application Version",
                    u"Tracks", u"Playlists",
                    u"Minor Version", u"Major Version"):
            if key not in nsdict:
                isIML = False
                break
        if isIML:
            return openIML_( nsdict )

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    progressCount = 0

    def dispatchLevel( nsdict, parent, root, progressCount ):
        # array or dict
        i = 0

        if hasattr(nsdict, "objectForKey_"):
            selfTypeName = "dictionary"
        elif hasattr(nsdict, "objectAtIndex_"):
            selfTypeName = "list"
        else:
            selfTypeName = "None"
        selfType = [ ('cactusNodeType', selfTypeName) ]

        parent.setValue_( selfType )

        for key in nsdict:
            i += 1

            typeAttribute = ""
            value = ""

            if selfTypeName == "list":
                itemName = str(i)
                nsvalue = nsdict.objectAtIndex_( i-1 )
            else:
                itemName = unicode(key)
                nsvalue = nsdict.objectForKey_(key)

            valueType = type(nsvalue)

            node = OutlineNode(itemName, "", parent, typeOutline, root)

            if valueType == bool:
                # print "BOOLVALUE: '%s' --> '%s'" % (repr(nsvalue), repr(bool(nsvalue)) )
                value = repr(bool(nsvalue))
                node.setValue_( [ ('cactusNodeType', "bool") ] )

            # dict
            elif hasattr(nsvalue, "objectForKey_"):
                dispatchLevel(nsvalue, node, root, progressCount)

            # list
            elif hasattr(nsvalue, "objectAtIndex_"):
                dispatchLevel(nsvalue, node, root, progressCount)

            # number
            elif hasattr(nsvalue, "descriptionWithLocale_"):
                value = unicode(nsvalue.descriptionWithLocale_( None ))
                node.setValue_( [ ('cactusNodeType', "number") ] )

            # data
            elif hasattr(nsvalue, "bytes"):
                value = unicode( binascii.hexlify(nsvalue.bytes()) )
                node.setValue_( [ ('cactusNodeType', "data") ] )

            # anything else
            elif hasattr(nsvalue, "description"):
                value = unicode(nsvalue.description())
                node.setValue_( [ ('cactusNodeType', "string") ] )
            else:
                print "BOGATIVE VALUE TYPE:", repr(valueType)
                #pdb.set_trace()
                print

            node.setComment_( value )
            parent.addChild_(node)
            progressCount += 1
            if kwlog:
                if progressCount % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    if progressCount % 100000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
    dispatchLevel(nsdict, root, root, progressCount)
    return root, CactusPLISTType
