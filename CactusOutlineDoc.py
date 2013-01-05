
# -*- coding: utf-8 -*-


"""
"""

import sys
import os
import traceback

import time
import datetime
import urllib

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import cStringIO

import pdb
import pprint
pp = pprint.pprint
kwdbg = True
kwlog = True

import feedparser

import opml

import CactusVersion

import CactusTools
readURL = CactusTools.readURL
errorDialog = CactusTools.errorDialog
NSURL2str = CactusTools.NSURL2str

import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException
XMLParseErrorException = CactusExceptions.XMLParseErrorException
HTMLParseErrorException = CactusExceptions.HTMLParseErrorException

import objc

import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL
NSData = Foundation.NSData

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

    head.addChild_(OutlineNode("dateCreated", s, head, typeOutline, root))
    head.addChild_(OutlineNode("dateModified", s, head, typeOutline, root))
    head.addChild_(OutlineNode("ownerName", "", head, typeOutline, root))
    head.addChild_(OutlineNode("ownerEmail", "", head, typeOutline, root))
    head.addChild_(OutlineNode("expansionState", "", head, typeOutline, root))
    head.addChild_(OutlineNode("vertScrollState", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowTop", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowLeft", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowBottom", "", head, typeOutline, root))
    head.addChild_(OutlineNode("windowRight", "", head, typeOutline, root))

    body = OutlineNode("body", "", rootNode, typeOutline, root)
    rootNode.addChild_( body )

    body.addChild_( OutlineNode("", "", body, typeOutline, root) )


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
                root = openOPML_( d, urltag=NSURL2str(url) )
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
            root = openRSS_( url )
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

            root = openXML_( d )

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

            root = openXML_( d )

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
                
                self.makeWindowControllers()
                self.showWindows()

            # check opml file metadata
            if theType == CactusOPMLType:
                pass
            return (self, err)

        # could not create document
        return (None, err)


    def initWithType_error_(self, theType):
        
        if kwlog:
            print "CactusOutlineDocument.initWithType_error_( %s )" % (repr(theType),)

        self = self.init()
        if not self:
            return (None, None)

        self.setFileType_( theType )

        self.rootNode = OutlineNode("__ROOT__", "", None, typeOutline, None)
        boilerplateOPML( self.rootNode )
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


    def dataRepresentationOfType_( self, theType ):
        if kwlog:
            print "CactusOutlineDocument.dataRepresentationOfType_( %s )" % repr(theType)

        # future scaffolding
        if theType == CactusOPMLType:

            rootOPML = opml.generateOPML( self.rootNode, indent=1 )

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
            rootXML = opml.generateXML( self.rootNode) #, indent=1 )

            e = etree.ElementTree( rootXML )

            fob = cStringIO.StringIO()
            # e.write(fob, pretty_print=True, encoding="utf-8", xml_declaration=True, method="xml" )
            e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
            t = fob.getvalue()
            fob.close()
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusHTMLType:
            rootHTML = opml.generateHTML( self.rootNode) #, indent=1 )
            if rootHTML:
                e = etree.ElementTree( rootXML )
    
                fob = cStringIO.StringIO()
                # e.write(fob, pretty_print=True, encoding="utf-8", xml_declaration=True, method="xml" )
                e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
                t = fob.getvalue()
                fob.close()
                return NSData.dataWithBytes_length_(t, len(t))

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
                root = openOPML_( d )
                if self.rootNode:
                    pass
                    # release here
                self.rootNode = root
                readSuccess = True

        elif theType == CactusDocumentTypes.CactusRSSType:
            d = feedparser.parse( s, agent=CactusVersion.user_agent )
            if d:
                root = openRSS_( d )
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
            searchKeys = ( 'dateCreated dateModified ownerName ownerEmail '
                           'expansionState windowTop windowLeft windowBottom '
                           'windowRight'.split() )
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
                rows = False
                if "expansionState" in meta:
                    rows = meta[ 'expansionState' ]
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

        outlineView.setNeedsDisplay_( True )

    def makeWindowControllers(self):
        if kwlog:
            print "CactusOutlineDocument.makeWindowControllers()"
        self.addWindowController_( CactusOutlineWindowController.alloc().initWithObject_( self ) )


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

        # check if needed
        self.document = document

        if not isinstance(document, CactusOutlineDocument):
            print "FAKE document"
            # pdb.set_trace()
            print "FAKE document"

        path = False
        if document.url:
            if document.url.isFileURL():
                path = unicode(document.url.path())
            else:
                path = NSURL2str(document.url)
        # path is a string or False now

        self.rootNode = document.rootNode
        self.parentNode = document.parentNode
        title = document.title

        # get window name from url or path
        if path:
            if os.path.exists(path):
                fld, fle = os.path.split(path)
                title = fle
            else:
                title = path
        else:
            # keep unnamed title
            pass

        self.window().setTitle_( title )

        self.model = OutlineViewDelegateDatasource.alloc().initWithObject_type_parentNode_(
                                                self.rootNode,
                                                typeOutline,
                                                self.parentNode )

        # this is evil, and doesn't work
        self.rootNode.model = self.model
        
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

        # defaults to name & value visible, type & comment invisible
        self.optTypeVisible.setState_( False )

        self.optCommentVisible.setState_( False )
        if document.fileType() in (CactusXMLType, CactusHTMLType):
            # enable comment column
            self.optCommentVisible.setState_( True )

        self.menRowLines.setTitle_( u"2" )

        self.applySettings_(None)

        # The window controller doesn't need to be retained (referenced)
        # anywhere, so we pretend to have a reference to ourselves to avoid
        # being garbage collected before the window is closed. The extra
        # reference will be released in self.windowWillClose_()
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
            self.outlineView.reloadData() #reloadItem_reloadChildren_( item, True )
        else:
            self.outlineView.reloadItem_reloadChildren_( item, children )

    def loadFile_(self, sender):
        if kwlog:
            print "EMPTY CactusOutlineWindowController.loadFile_()"
            

    def applySettings_(self, sender):
        """target of the apply button. sets some tableview settings.
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
            if content == "":
                content = {u'value': ""}
            content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    l.append( (k, v) )
                content = l
            else:
                content = u""

            newnode = OutlineNode(name, content, node, typeOutline, root)
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

        # the outline body node
        body = OutlineNode("body", "", root, typeOutline, root)
        root.addChild_( body )

        for item in rootOPML['body']:
            name = item['name']
            children = item['children']


            # make table here
            content = item.get('attributes', "")
            content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    l.append( (k, v) )
                content = l
            else:
                content = u""

            node = OutlineNode(name, content, body, typeOutline, root)
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
    return root

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
            childs = c.get('children', [])
            content = c.get('attributes', "")
            txt = c.get('text', "")
            if content == "":
                # content = {u'value': ""}
                content = {u'': ""}
            # content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    l.append( (k, v) )
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

            if txt:
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
    return root

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
    return root
