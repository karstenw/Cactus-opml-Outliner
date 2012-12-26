
# -*- coding: utf-8 -*-


"""
"""

import sys
import os

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

import CactusTools
readURL = CactusTools.readURL


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


extractClasses("OutlineEditor")


def boilerplateOPML( rootNode ):
    """Creates the minimal outline nodes for the OPML structure.

    rootNode - the node under which the structure will be created

    """
    now = datetime.datetime.now()
    s = now.strftime("%a, %d %b %Y %H:%M:%S %Z")
    head = OutlineNode("head", "", rootNode, typeOutline)
    rootNode.addChild_( head )

    head.addChild_(OutlineNode("dateCreated", s, head, typeOutline))
    head.addChild_(OutlineNode("dateModified", s, head, typeOutline))
    head.addChild_(OutlineNode("ownerName", "", head, typeOutline))
    head.addChild_(OutlineNode("ownerEmail", "", head, typeOutline))
    head.addChild_(OutlineNode("expansionState", "", head, typeOutline))
    head.addChild_(OutlineNode("vertScrollState", "", head, typeOutline))
    head.addChild_(OutlineNode("windowTop", "", head, typeOutline))
    head.addChild_(OutlineNode("windowLeft", "", head, typeOutline))
    head.addChild_(OutlineNode("windowBottom", "", head, typeOutline))
    head.addChild_(OutlineNode("windowRight", "", head, typeOutline))

    body = OutlineNode("body", "", rootNode, typeOutline)
    rootNode.addChild_( body )

    body.addChild_( OutlineNode("", "", body, typeOutline) )


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
        self.url = ""

        #
        self.title = "Untitled Outline"

        # one of OPML, RSS
        self.type = None
        return self


    def autosavingFileType(self):
        """2012-12-12 KW created to disable autosaving."""
        return None


    def readFromURL_ofType_error_(self, url, theType):
        if kwlog:
            print ("CactusOutlineDocument.readFromURL_ofType_error_( %s, %s )"
                   % (repr(url), repr(theType),))
            # print repr(url)
            print

        OK = True
        s = None

        self.url = url
        
        s = readURL( url )

        # pdb.set_trace()

        if s:
            if theType == CactusDocumentTypes.CactusOPMLType:
                d = opml.opml_from_string(s)
                if d:
                    root = self.openOPML_( d )
                    if not root:
                        if kwlog:
                            print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                        return (False, None)
                    else:
                        self.rootNode = root
                    
            elif theType == CactusDocumentTypes.CactusRSSType:
                root = self.openRSS_( s )
                if root:
                    self.rootNode = root
                else:
                    if kwlog:
                        print "FAILED CactusOutlineDocument.readFromURL_ofType_error_()"
                    return (False, None)

            del s
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
        # pdb.set_trace()

        self.rootNode = OutlineNode("__ROOT__", "", None, typeOutline)
        # boilerplateOPML( self.rootNode )

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
        # pdb.set_trace()
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
        if theType == CactusDocumentTypes.CactusOPMLType:

            rootOPML = opml.generateOPML( self.rootNode, indent=1 )

            e = etree.ElementTree( rootOPML )

            fob = cStringIO.StringIO()
            e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
            t = fob.getvalue()
            fob.close()
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusDocumentTypes.CactusRSSType:
            t = opml.generateRSS( self.rootNode, indent=1 )
            return NSData.dataWithBytes_length_(t, len(t))

        elif theType == CactusDocumentTypes.CactusTEXTType:
            pass
        elif theType == CactusDocumentTypes.CactusSQLITEType:
            pass
        elif theType == CactusDocumentTypes.CactusXOXOType:
            pass
        elif theType == CactusDocumentTypes.CactusXMLType:
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
            print "CactusOutlineDocument.loadDataRepresentation_ofType_()"
            print "EMPTY"
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
            print "CactusOutlineDocument.readFromData_ofType_error_()"
        # pdb.set_trace()
        outError = None
        readSuccess = False

        #
        # open outline here
        #
        s = str(data.bytes())
        if typeName == CactusDocumentTypes.CactusOPMLType:
            d = opml.opml_from_string( s )
            if d:
                root = self.openOPML_( d )
                if self.rootNode:
                    pass
                    # release here
                self.rootNode = root
                readSuccess = True
        elif theType == CactusDocumentTypes.CactusRSSType:
            d = feedparser.parse( s )
            if d:
                root = self.openRSS_( d )
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
        

    def makeWindowControllers(self):
        if kwlog:
            print "CactusOutlineDocument.makeWindowControllers()"
        wc = CactusOutlineWindowController.alloc().initWithObject_( self )
        self.addWindowController_( wc )


    def openOPML_(self, rootOPML):
        if kwlog:
            print "CactusOutlineDocument.openOPML_()"
        """This builds the node tree and returns the root node."""
        #
        #  Split this up.
        def getChildrenforNode(node, children):
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

                newnode = OutlineNode(name, content, node, typeOutline)
                node.addChild_( newnode )
                if len(childs) > 0:
                    getChildrenforNode(newnode, childs)

        ######

        # root node for document; never visible,
        # always outline type (even for tables)
        root = OutlineNode("__ROOT__", "", None, typeOutline)
        
        # get opml head section
        if rootOPML['head']:
            
            # the outline head node
            head = OutlineNode("head", "", root, typeOutline)
            root.addChild_( head )
            for headnode in rootOPML['head']:
                k, v = headnode
                #v = {'value': v}
                
                node = OutlineNode(k, v, head, typeOutline)
                #print "HEAD:", node.name
                head.addChild_( node )

        # fill in missing opml attributes here
        # created, modified
        #
        # how to propagate expansionstate, windowState?
        # make a document object and pass that to docdelegate?
        #
        # get opml body section
        if rootOPML['body']:

            # the outline body node
            body = OutlineNode("body", "", root, typeOutline)
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

                node = OutlineNode(name, content, body, typeOutline)
                # node.setValue_(content)
                body.addChild_( node )
                if len(children) > 0:
                    try:
                        getChildrenforNode( node, children )
                    except Exception, err:
                        print err
                        # pdb.set_trace()
                        pp(children)
                        pp(item)
        #title = os
        return root


    def openRSS_(self, url):
        if kwlog:
            s = url
            if len(url) > 31:
                s = url[:32]
            print "CactusOutlineDocument.openRSS_( %s )" % repr(s)
        d = feedparser.parse( url )

        # make basic nodes
        root = OutlineNode("__ROOT__", "", None, typeOutline)

        head = OutlineNode("head", "", root, typeOutline)
        root.addChild_( head )

        body = OutlineNode("body", "", root, typeOutline)
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
                        # pdb.set_trace()
                        l = []
                        for key, val in v.items():
                            l.append( (key,val) )
                        v = l
                    elif type(v) == time.struct_time:
                        v = time.asctime(v)
                    else:
                        # pdb.set_trace()
                        # if k in ('',)
                        if 1:
                            print "ATTENTION RSS Head values"
                            print "KEY:", k
                            print "TYPE:", type(v)
                            print "REPR:", repr(v)
                            print
                        v = repr(v)
                node = OutlineNode(k, v, head, typeOutline)
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
            node = OutlineNode(k, v, head, typeOutline)
            head.addChild_( node )
            
        if 0:
            # encoding
            if 'encoding' in d:
                node = OutlineNode('encoding', d.encoding, head, typeOutline)
                head.addChild_( node )
    
            # bozo
            if 'bozo' in d:
                node = OutlineNode('bozo', str(d.bozo), head, typeOutline)
                head.addChild_( node )
    
            # etag
            if 'etag' in d:
                node = OutlineNode('etag', d.etag, head, typeOutline)
                head.addChild_( node )
    
            # headers dict
            if 'headers' in d:
                node = OutlineNode('headers', d.headers, head, typeOutline)
                head.addChild_( node )
    
            # href
            if 'href' in d:
                node = OutlineNode('href', d.href, head, typeOutline)
                head.addChild_( node )
            
            # namespaces
            if 'namespaces' in d:
                # pdb.set_trace()
                node = OutlineNode('namespaces', d.namespaces, head, typeOutline)
                head.addChild_( node )
            
            # version
            if 'version' in d:
                node = OutlineNode('version', d.version, head, typeOutline)
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

            node = OutlineNode(name, value, body, typeOutline)
            body.addChild_( node )
        return root


