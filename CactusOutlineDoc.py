
# -*- coding: utf-8 -*-

from __future__ import print_function


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

import CactusOPML

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
NSApplication = AppKit.NSApplication
NSDocument = AppKit.NSDocument
NSDocumentController = AppKit.NSDocumentController
NSWorkspace = AppKit.NSWorkspace
NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString
NSWindowController = AppKit.NSWindowController
NSPrintOperation = AppKit.NSPrintOperation

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
#import PyObjCTools.NibClassBuilder
#extractClasses = PyObjCTools.NibClassBuilder.extractClasses
#AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass


import CactusOutlineTypes
typeOutline = CactusOutlineTypes.typeOutline
typeTable = CactusOutlineTypes.typeTable
typeBrowser = CactusOutlineTypes.typeBrowser


import CactusOutline
OutlineViewDelegateDatasource = CactusOutline.OutlineViewDelegateDatasource

import CactusOutlineNode
OutlineNode = CactusOutlineNode.OutlineNode

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType
CactusPLISTType = CactusDocumentTypes.CactusPLISTType
CactusIMLType = CactusDocumentTypes.CactusIMLType

# extractClasses("OutlineEditor")

import CactusFileOpeners

openOPML_ = CactusFileOpeners.openOPML_
openOPML_withURLTag_ = CactusFileOpeners.openOPML_withURLTag_
openXML_ = CactusFileOpeners.openXML_
openRSS_ = CactusFileOpeners.openRSS_
getPLISTValue = CactusFileOpeners.getPLISTValue
openIML_ = CactusFileOpeners.openIML_
openPLIST_ = CactusFileOpeners.openPLIST_


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

def boilerplateOPML( rootNode ):
    """Creates the minimal outline nodes for the OPML structure.

    rootNode - the node under which the structure will be created

    """
    if kwlog:
        print( "boilerplateOPML()" )

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
    except StandardError as err:
        print( "ERROR reading defaults.", repr(err) )

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
    if 0:
        print( "root:", root.retainCount() )
        print( "head:", head.retainCount() )
        print( "body:", body.retainCount() )
    return


