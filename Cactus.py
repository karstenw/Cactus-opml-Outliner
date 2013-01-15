
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

import pdb
import pprint
pp = pprint.pprint
kwdbg = True
kwlog = True

import feedparser

import objc

import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL
NSMutableDictionary = Foundation.NSMutableDictionary

NSUserDefaults = Foundation.NSUserDefaults

NSBundle = Foundation.NSBundle

import AppKit
NSApplication = AppKit.NSApplication
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

import CactusOutlineDoc
boilerplateOPML = CactusOutlineDoc.boilerplateOPML
CactusOutlineDocument = CactusOutlineDoc.CactusOutlineDocument

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType

import CactusTools
NSURL2str = CactusTools.NSURL2str

import opml

extractClasses("MainMenu")
extractClasses("OpenURL")
extractClasses("OutlineEditor")
extractClasses("OpenAsAccessoryView")


import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException


#
# Open URL Delegate
#
class OpenURLWindowController(AutoBaseClass):
    """Present a dialog for entering a URL for http document retrieval."""

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
        window.setTitle_( u"Open URL…" )
        # self.label.setStringValue_(u"URL:")
        window.makeFirstResponder_(self.textfield)
        app = NSApplication.sharedApplication()
        delg = app.delegate()
        self.readAsType = CactusOPMLType
        self.visitedURLs = delg.visitedURLs[:]
        self.menuLastVisited.removeAllItems()
        for url in self.visitedURLs:
            self.menuLastVisited.addItemWithTitle_( url )
        self.showWindow_(self)

        self.retain()
        return self

    def clearMenu_(self, sender):
        self.visitedURLs = []
        app = NSApplication.sharedApplication()
        delg = app.delegate()
        delg.visitedURLs = self.visitedURLs
        self.menuLastVisited.removeAllItems()

    def lastVisitedMenuSelection_(self, sender):
        urlSelected = self.menuLastVisited.title()
        self.textfield.setStringValue_( urlSelected )

    def openAsMenuSelection_(self, sender):
        self.readAsType = self.menuOpenAs.title()

    def windowWillClose_(self, notification):
        # see comment in self.initWithObject_()
        self.autorelease()


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
            if n > 40:
                self.visitedURLs = self.visitedURLs[:50]
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

    def Cancel_(self, sender):
        #pdb.set_trace()
        self.close()


class Document(object):
    # this should be replaced by NSDocument.
    def __init__(self, fileorurl, rootNode, parentNode=None):
        self.fileorurl = fileorurl
        if not rootNode:
            self.root = OutlineNode("__ROOT__", "", None, typeOutline)
        else:
            self.root = rootNode
        self.parentNode = parentNode


