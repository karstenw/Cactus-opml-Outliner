
# -*- coding: utf-8 -*-

from __future__ import print_function

"""
"""

import sys
import os


import pdb
import pprint
pp = pprint.pprint

import CactusVersion
kwdbg = CactusVersion.developmentversion
kwlog = CactusVersion.developmentversion

cachefolder = CactusVersion.cachefolder

import objc
super = objc.super

import Foundation
NSObject = Foundation.NSObject
NSMutableDictionary = Foundation.NSMutableDictionary
NSUserDefaults = Foundation.NSUserDefaults
NSURL = Foundation.NSURL
NSBundle = Foundation.NSBundle


import AppKit
NSApplication = AppKit.NSApplication
NSWindowController = AppKit.NSWindowController
NSDocument = AppKit.NSDocument
NSDocumentController = AppKit.NSDocumentController
NSWorkspace = AppKit.NSWorkspace

NSOutlineView = AppKit.NSOutlineView
NSWindowController = AppKit.NSWindowController

NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString

# grid styles
NSTableViewGridNone = AppKit.NSTableViewGridNone
NSTableViewSolidVerticalGridLineMask = AppKit.NSTableViewSolidVerticalGridLineMask
NSTableViewSolidHorizontalGridLineMask = AppKit.NSTableViewSolidHorizontalGridLineMask


import CactusOutlineTypes
typeOutline = CactusOutlineTypes.typeOutline
typeTable = CactusOutlineTypes.typeTable
typeBrowser = CactusOutlineTypes.typeBrowser


import CactusOutline
OutlineViewDelegateDatasource = CactusOutline.OutlineViewDelegateDatasource

import CactusOutlineDoc
CactusOutlineDocument = CactusOutlineDoc.CactusOutlineDocument

import CactusOutlineNode
OutlineNode = CactusOutlineNode.OutlineNode

import CactusOPML

import CactusPreferenceController
CactusPreferenceController = CactusPreferenceController.CactusPreferenceController


import CactusAccessoryController
CactusOpenAsAccessoryController = CactusAccessoryController.CactusOpenAsAccessoryController


import CactusTools
NSURL2str = CactusTools.NSURL2str


import CactusOpenURLController
OpenURLWindowController = CactusOpenURLController.OpenURLWindowController


import CactusMakeCalendarController
MakeCalendarController = CactusMakeCalendarController.MakeCalendarController




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

class Document(object):
    # this should be replaced by NSDocument.
    def __init__(self, fileorurl, rootNode, parentNode=None):
        self.fileorurl = fileorurl
        if not rootNode:
            self.root = OutlineNode("__ROOT__", "", None, typeOutline)
        else:
            self.root = rootNode
        self.parentNode = parentNode



# instantiated in NIB
class CactusDocumentController(NSDocumentController):
    def init(self):
        if kwlog:
            print( "CactusDocumentController.init()" )
        self = super( CactusDocumentController, self).init()
        self.selectedType = u"automatic"
        self.urllist = []
        return self

    def newDocument_(self, sender):
        return super( CactusDocumentController, self).newDocument_(sender)

    def runModalOpenPanel_forTypes_( self, panel, types ):
        if kwlog:
            print()
            print( "CactusDocumentController.runModalOpenPanel_forTypes_()", )
        self.selectedType = "automatic"
        extensionCtrl = CactusOpenAsAccessoryController.alloc().init()

        if extensionCtrl.menuOpenAs != None:
            panel.setAccessoryView_( extensionCtrl.menuOpenAs )
        result = super( CactusDocumentController, self).runModalOpenPanel_forTypes_( panel, None)

        if result:
            self.selectedType = extensionCtrl.menuOpenAs.title()
            self.urllist = set([NSURL2str(t) for t in panel.URLs()])
        if kwlog:
            pp(result) 
            print()
        return result

    def makeDocumentWithContentsOfURL_ofType_error_(self, url, theType, err):
        if kwlog:
            print( "CactusDocumentController.makeDocumentWithContentsOfURL_ofType_error_()" )

        if self.selectedType != "automatic" and len(self.urllist) > 0:
            u = NSURL2str( url )
            if u in self.urllist:
                self.urllist.discard( u )
                theType = self.selectedType
        result, error = super( CactusDocumentController, self).makeDocumentWithContentsOfURL_ofType_error_( url, theType, err)
        # self.selectedType = "automatic"
        return (result, error)