# a cocoa NSDocument subclass
class CactusOutlineDocument(NSDocument):
    parentNode = objc.IBOutlet()
    rootNode = objc.IBOutlet()
    url = objc.IBOutlet()

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

    def __repr__(self):
        s = u"CactusOutlineDocument\n"
        s = s + u"    rootNode: '%s'\n" % self.rootNode
        s = s + u"    parentNode: '%s'\n" % self.parentNode
        s = s + u"    url: '%s'\n" % self.url
        s = s + u"    title: '%s'\n" % self.title
        s = s + u"    outlineView: '%s'\n" % self.outlineView
        return s.encode("utf-8")

    def init(self):
        if kwlog:
            print( "CactusOutlineDocument.init()" )
        self = objc.super( CactusOutlineDocument, self).init()

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
        print( "CactusOutlineDocument.dealloc()" )
        objc.super(CactusOutlineDocument, self).dealloc()


    def autosavingFileType(self):
        """2012-12-12 KW created to disable autosaving."""
        return None

    def readFromURL_ofType_error_(self, url, theType, err):
        if kwlog:
            msg = "CactusOutlineDocument.readFromURL_ofType_error_( %s, %s )\n"
            print( msg % (repr(url), repr(theType)) )

        OK = True
        s = None
        err = None
        self.url = url

        # read opml content
        if theType == CactusOPMLType:
            d = None
            try:
                d = CactusOPML.opml_from_string( readURL( url, CactusOPMLType ) )
            except OPMLParseErrorException as v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            if d:
                root, theType = openOPML_withURLTag_( d, NSURL2str(url) )
                del d
                if not root:
                    if kwlog:
                        print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
                    return (False, "Error creating the outline.")
                else:
                    self.rootNode = root
                    if not url.isFileURL():
                        self.updateChangeCount_( NSChangeReadOtherContents )
                    else:
                        self.updateChangeCount_( NSChangeCleared )
            else:
                if kwlog:
                    print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
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
                    print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
                return (False, None)

        # read xml content
        elif theType == CactusXMLType:
            d = None
            try:
                d = CactusOPML.xml_from_string( readURL( url, CactusXMLType ) )
            except XMLParseErrorException as v:
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
                    print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
                return (False, None)

        # read html content
        elif theType == CactusHTMLType:
            d = None
            try:
                d = CactusOPML.html_from_url( url )
            except HTMLParseErrorException as v:
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
                    print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
                return (False, None)

        # read plist content
        elif theType == CactusPLISTType:
            d = None
            try:
                d = CactusOPML.parse_plist( url )
            except PLISTParseErrorException as v:
                tb = unicode(traceback.format_exc())
                v = unicode( repr(v) )
                err = tb
                errorDialog( message=v, title=tb )
                return (False, None)

            # may return ttheType=CactusPLISTType
            root, theType = None, None
            if d:
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
                    print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
                return (False, None)

        # read itunes music xml
        elif theType == CactusIMLType:
            d = None
            try:
                d = CactusOPML.parse_plist( url )
            except PLISTParseErrorException as v:
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
                    print( "FAILED CactusOutlineDocument.readFromURL_ofType_error_()" )
                return (False, None)

        else:
            OK = False

        if OK:
            self.setFileURL_( url )
            self.setFileType_( theType )

        print( "OK CactusOutlineDocument.readFromURL_ofType_error_()" )
        return (OK, None)


    def initWithContentsOfURL_ofType_error_(self, url, theType, err):
        """Main entry point for opening documents."""
        if kwlog:
            msg = "\nCactusOutlineDocument.initWithContentsOfURL_ofType_error_( %s, %s )\n"
            print( msg % ( repr(theType), repr(url)) )


        self, err = self.initWithType_error_( theType, err )

        if not self:
            return( None, None)

        OK, err = self.readFromURL_ofType_error_( url, theType, err )

        if OK:
            if not url.isFileURL():
                #
                # evil hack, because NSDocumentController doesn't open window if
                # document is loaded with http: scheme
                #
                # addendum 10.6
                #
                # now this does not work anymore
                docc = NSDocumentController.sharedDocumentController()
                docc.addDocument_(self)

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


    def initWithType_error_(self, theType, err):
        if kwlog:
            print( "CactusOutlineDocument.initWithType_error_( %s )" % (repr(theType),) )

        self = self.init()
        if not self:
            return (None, None)

        self.setFileType_( theType )

        self.rootNode = OutlineNode("__ROOT__", "", None, typeOutline, None)
        if kwlog:
            print( "    .initWithType_error_ rootRetaines %i " % (self.rootNode.retainCount(),) )
        boilerplateOPML( self.rootNode )
        if kwlog:
            print( "    .initWithType_error_ boilerplate rootRetaines %i " % (self.rootNode.retainCount(),) )
        self.updateChangeCount_( NSChangeCleared )

        self.variableRowHeight = True
        return (self, None)


    def displayName(self):
        if kwlog:
            print( "CactusOutlineDocument.displayName() ->", )
        title = objc.super( CactusOutlineDocument, self).displayName()

        if 0:
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
            except Exception as err:
                print()
                print( "displayName CRASHED!" )
                print( err )
                print()
            finally:
                pass

        if kwlog:
            print( repr(title) )
        self.title = title
        return title


    def awakeFromNib(self):
        if kwlog:
            print( "CactusOutlineDocument.awakeFromNib()" )


    def XXwindowNibName(self):
        # deactivated
        if kwlog:
            print( "CactusOutlineDocument.windowNibName()" )
        return u"OutlineEditor"


    def fileURL( self ):
        # do nothing the superclass wouldn't do
        if kwlog:
            print( "SUPER CactusOutlineDocument.fileURL()" )
        return objc.super( CactusOutlineDocument, self).fileURL()


    def setFileURL_( self, theURL ):
        # print( "URLType:", type(theURL) )
        if not isinstance( theURL, NSURL ):
            theURL = NSURL.URLWithString_( theURL )
        # do nothing the superclass wouldn't do
        if kwlog:
            print( "SUPER CactusOutlineDocument.setFileURL()", repr(NSURL2str(theURL)) )
        objc.super( CactusOutlineDocument, self).setFileURL_( theURL )
        self.url = theURL




    def windowControllerWillLoadNib_( self, aController):
        # do nothing the superclass wouldn't do
        if kwlog:
            print( "SUPER CactusOutlineDocument.windowControllerWillLoadNib_( %s )" % repr(aController) )
        objc.super( CactusOutlineDocument, self).windowControllerWillLoadNib_(aController)


    def windowControllerDidLoadNib_( self, aController):
        # do nothing the superclass wouldn't do
        if kwlog:
            print( "SUPER CactusOutlineDocument.windowControllerDidLoadNib_( %s )" % repr(aController) )
        objc.super( CactusOutlineDocument, self).windowControllerDidLoadNib_(aController)


    def calculateExpansionState_( self, rootNode ):

        winframe = {}
        rootNode = self.rootNode
        ov = self.outlineView
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
                        print( "idx, items", idx, len(expanded) )

                expanded = [str(i) for i in expanded]
                expanded = ', '.join( expanded )
                if expanded == "":
                    expanded = "1"
                if 1: #kwlog:
                    print( "CactusOutlineDocument.calculateExpansionState_()" )
                    print( "expansionState: ", repr(expanded) )
                    print()
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
            print( "CactusOutlineDocument.dataRepresentationOfType_( %s )" % repr(theType) )

        defaults = NSUserDefaults.standardUserDefaults()

        # future scaffolding
        if theType == CactusOPMLType:

            expansionState = self.calculateExpansionState_( self.rootNode )
            if expansionState == None:
                expansionState = {}
            rootOPML = CactusOPML.generateOPML( self.rootNode, indent=1, expansion=expansionState )

            e = etree.ElementTree( rootOPML )

            fob = cStringIO.StringIO()
            e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
            t = fob.getvalue()
            fob.close()
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusRSSType:
            t = CactusOPML.generateRSS( self.rootNode, indent=1 )
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusXMLType:
            # closed after finding the trailing text bug/misconception
            # return None
            rootXML = CactusOPML.generateXML( self.rootNode) #, indent=1 )

            # check consistency
            if self.rootNode.noOfChildren() > 1:
                firstborn = self.rootNode.childAtIndex_(0)
                name = firstborn.name
                errorDialog(u"Warning",
                    u"XML documents can have only 1 to level node. Every node after '%s' will be ommited on save." % (name,))
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

            except StandardError as err:
                print( "ERROR reading defaults.", repr(err) )

            etHTML = CactusOPML.generateHTML( self.rootNode, doctype, encoding, indent )

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
            return CactusOPML.serializePLISTOutline_( self.rootNode )

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
            print()
            print( "ERROR! Bogus filetype for writing: '%s'" % repr(theType) )
            print()

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
            print( "CactusOutlineDocument.dataRepresentationOfType_( %s ) RETURNED NONE" % repr(theType) )
        return None


    def loadDataRepresentation_ofType_(self, data, aType):
        if kwlog:
            print()
            print( "------ TBD ----- CactusOutlineDocument.loadDataRepresentation_ofType_()" )
            print()
        # Insert code here to read your document from the given data.  You can
        # also choose to override -loadFileWrapperRepresentation:ofType: or
        # -readFromFile:ofType: instead.

        # For applications targeted for Tiger or later systems, you should use
        # the new Tiger API readFromData:ofType:error:.  In this case you can
        # also choose to override -readFromURL:ofType:error: or
        # -readFromFileWrapper:ofType:error: instead.

        return True


    def readFromData_ofType_error_(self, data, typeName, err):
        # This should be deleted
        if kwlog:
            print( "X" * 80 )
            print( "CactusOutlineDocument.readFromData_ofType_error_()" )
            print( "X" * 80 )

        outError = None
        readSuccess = False

        s = str(data.bytes())
        if typeName == CactusOPMLType:
            d = CactusOPML.opml_from_string( s )
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
            print( "ERROR: Wrong type requested: ", repr(typename) )
        return (readSuccess, outError)


    def showWindows( self ):
        if kwlog:
            print( "CactusOutlineDocument.showWindows()" )

        c = objc.super( CactusOutlineDocument, self).showWindows()
        #
        # extract data for expansionstate & window size
        #
        controllers = self.windowControllers()

        defaults = NSUserDefaults.standardUserDefaults()
        doanimate = True
        try:
            doanimate = bool(defaults.objectForKey_( u'optAnimateOPMLOpen'))
        except Exception as err:
            pass

        for controller in controllers:
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
        
            redisplay = True
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

                if rows:
                    try:
                        rows = rows.split(',')
                        rows = [int(i)+1 for i in rows if i]
                    except Exception as err:
                        print( "\nERROR: expansionState reading failed.\n", err )
                        print()
                    if rows:
                        for row in rows:
                            item = outlineView.itemAtRow_( row )
                            outlineView.expandItem_expandChildren_(item, False)

                keys = 'windowLeft windowTop windowRight windowBottom'.split()
                coords = []

                try:
                    for key in keys:
                        coords.append( float( meta[key] ))
                    window = outlineView.window()

                    # this makes the found rect the minimum size of the nib
                    # can the nib values be queried?
                    w = coords[2] - coords[0]
                    h = coords[3] - coords[1]
                    h = max(h, 260.0)
                    w = max(w, 590.0)
                    s = NSMakeRect(coords[0], coords[1], w, h)

                    # animation is too slow, ca 0.5s per file
                    # print( "ANIME:", window.animationResizeTime_( s ) )
                    window.setFrame_display_animate_(s, True, doanimate)

                    # window.setFrame_display_(s, True)
                    redisplay = False
                except StandardError as err:
                    print( err )
                    print( "No window setting for you." )
            outlineView.setNeedsDisplay_( redisplay )

    def makeWindowControllers(self):
        if kwlog:
            print( "CactusOutlineDocument.makeWindowControllers()" )

        c = CactusOutlineWindowController.alloc().init()
        self.addWindowController_( c )
        
        # c.document is set by addWindowController_
        c.finishControllerInit()

    def windowControllers(self):
        if kwlog:
            print( "CactusOutlineDocument.windowControllers()" )
        #pdb.set_trace()
        #print
        return objc.super( CactusOutlineDocument, self).windowControllers()

    def printShowingPrintPanel_(self, show):
        printInfo = self.printInfo()
        printOp = NSPrintOperation.printOperationWithView_printInfo_(
                            self.outlineView, printInfo )
        printOp.setShowPanels_( show )
        self.runModalPrintOperation_delegate_didRunSelector_contextInfo_(
                            printOp, None, None, None )


    #
    # methods to do:
    #
    # writeSafelyToURL_ofType_forSaveOperation_error_


