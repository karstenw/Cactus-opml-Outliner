
# -*- coding: utf-8 -*-


"""
"""

import sys
import os

import pdb
kwdbg = True
kwlog = True

import time
import datetime

import urllib

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import pprint
pp = pprint.pprint

import feedparser

import objc

import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL
NSMutableDictionary = Foundation.NSMutableDictionary

NSUserDefaults = Foundation.NSUserDefaults


import AppKit
NSOpenPanel = AppKit.NSOpenPanel
NSApplication = AppKit.NSApplication
NSDocument = AppKit.NSDocument
NSDocumentController = AppKit.NSDocumentController
NSWorkspace = AppKit.NSWorkspace

NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString

NSSavePanel = AppKit.NSSavePanel
NSFileHandlingPanelOKButton  = AppKit.NSFileHandlingPanelOKButton


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


import opml

extractClasses("MainMenu")
extractClasses("OpenURL")
extractClasses("OutlineEditor")



#
# Open File
#
def getFileDialog(multiple=False):
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(multiple)
    rval = panel.runModalForTypes_( None )
    if rval:
        return [t for t in panel.filenames()]
    return []


#
# File save dialog
#
def saveAsDialog(path):
    panel = NSSavePanel.savePanel()

    if path:
        panel.setDirectory_( path )

    panel.setMessage_( u"Save as OPML" )
    panel.setExtensionHidden_( False )
    panel.setCanSelectHiddenExtension_(True)
    panel.setRequiredFileType_( u"opml" )
    if path:
        if not os.path.isdir( path ):
            folder, fle = os.path.split(path)
        else:
            folder = path
            fle = "Untitled.opml"
        rval = panel.runModalForDirectory_file_(folder, fle)
    else:
        rval = panel.runModal()

    if rval == NSFileHandlingPanelOKButton:
        return panel.filename()
    return False


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
        # pdb.set_trace()
        self = self.initWithWindowNibName_("OpenURL")
        window = self.window()
        window.setTitle_( u"Open URL…" )
        # self.label.setStringValue_(u"URL:")
        window.makeFirstResponder_(self.textfield)
        app = NSApplication.sharedApplication()
        delg = app.delegate()
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

    def clearMenu_(self, sender):
        self.visitedURLs = []
        app = NSApplication.sharedApplication()
        delg = app.delegate()
        delg.visitedURLs = self.visitedURLs
        self.menuLastVisited.removeAllItems()

    def lastVisitedMenuSelection_(self, sender):
        urlSelected = self.menuLastVisited.title()
        self.textfield.setStringValue_( urlSelected )


    def windowWillClose_(self, notification):
        #pdb.set_trace()
        # see comment in self.initWithObject_()
        self.autorelease()


    def OK_(self, sender):
        "User pressed OK button. Get data and try to open that stuff."

        app = NSApplication.sharedApplication()
        delg = app.delegate()
        t_url = self.textfield.stringValue()
        url = NSURL.URLWithString_( t_url )
        if t_url not in self.visitedURLs:
            self.visitedURLs.append( t_url )
            n = len(self.visitedURLs)
            if n > 30:
                start = n - 30
                self.visitedURLs = self.visitedURLs[start:]
            delg.visitedURLs = self.visitedURLs[:]

        delg.newOutlineFromOPMLURL_( url )
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

    #
    # Can this be made for dual-use? outlines and tables?
    
    # the actual base class is NSWindowController
    # outlineView


    def init(self):
        # outline or table here
        # tables are outlines with no children
        if kwlog:
            print "CactusWindowController.init()"
        doc = Document("Untitled", None)
        return self.initWithObject_type_(doc, typeOutline)


    def initWithObject_type_(self, obj, theType):
        """This controller is used for outline and table windows."""

        if kwlog:
            print "CactusWindowController.initWithObject_type_()"

        if theType == typeOutline:
            self = self.initWithWindowNibName_("OutlineEditor")
            title = u"Unnamed Outline"
        elif theType == typeTable:
            # pdb.set_trace()
            self = self.initWithWindowNibName_("TableEditor")
            title = u"Unnamed Table"
        elif theType == typeBrowser:
            pass #title = u"Browser"
        else:
            pass

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
        dataCell = self.nameColumn.dataCell()
        dataCell.setWraps_( True )

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
            print "CactusWindowController.windowWillClose_()"
        # see comment in self.initWithObject_()
        #
        # check model.dirty
        #
        self.autorelease()


    def doubleClick_(self, sender):
        # Open a new browser window for each selected expandable item
        print "doubleClick_()"

    def reloadData_(self, item=None, children=False):
        if item == None:
            self.outlineView.reloadData() #reloadItem_reloadChildren_( item, True )
        else:
            self.outlineView.reloadItem_reloadChildren_( item, children )

    def loadFile_(self, sender):
        pass
            

    def applySettings_(self, sender):
        # pdb.set_trace()
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


class CactusAppDelegate(NSObject):
    # defined in mainmenu

    def initialize(self):
        if kwlog:
            print "CactusAppDelegate.initialize()"
        self.visitedURLs = []
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
        # pdb.set_trace()
        #doc = Document("Untitled Outline", None)
        #boilerplateOPML( doc.root )
        #CactusWindowController.alloc().initWithObject_type_(doc, typeOutline)
        # docc = NSDocumentController.sharedDocumentController()
        # docc.newDocument_(sender)


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


    def newOutlineFromRSSURL_(self, url):
        root = self.openRSS_( url )
        doc = Document(url, root)
        CactusWindowController.alloc().initWithObject_type_(doc, typeOutline)


    # used by OpenURL delegate OK_ action
    def newOutlineFromOPMLURL_(self, url):
        """
        """
        if not isinstance(url, NSURL):
            url = NSURL.URLWithString_( url )
        docc = NSDocumentController.sharedDocumentController()
        err = docc.makeDocumentWithContentsOfURL_ofType_error_(url,
                                                           'Cactus Outline')
            

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
            print "CactusAppDelegate.openFile_()"
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
                    root = self.openOPML_( d )
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


    def openRSS_(self, url):
        if kwlog:
            print "CactusAppDelegate.openRSS_()"
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
            keys = """cloud docs generator generator_detail image language link links
                      microblog_archive microblog_endday microblog_filename
                      microblog_startday microblog_url published subtitle
                      subtitle_detail sy_updatefrequency sy_updateperiod title
                      title_detail updated updated_parsed""".split()
            #for k in keys:
            #    if k in d.feed:

            feedkeys = d.feed.keys()
            feedkeys.sort()
            # pdb.set_trace()
            #print
            #pp(feedkeys)
            #print
            for k in feedkeys:

                # keys to ignore
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
                        if 0:
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

        # deactivated
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
            for k in killkeys:
                value.pop( k, None )
            node = OutlineNode(name, value, body, typeOutline)
            body.addChild_( node )
        return root


    def saveAs_(self, sender):
        if kwlog:
            print "CactusAppDelegate.saveAs_()"
        print "Save As..."
        app = NSApplication.sharedApplication()
        win = app.keyWindow()
        if win:
            print "Save As...", win.title()
            windelg = win.delegate()
            # pdb.set_trace()
            if windelg:
                path = windelg.path
                model = windelg.model
                root = model.root
    
                f = saveAsDialog( path )
                if f:
                    rootOPML = opml.generateOPML( root, indent=1 )
                    # pdb.set_trace()
                    e = etree.ElementTree( rootOPML )
                    fob = open(f, 'w')
                    e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
                    fob.close()


if __name__ == "XX__main__":
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()