class CactusOutlineWindowController(AutoBaseClass):

    # the actual base class is NSWindowController
    # outlineView

    def initWithObject_(self, document):
        """This controller is used for outline and table windows."""
        if kwlog:
            print "CactusOutlineWindowController.initWithObject_()"

        self = self.initWithWindowNibName_("OutlineEditor")
        title = u"Unnamed Outline"

        # pdb.set_trace()

        self.path = ""
        self.rootNode = None
        self.parentNode = None
        self.variableRowHeight = True

        if isinstance(document, CactusOutlineDocument):
            if isinstance(document.url, NSURL):
                self.path = str(document.url.absoluteString())
            else:
                self.path = document.url
            self.rootNode = document.rootNode
            self.parentNode = document.parentNode
            title = document.title

        # get window name from url or path
        if self.path:
            if os.path.exists(self.path):
                fld, fle = os.path.split(self.path)
                title = fle
            else:
                title = self.path
        else:
            # keep unnamed title
            pass

        self.window().setTitle_( title )

        theType = typeOutline
        self.model = OutlineViewDelegateDatasource.alloc().initWithObject_type_parentNode_(
                                                self.rootNode, theType, self.parentNode )

        # this is evil
        self.rootNode.model = self.model

        self.model.setController_( self )
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
        dataCell = self.nameColumn.dataCell()
        dataCell.setWraps_( True )

        # defaults to name & value visible, type & comment invisible
        typeVisible = self.optTypeVisible.setState_( False )
        commentVisible = self.optCommentVisible.setState_( False )
        self.applySettings_(None)

        # self.showWindow_(self)

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

        # pdb.set_trace()

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