class CactusOutlineWindowController(NSWindowController):
    menRowLines = objc.IBOutlet()
    outlineView = objc.IBOutlet()
    optAlterLines = objc.IBOutlet()
    optCommentVisible = objc.IBOutlet()
    optHLines = objc.IBOutlet()
    optNameVisible = objc.IBOutlet()
    optTypeVisible = objc.IBOutlet()
    optValueVisible = objc.IBOutlet()
    optVariableRow = objc.IBOutlet()
    optVLines = objc.IBOutlet()
    txtOutlineType = objc.IBOutlet()
    txtWindowStatus = objc.IBOutlet()

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

    window # in NSWindowController
    """

    def dealloc(self):
        print( "CactusOutlineWindowController.dealloc()", self.retainCount() )
        #if self.rootNode:
        #    self.rootNode.release()
        #if self.parentNode:
        #    self.parentNode.release()
        print( "DEALLOCDBG model:", self.model, self.model.retainCount() )
        self.model.release()
        objc.super(CactusOutlineWindowController, self).dealloc()

    def init(self):
        self = self.initWithWindowNibName_("OutlineEditor")
        self.retain()
        return self


    def finishControllerInit(self):
        """This controller is used for outline and table windows.

        document is a CactusOutlineDocument

        """
        if kwlog:
            print( "CactusOutlineWindowController.initWithObject_()" )

        # self = self.initWithWindowNibName_("OutlineEditor")
        title = u"Unnamed Outline"

        # self.path = ""
        self.rootNode = None
        self.parentNode = None
        self.variableRowHeight = True
        self.rowLines = 2
        self.url = None

        document = self.document()

        if not isinstance(document, CactusOutlineDocument):
            print( "FAKE document" )

        if document.url:
            # self.nsurl = document.url
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

        if 0:
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

        window = self.window()
        window.setTitle_( self.displayName() )

        self.model = OutlineViewDelegateDatasource.alloc().initWithObject_type_parentNode_(
                                                self.rootNode,
                                                typeOutline,
                                                self.parentNode )

        # needed for drag and drop
        self.model.setOutlineView_( self.outlineView )

        # this is evil, and doesn't work
        # self.rootNode.model = self.model

        # TBD: make this accesssor
        # self.model.document = document

        self.model.setController_( self )

        # this will become very dangerous when a document gets more than 1 window
        #s = self.document()
        #s.outlineView = self.outlineView
        
        document.outlineView = self.outlineView

        self.outlineView.setDataSource_(self.model)
        self.outlineView.setDelegate_(self.model)

        self.outlineView.setTarget_(self)
        # self.outlineView.setDoubleAction_("doubleClick:")

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

        except StandardError as err:
            print( "ERROR reading defaults.", repr(err) )

        if document.fileType() in (CactusPLISTType,):
            # disable value column for plist (for now)
            self.optValueVisible.setState_( False )

        if document.fileType() in (CactusXMLType, CactusHTMLType, CactusPLISTType):
            # enable comment column
            self.optCommentVisible.setState_( True )

        self.applySettings_(None)

        self.showWindow_(self)

        #self.retain()
        #return self

    def nsurl(self):
        result = None
        try:
            result = self.document().fileURL()
        except Exception as err:
            pass
        return result


    def displayName(self):
        # get window name
        if 0: #kwlog:
            print( "CactusOutlineWindowController.displayName() ->", )
        doc = self.document()
        if not doc:
            return ""

        title = doc.title
        url = doc.fileURL()
        
        if url:
            path = unicode(url.path())
            urslstring = NSURL2str( url )
            if os.path.exists( path ):
                fld, fle = os.path.split( path )
                title = fle
            else:
                title = urslstring
        else:
            # keep unnamed title
            pass
        if 0: #kwlog:
            print( repr(title) )
        return title


    def windowWillClose_(self, notification):
        if kwlog:
            print( "CactusOutlineWindowController.windowWillClose_()" )
        # see comment in self.initWithObject_()
        #
        # TBD: check model.dirty
        #
        self.autorelease()


    def doubleClick_(self, sender):
        if kwlog:
            print( "CactusOutlineWindowController.doubleClick_()" )
        #objc.super(CactusOutlineWindowController, self).doubleClick_(sender)

    def reloadData(self):
        if kwlog:
            print( "CactusOutlineWindowController.reloadData()" )
        self.outlineView.reloadData()

    def reloadData_(self, item):
        if kwlog:
            print( "CactusOutlineWindowController.reloadData_(item)" )
        self.outlineView.reloadItem_reloadChildren_( item, True )

    def reloadData_reloadChildren_(self, item, children):
        if kwlog:
            print( "CactusOutlineWindowController.reloadData_reloadChildren_(item, children)" )
        self.outlineView.reloadItem_reloadChildren_( item, children )

    @objc.IBAction
    def loadFile_(self, sender):
        if kwlog:
            print( "-" * 80 )
            print( "EMPTY CactusOutlineWindowController.loadFile_()" )

    @objc.IBAction
    def applySettings_(self, sender):
        """target of the document check boxes. sets some tableview settings.
        """

        if kwlog:
            print( "CactusOutlineWindowController.applySettings_()" )

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
            s = self.document()
            self.txtOutlineType.setStringValue_( unicode( s.fileType() ) )

        # lines per row menu
        try:
            l = self.menRowLines.title()
            l = int(l)
            self.rowLines = l
        except StandardError as err:
            print( "\nERROR  ---  Menu Row lines '%'" % repr(l) )
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