class CactusAppDelegate(NSObject):
    # defined in mainmenu

    def initialize(self):
        if kwlog:
            print( "CactusAppDelegate.initialize()" )
        self.visitedURLs = []
        self.documentcontroller = None
        # default settings for preferences
        userdefaults = NSMutableDictionary.dictionary()

        # application tab
        userdefaults.setObject_forKey_([],          u'lastURLsVisited')
        userdefaults.setObject_forKey_(False,       u'optCache')
        userdefaults.setObject_forKey_(cachefolder, u'txtCacheFolder')
        userdefaults.setObject_forKey_("2",         u'txtNoOfMaxRowLines')
        userdefaults.setObject_forKey_("40",        u'txtNoOfRecentURLs')
        userdefaults.setObject_forKey_(False,       u'optNewDocumentOnStart')

        # outline tab
        userdefaults.setObject_forKey_(True,        u'optAlternateLines')
        userdefaults.setObject_forKey_(True,        u'optHLines')
        userdefaults.setObject_forKey_(True,        u'optVLines')
        userdefaults.setObject_forKey_(True,        u'optVariableRowHeight')
        userdefaults.setObject_forKey_(False,       u'optCommentColumn')
        userdefaults.setObject_forKey_(False,       u'optTypeColumn')
        userdefaults.setObject_forKey_(True,        u'optValueColumn')

        # opml tab
        userdefaults.setObject_forKey_("",          u'txtUserEmail')
        userdefaults.setObject_forKey_("",          u'txtUserName')
        userdefaults.setObject_forKey_(True,        u'optAnimateOPMLOpen')
        userdefaults.setObject_forKey_(False,       u'optMergeComment')
        userdefaults.setObject_forKey_(True,        u'optIgnoreDotFiles')

        # html tab
        userdefaults.setObject_forKey_("<!DOCTYPE html>",   u'menDoctype')
        userdefaults.setObject_forKey_("utf-8",     u'menEncoding')
        userdefaults.setObject_forKey_("2",         u'txtIndent')

        # xml tab
        userdefaults.setObject_forKey_(False,        u'optIMLAutodetect')
        userdefaults.setObject_forKey_(False,        u'optOPMLAutodetect')
        userdefaults.setObject_forKey_(False,        u'optRSSAutodetect')
        userdefaults.setObject_forKey_(False,        u'optHTMLAutodetect')
        userdefaults.setObject_forKey_(False,        u'optPLISTAutodetect')

        # rss tab
        userdefaults.setObject_forKey_(False,        u'optRSSOpenEnclosure')

        # itunes tab
        userdefaults.setObject_forKey_(False,        u'optIMLImportSystemLibraries')

        NSUserDefaults.standardUserDefaults().registerDefaults_(userdefaults)
        self.preferenceController = None


    def awakeFromNib(self):
        defaults = NSUserDefaults.standardUserDefaults()
        self.visitedURLs = defaults.arrayForKey_( u"lastURLsVisited" )

    def applicationDidFinishLaunching_(self, notification):
        if kwlog:
            print( "CactusAppDelegate.applicationDidFinishLaunching_()" )
        self.documentcontroller = CactusDocumentController.alloc().init()
        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)

    @objc.IBAction
    def applicationShouldOpenUntitledFile_( self, sender ):
        if kwlog:
            print( "CactusAppDelegate.applicationShouldOpenUntitledFile_()" )
        defaults = NSUserDefaults.standardUserDefaults()
        return defaults.objectForKey_( u"optNewDocumentOnStart" )

    def applicationShouldHandleReopen_hasVisibleWindows_( self, theApplication, flag ):
        if kwlog:
            print( "CactusAppDelegate.applicationShouldHandleReopen_hasVisibleWindows_()" )
        # this is needed to prevent creating an untitled document when clicking the dock
        #
        # should really be in the (not yet existent) preferences
        return False

    def applicationShouldTerminate_(self, aNotification):
        """Store preferences before quitting
        """

        defaults = NSUserDefaults.standardUserDefaults()
        defaults.setObject_forKey_(self.visitedURLs,
                                   u'lastURLsVisited')
        return True

    ####

    @objc.IBAction
    def showPreferencePanel_(self, sender):
        if self.preferenceController == None:
            self.preferenceController = CactusPreferenceController.alloc().init()
        self.preferenceController.showWindow_( self.preferenceController )

    ####

    """ """
    def newTableWithRoot_(self, root):
        if kwlog:
            print( "CactusAppDelegate.newTableWithRoot_()" )
        self.newTableWithRoot_title_(root, None)

    def newTableWithRoot_title_(self, root, title):
        if kwlog:
            print( "DEPRECATED CactusAppDelegate.newTableWithRoot_title_()" )
        # find owning controller here and pass on
        if not title:
            title = u"Table Editor"
        doc = Document(title, root)
        CactusWindowController_OLD.alloc().initWithObject_type_(doc, typeTable)

    def newTableWithRoot_fromNode_(self, root, parentNode):
        if kwlog:
            print( "DEPRECATED CactusAppDelegate.newTableWithRoot_fromNode_()" )
        title = "Unnamed"
        if parentNode:
            title = parentNode.name
        doc = Document(title, root, parentNode)
        CactusWindowController_OLD.alloc().initWithObject_type_(doc, typeTable)

    """ """

    # menu "New Table"
    @objc.IBAction
    def newTable_(self, sender):
        if kwlog:
            print( "DEPRECATED CactusAppDelegate.newTable_()" )
        doc = Document("Untitled Table", None)
        CactusWindowController_OLD.alloc().initWithObject_type_(doc, typeTable)

    ####

    # menu "New Outline"
    @objc.IBAction
    def newOutline_(self, sender):
        if kwlog:
            print( "DEPRECATED CactusAppDelegate.newOutline_()" )

    # UNUSED
    @objc.IBAction
    def newRoot_(self, sender):
        pass

    # menu "Open URL"
    @objc.IBAction
    def openURL_(self, sender):
        """Open new "URL opener". Currently no measures against opening multiple of those...
        """
        OpenURLWindowController().init()

    ####

    @objc.IBAction
    def handleNodeMenu_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.handleNodeMenu_(%s)" % repr(sender) )
        app = NSApplication.sharedApplication()
        win = app.keyWindow()
        if win:
            print( "Save As...", win.title() )
            windelg = win.delegate()
            if windelg:
                ov = windelg.outlineView
                name = sender.title()
                print( name )
                if name == u"Move up":
                    ov.moveSelectionUp()
                elif name == u"Move down":
                    ov.moveSelectionDown()
                elif name == u"Move left":
                    ov.outdentSelection()
                elif name == u"Move right":
                    ov.indentSelection()

                elif name == u"Include":
                    pass
                elif name == u"Open in Browser":
                    pass
                elif name == u"Open in QT-Player":
                    pass
                elif name == u"Open linked opml":
                    pass


    @objc.IBAction
    def openMailingList_(self, sender):
        workspace= NSWorkspace.sharedWorkspace()
        url = NSURL.URLWithString_( u"http://groups.google.com/group/cactus-outliner-dev" )
        workspace.openURL_( url )

    @objc.IBAction
    def openGithubPage_(self, sender):
        workspace= NSWorkspace.sharedWorkspace()
        url = NSURL.URLWithString_( u"https://github.com/karstenw/Cactus-opml-Outliner" )
        workspace.openURL_( url )

    @objc.IBAction
    def openDownloadsPage_(self, sender):
        workspace= NSWorkspace.sharedWorkspace()
        url = NSURL.URLWithString_( u"http://goo.gl/EALQi" )
        workspace.openURL_( url )

    ####


    def newOutlineFromURL_Type_(self, url, type_):
        if kwlog:
            print( "CactusAppDelegate.newOutlineFromURL_Type_(\n\t%s\m\t%s )" %
                                                    repr(url), repr(type_))

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
                                                                       type_,
                                                                       None)

    # UNUSED but defined in class
    @objc.IBAction
    def newBrowser_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.newBrowser_()" )
        # The CactusWindowController_OLD instance will retain itself,
        # so we don't (have to) keep track of all instances here.
        doc = Document("Untitled Outline", None)
        CactusWindowController_OLD.alloc().initWithObject_type_(doc, typeOutline)

    @objc.IBAction
    def openOutlineDocument_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.openOutlineDocument_()" )
        docctrl = NSDocumentController.sharedDocumentController()
        docctrl.openDocument_(sender)

    @objc.IBAction
    def openFile_(self, sender):
        if kwlog:
            print( "DEPRECATED CactusAppDelegate.openFile_()" )
        # this is ugly
        f = getFileDialog(multiple=True)
        if f:
            for opmlFile in f:
                print( "Reading OPML '%s'" % (opmlFile.encode("utf-8"),) )
                fob = open(opmlFile, 'r')
                folder, filename = os.path.split(opmlFile)
                s = fob.read()
                fob.close()
                d = CactusOPML.opml_from_string(s)
                if d:
                    root = CactusOutlineDoc.openOPML_( d )
                    doc = Document(opmlFile, root)
                    CactusWindowController_OLD.alloc().initWithObject_type_(doc, typeOutline)

                    print( "Reading OPML '%s' Done." % (opmlFile.encode("utf-8"),) )
                else:
                    print( "Reading OPML '%s' FAILED." % (opmlFile.encode("utf-8"),) )

    def openOPML_(self, rootOPML):
        if kwlog:
            print( "CactusAppDelegate.openOPML_()" )
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
                del newnode

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
                #print( "HEAD:", node.name )
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
                body.addChild_( node )
                if len(children) > 0:
                    try:
                        getChildrenforNode( node, children )
                    except Exception as err:
                        print( err )
                        pp(children)
                        pp(item)
        return root

    @objc.IBAction
    def saveAs_(self, sender):
        if kwlog:
            print( "DEPRECATED CactusAppDelegate.saveAs_()" )
        print( "Save As..." )
        app = NSApplication.sharedApplication()
        win = app.keyWindow()
        if win:
            print( "Save As...", win.title() )
            windelg = win.delegate()
            if windelg:
                path = windelg.path
                model = windelg.model
                root = model.root

                f = saveAsDialog( path )
                if f:
                    rootOPML = opml.generateOPML( root, indent=1, expansion={} )
                    e = etree.ElementTree( rootOPML )
                    fob = open(f, 'w')
                    e.write(fob, encoding="utf-8", xml_declaration=True, method="xml" )
                    fob.close()

    def getCurrentAppWindow(self):
        if kwlog:
            print( "CactusAppDelegate.getCurrentAppWindow()" )
        return NSApplication.sharedApplication().keyWindow()

    def getCurrentDocument(self):
        if kwlog:
            print( "CactusAppDelegate.getCurrentDocument()" )
        return NSDocumentController.sharedDocumentController().currentDocument()

    def getCurrentOutlineView(self):
        if kwlog:
            print( "CactusAppDelegate.getCurrentOutlineView()" )
        doc = self.getCurrentDocument()
        if isinstance(doc, CactusOutlineDocument):
            win = self.getCurrentAppWindow()
            ctrl = win.windowController()
            return ctrl.outlineView
        return False

    @objc.IBAction
    def outlineMenuExpand_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.outlineMenuExpand_()" )
        ov = self.getCurrentOutlineView()
        if ov:
            ov.expandSelection_(sender)

    @objc.IBAction
    def outlineMenuExpandAll_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.outlineMenuExpandAll_()" )
        ov = self.getCurrentOutlineView()
        if ov:
            ov.expandAllSelection_(sender)

    @objc.IBAction
    def outlineMenuCollapse_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.outlineMenuCollapse_()" )
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseSelection_(sender)

    @objc.IBAction
    def outlineMenuCollapseAll_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.outlineMenuCollapseAll_()" )
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseAllSelection_(sender)

    @objc.IBAction
    def outlineMenuCollapseToParent_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.outlineMenuCollapseToParent_()" )
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseToParent_(sender)

    @objc.IBAction
    def makeCalendar_(self, sender):
        if kwlog:
            print( "CactusAppDelegate.makeCalendar_()" )
        MakeCalendarController().init()

    def appendNode_CurrentDoc_(self, node, doc):
        pass

    def makeCalendarCurrentOrNewDoc_(self, params):
        if kwlog:
            print( "CactusAppDelegate.makeCalendarCurrentOrNewDoc_()" )
        doc = self.getCurrentDocument()

        if not doc:
            app = NSApplication.sharedApplication()
            delg = app.delegate()
            docctrl = delg.documentcontroller
            docctrl.newDocument_(None)

        doc = self.getCurrentDocument()

        if not doc:
            return

        if not isinstance(doc, CactusOutlineDocument):
            return

        win = self.getCurrentAppWindow()
        ctrl = win.windowController()
        ov = ctrl.outlineView
        
        # find the root for the calendar
        # either the current selected node or append after last body child
        rootNode = ov.getSelectedRow()
        if rootNode == -1:
            r = ctrl.rootNode
            children = r.children
            head = body = False
            for child in children:
                if child.name == u"body":
                    rootNode = body = child
                    break
            if not body:
                rootNode = OutlineNode("body", "", r, typeOutline)
                r.addChild_( rootNode )

        # 
        cal, conf = params

        separateMonth = conf["separateMonth"]
        separateWeek = conf["separateWeek"]
        separateYear = conf["separateYear"]
        weekMonday = conf["weekMonday"]
        weekNumber = conf["weekNumber"]

        includeDays = conf["includeDays"]
        calDayFormat = conf["calDayFormat"]
        calHourFormat = conf["calHourFormat"]
        calMonthFormat = conf["calMonthFormat"]
        calTitle = conf["calTitle"]
        calWeekFormat = conf["calWeekFormat"]
        calYearFormat = conf["calYearFormat"]
        includeHours = conf["includeHours"]

        theRoot = rootNode.rootNode
        calRoot = OutlineNode(calTitle, "", rootNode, typeOutline, theRoot)
        
        rootNode.addChild_( calRoot )
        
        years = list( cal.keys() )
        
        try:
            years.remove('year')
        except  Exception:
             pass
        
        years.sort()
        
        for yearNumber in years:
            monthd = cal[yearNumber]['months']
            yearDT = cal[yearNumber]['dt']
            yearString = yearDT.strftime(calYearFormat)

            yearNode = OutlineNode(yearString, "", calRoot, typeOutline, theRoot)
            calRoot.addChild_( yearNode )

            months = list( monthd.keys() )
            months.sort()

            for monthNumber in months:
                daysd = monthd[monthNumber]['days']
                monthDT = monthd[monthNumber]['dt']
                monthString = monthDT.strftime(calMonthFormat)

                monthNode = OutlineNode(monthString, "", yearNode, typeOutline, theRoot)
                yearNode.addChild_( monthNode )

                days = list( daysd.keys() )
                days.sort()
                
                currWeeks = set()
                currWeek = None

                for day in days:
                    dayItemss = daysd[day]['day']
                    dayDT = daysd[day]['dt']
                    dayString = dayDT.strftime(calDayFormat)

                    isoYear, isoWeek, isoDay = dayDT.isocalendar()

                    parentNode = monthNode

                    if separateWeek:
                        if not isoWeek in currWeeks:
                            currWeeks.add( isoWeek)
                            weekString = dayDT.strftime(calWeekFormat)
                            currWeek = OutlineNode( weekString,
                                                    # "Week: " + str(isoWeek),
                                                    "",
                                                    parentNode,
                                                    typeOutline,
                                                    theRoot)
                            parentNode.addChild_( currWeek )
                        parentNode = currWeek

                    dayNode = OutlineNode( dayString,
                                           "",
                                           parentNode,
                                           typeOutline,
                                           theRoot)
                    parentNode.addChild_( dayNode )

                    dayItems = list(dayItemss)
                    dayItems.sort()
                    
                    if includeHours:
                        for dayItemDT in dayItems:
                            dayItemName = dayItemDT.strftime(calHourFormat)

                            itemNode = OutlineNode( dayItemName,
                                                    "",
                                                    dayNode,
                                                    typeOutline,
                                                    theRoot)
                            dayNode.addChild_( itemNode )
        ov.expandItem_( rootNode )
        ov.expandItem_( calRoot )
        ov.reloadData()

class CactusWindowController_OLD(NSWindowController):
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

    
    #
    # Can this be made for dual-use? outlines and tables?

    # the actual base class is NSWindowController
    # outlineView

    def init(self):
        # outline or table here
        # tables are outlines with no children
        if kwlog:
            print( "DEPRECATED CactusWindowController_OLD.init()" )
        doc = Document("Untitled", None)
        return self.initWithObject_type_(doc, typeOutline)

    def initWithObject_type_(self, obj, theType):
        """This controller is used for outline and table windows."""

        if kwlog:
            print( "DEPRECATED CactusWindowController_OLD.initWithObject_type_()" )

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

        self.path = objc.ivar()
        self.root = objc.ivar()
        self.parentNode = objc.ivar()
        self.variableRowHeight = objc.ivar()

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
            print( "DEPRECATED CactusWindowController_OLD.windowWillClose_()" )
        # see comment in self.initWithObject_type_()
        #
        # check model.dirty
        #
        self.autorelease()

    def doubleClick_(self, sender):
        # Open a new browser window for each selected expandable item
        print( "DEPRECATED doubleClick_()" )

    @objc.IBAction
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