class CactusWindowController(AutoBaseClass):
    def init(self):
        if kwlog:
            print "XXXXXXXXXXXXXXXXXXXX               CactusWindowController.init()"
        self = self.initWithWindowNibName_("OpenAsAccessoryView")
        window = self.window()
        window.setTitle_( u"Open URL…" )
        # self.label.setStringValue_(u"URL:")
        window.makeFirstResponder_(self.textfield)
        app = NSApplication.sharedApplication()
        delg = app.delegate()
        self.readAsType = None
        self.visitedURLs = delg.visitedURLs[:]
        self.menuLastVisited.removeAllItems()
        for url in self.visitedURLs:
            self.menuLastVisited.addItemWithTitle_( url )
        self.showWindow_(self)

        # The window controller doesn't need to be retained (referenced)
        # anywhere, so we pretend to have a reference to ourselves to avoid
        # being garbage collected before the window is closed. The extra
        # reference will be released in self.windowWillClose_()
        self.retain()
        return self

    #
    # Can this be made for dual-use? outlines and tables?
    
    # the actual base class is NSWindowController
    # outlineView


    def init(self):
        # outline or table here
        # tables are outlines with no children
        if kwlog:
            print "DEPRECATED CactusWindowController.init()"
        doc = Document("Untitled", None)
        return self.initWithObject_type_(doc, typeOutline)


    def initWithObject_type_(self, obj, theType):
        """This controller is used for outline and table windows."""

        if kwlog:
            print "DEPRECATED CactusWindowController.initWithObject_type_()"

        if theType == typeOutline:
            self = self.initWithWindowNibName_("OutlineEditor")
            title = u"Unnamed Outline"

        elif theType == typeTable:
            self = self.initWithWindowNibName_("TableEditor")
            title = u"Unnamed Table"
        elif theType == typeBrowser:
            pass #title = u"Browser"
        else:
            pass

        self.rowLines = 2

        if not obj:
            obj = Document(title, None)

        self.path = ""
        self.root = None
        self.parentNode = None
        self.variableRowHeight = True

        if isinstance(obj, Document):
            self.path = obj.fileorurl
            self.root = obj.root
            self.parentNode = obj.parentNode

        # get window name from url or path
        if os.path.exists(self.path):
            fld, fle = os.path.split(self.path)
            title = fle
        elif self.path:
            title = self.path
        else:
            # keep unnamed title
            pass

        self.window().setTitle_( title )

        self.model = OutlineViewDelegateDatasource.alloc().initWithObject_type_parentNode_(
                                                self.root, theType, self.parentNode )

        # this is evil
        self.root.model = self.model

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
        self.nameColumn.dataCell().setWraps_( True )
        self.commentColumn.dataCell().setWraps_( True )
        self.valueColumn.dataCell().setWraps_( True )

        # defaults to name & value visible, type & comment invisible
        typeVisible = self.optTypeVisible.setState_( False )
        commentVisible = self.optCommentVisible.setState_( False )
        self.applySettings_(None)

        self.showWindow_(self)

        # The window controller doesn't need to be retained (referenced)
        # anywhere, so we pretend to have a reference to ourselves to avoid
        # being garbage collected before the window is closed. The extra
        # reference will be released in self.windowWillClose_()
        self.retain()
        return self

    def windowWillClose_(self, notification):
        if kwlog:
            print "DEPRECATED CactusWindowController.windowWillClose_()"
        # see comment in self.initWithObject_()
        #
        # check model.dirty
        #
        self.autorelease()

    def doubleClick_(self, sender):
        # Open a new browser window for each selected expandable item
        print "DEPRECATED doubleClick_()"

    def reloadData_(self, item=None, children=False):
        if item == None:
            self.outlineView.reloadData() #reloadItem_reloadChildren_( item, True )
        else:
            self.outlineView.reloadItem_reloadChildren_( item, children )

    def applySettings_(self, sender):
        """target of the apply button. sets some tableview settings.
        """
        # rowHeight
        self.variableRowHeight = self.optVariableRow.state()

        # menus - NOT YET USED
        # formatChoice = self.menFormat.state()
        # behaviourChoice = self.menBehaviour.state()

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


class CactusOpenAsAccessoryController(AutoBaseClass):
    """Just a holder for some values and an action for a open panel accessory."""

    def __new__(cls):
        return cls.alloc()

    def init(self):
        panel = NSBundle.loadNibNamed_owner_( u"OpenAsAccessoryView", self)
        return self

    def menuOpenAsType_( self, sender ):
        return self.menuOpenAs.title()


# instantiated in NIB
class CactusDocumentController(NSDocumentController):
    def init(self):
        if kwlog:
            print "CactusDocumentController.init()"
        self = super( CactusDocumentController, self).init()
        self.selectedType = u"automatic"
        self.urllist = []
        return self

    def runModalOpenPanel_forTypes_( self, panel, types ):
        if kwlog:
            print "CactusDocumentController.runModalOpenPanel_forTypes_()"
        self.selectedType = "automatic"
        extensionCtrl = CactusOpenAsAccessoryController.alloc().init()

        if extensionCtrl.menuOpenAs != None:
            panel.setAccessoryView_( extensionCtrl.menuOpenAs )
        result = super( CactusDocumentController, self).runModalOpenPanel_forTypes_( panel, None)

        if result:
            self.selectedType = extensionCtrl.menuOpenAs.title()
            self.urllist = set([NSURL2str(t) for t in panel.URLs()])
        return result

    def makeDocumentWithContentsOfURL_ofType_error_(self, url, theType):
        if kwlog:
            print "CactusDocumentController.makeDocumentWithContentsOfURL_ofType_error_()"
        if self.selectedType != "automatic" and len(self.urllist) > 0:
            u = NSURL2str( url )
            if u in self.urllist:
                self.urllist.discard( u )
                theType = self.selectedType
        result, error = super( CactusDocumentController, self).makeDocumentWithContentsOfURL_ofType_error_( url, theType)
        # self.selectedType = "automatic"
        return (result, error)
        

class CactusAppDelegate(NSObject):
    # defined in mainmenu

    def initialize(self):
        if kwlog:
            print "CactusAppDelegate.initialize()"
        self.visitedURLs = []
        self.documentcontroller = None
        # default settings for preferences
        userdefaults = NSMutableDictionary.dictionary()

        userdefaults.setObject_forKey_([],   u'lastURLsVisited')

        NSUserDefaults.standardUserDefaults().registerDefaults_(userdefaults)


    def awakeFromNib(self):
        defaults = NSUserDefaults.standardUserDefaults()
        self.visitedURLs = defaults.arrayForKey_( u"lastURLsVisited" )
        

    def applicationDidFinishLaunching_(self, notification):
        if kwlog:
            print "CactusAppDelegate.applicationDidFinishLaunching_()"

        self.documentcontroller = CactusDocumentController.alloc().init()

        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)


    def applicationShouldOpenUntitledFile_( self, sender ):
        if kwlog:
            print "CactusAppDelegate.applicationShouldOpenUntitledFile_()"
        # this is neede to prevent creating an untitled document at startup
        #
        # should really be in the (not yet existent) preferences
        return False


    def applicationShouldHandleReopen_hasVisibleWindows_( self, theApplication, flag ):
        if kwlog:
            print "CactusAppDelegate.applicationShouldHandleReopen_hasVisibleWindows_()"
        # this is neede to prevent creating an untitled document when clicking the dock
        #
        # should really be in the (not yet existent) preferences
        return False


    def applicationShouldTerminate_(self, aNotification):
        """Store preferences before quitting
        """

        defaults = NSUserDefaults.standardUserDefaults()

        defaults.setObject_forKey_(self.visitedURLs ,
                                   u'lastURLsVisited')
        return True


    def newTableWithRoot_(self, root):
        if kwlog:
            print "CactusAppDelegate.newTableWithRoot_()"
        self.newTableWithRoot_title_(root, None)


    def newTableWithRoot_title_(self, root, title):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.newTableWithRoot_title_()"
        # find owning controller here and pass on
        if not title:
            title = u"Table Editor"
        doc = Document(title, root)
        CactusWindowController.alloc().initWithObject_type_(doc, typeTable)

    def newTableWithRoot_fromNode_(self, root, parentNode):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.newTableWithRoot_fromNode_()"
        title = "Unnamed"
        if parentNode:
            title = parentNode.name
        doc = Document(title, root, parentNode)
        CactusWindowController.alloc().initWithObject_type_(doc, typeTable)

    # menu "New Table"
    def newTable_(self, sender):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.newTable_()"
        doc = Document("Untitled Table", None)
        CactusWindowController.alloc().initWithObject_type_(doc, typeTable)

    # menu "New Outline"
    def newOutline_(self, sender):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.newOutline_()"

    # UNUSED
    def newRoot_(self, sender):
        pass

    # menu "Open URL"
    def openURL_(self, sender):
        """Open new "URL opener". Currently no measures against opening multiple of those...
        """
        OpenURLWindowController().init()

    def openMailingList_(sender):
        workspace= NSWorkspace.sharedWorkspace()
        url = NSURL.URLWithString_( u"http://groups.google.com/group/cactus-outliner-dev" )
        workspace.openURL_( url )

    def openGithubPage_(sender):
        workspace= NSWorkspace.sharedWorkspace()
        url = NSURL.URLWithString_( u"https://github.com/karstenw/Cactus-opml-Outliner" )
        workspace.openURL_( url )

    def openDownloadsPage_(sender):
        workspace= NSWorkspace.sharedWorkspace()
        url = NSURL.URLWithString_( u"http://goo.gl/EALQi" )
        workspace.openURL_( url )
    
    def newOutlineFromURL_Type_(self, url, type_):
        if not isinstance(url, NSURL):
            url = NSURL.URLWithString_( url )
        # just check for local files
        docc = NSDocumentController.sharedDocumentController()
        localurl = url.isFileURL()
        loaded = True
        if localurl:
            loaded = docc.documentForURL_( url )
        if not loaded or not localurl:
            doc, err = docc.makeDocumentWithContentsOfURL_ofType_error_(url,
                                                                       type_)


    # UNUSED but defined in class
    def newBrowser_(self, sender):
        if kwlog:
            print "CactusAppDelegate.newBrowser_()"
        # The CactusWindowController instance will retain itself,
        # so we don't (have to) keep track of all instances here.
        doc = Document("Untitled Outline", None)
        CactusWindowController.alloc().initWithObject_type_(doc, typeOutline)

    def openOutlineDocument_(self, sender):
        if kwlog:
            print "CactusAppDelegate.openOutlineDocument_()"

        # docctrl = CactusDocumentController.sharedDocumentController()
        docctrl = NSDocumentController.sharedDocumentController()
        docctrl.openDocument_(sender)

    def openFile_(self, sender):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.openFile_()"
        # this is ugly
        f = getFileDialog(multiple=True)
        if f:
            for opmlFile in f:
                print "Reading OPML '%s'" % (opmlFile.encode("utf-8"),)
                fob = open(opmlFile, 'r')
                folder, filename = os.path.split(opmlFile)
                s = fob.read()
                fob.close()
                d = opml.opml_from_string(s)
                if d:
                    root = CactusOutlineDoc.openOPML_( d )
                    doc = Document(opmlFile, root)
                    CactusWindowController.alloc().initWithObject_type_(doc, typeOutline)

                    print "Reading OPML '%s' Done." % (opmlFile.encode("utf-8"),)
                else:
                    print "Reading OPML '%s' FAILED." % (opmlFile.encode("utf-8"),)

    def openOPML_(self, rootOPML):
        if kwlog:
            print "CactusAppDelegate.openOPML_()"
        """This builds the node tree and opens a window."""
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

    def saveAs_(self, sender):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.saveAs_()"
        print "Save As..."
        app = NSApplication.sharedApplication()
        win = app.keyWindow()
        if win:
            print "Save As...", win.title()
            windelg = win.delegate()
            if windelg:
                path = windelg.path
                model = windelg.model
                root = model.root
    
                f = saveAsDialog( path )
                if f:
                    rootOPML = opml.generateOPML( root, indent=1 )
                    e = etree.ElementTree( rootOPML )
                    fob = open(f, 'w')
                    e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
                    fob.close()

    def getCurrentAppWindow(self):
        if kwlog:
            print "CactusAppDelegate.getCurrentAppWindow()"
        return NSApplication.sharedApplication().keyWindow()

    def getCurrentDocument(self):
        if kwlog:
            print "CactusAppDelegate.getCurrentDocument()"
        return NSDocumentController.sharedDocumentController().currentDocument()

    def getCurrentOutlineView(self):
        if kwlog:
            print "CactusAppDelegate.getCurrentOutlineView()"
        doc = self.getCurrentDocument()
        if isinstance(doc, CactusOutlineDocument):
            win = self.getCurrentAppWindow()
            controllers = doc.windowControllers()
            for controller in controllers:
                if win == controller.window():
                    return controller.outlineView
        return False

    def outlineMenuExpand_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuExpand_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.expandSelection_(sender)

    def outlineMenuExpandAll_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuExpandAll_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.expandAllSelection_(sender)

    def outlineMenuCollapse_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuCollapse_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseSelection_(sender)

    def outlineMenuCollapseAll_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuCollapseAll_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseAllSelection_(sender)

    def outlineMenuCollapseToParent_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuCollapseToParent_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseToParent_(sender)
