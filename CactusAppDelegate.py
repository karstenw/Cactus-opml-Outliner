
# -*- coding: utf-8 -*-

"""
"""

import pdb
import pprint
pp = pprint.pprint
kwdbg = False
kwlog = True



import objc

import Foundation
NSObject = Foundation.NSObject
NSMutableDictionary = Foundation.NSMutableDictionary
NSUserDefaults = Foundation.NSUserDefaults
NSURL = Foundation.NSURL


import AppKit
NSApplication = AppKit.NSApplication
NSWindowController = AppKit.NSWindowController
NSDocumentController = AppKit.NSDocumentController
NSWorkspace = AppKit.NSWorkspace

import CactusVersion
cachefolder = CactusVersion.cachefolder

import CactusPreferenceController
CactusPreferenceController = CactusPreferenceController.CactusPreferenceController

import CactusAccessoryController
CactusOpenAsAccessoryController = CactusAccessoryController.CactusOpenAsAccessoryController


import CactusTools
NSURL2str = CactusTools.NSURL2str


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

    def makeDocumentWithContentsOfURL_ofType_error_(self, url, theType, err):
        if kwlog:
            print "CactusDocumentController.makeDocumentWithContentsOfURL_ofType_error_()"
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
            print "CactusAppDelegate.initialize()"
        self.visitedURLs = []
        self.documentcontroller = None
        # default settings for preferences
        userdefaults = NSMutableDictionary.dictionary()

        userdefaults.setObject_forKey_([],          u'lastURLsVisited')
        userdefaults.setObject_forKey_(False,       u'optCache')
        userdefaults.setObject_forKey_(cachefolder, u'txtCacheFolder')
        userdefaults.setObject_forKey_("2",         u'txtNoOfMaxRowLines')
        userdefaults.setObject_forKey_("40",        u'txtNoOfRecentURLs')
        userdefaults.setObject_forKey_("",          u'txtUserEmail')
        userdefaults.setObject_forKey_("",          u'txtUserName')

        userdefaults.setObject_forKey_(True,        u'optAlternateLines')
        userdefaults.setObject_forKey_(True,        u'optHLines')
        userdefaults.setObject_forKey_(True,        u'optVLines')
        userdefaults.setObject_forKey_(True,        u'optVariableRowHeight')

        userdefaults.setObject_forKey_(False,       u'optCommentColumn')
        userdefaults.setObject_forKey_(False,       u'optTypeColumn')
        userdefaults.setObject_forKey_(True,        u'optValueColumn')

        userdefaults.setObject_forKey_("<!DOCTYPE html>",   u'menDoctype')
        userdefaults.setObject_forKey_("utf-8",     u'menEncoding')
        userdefaults.setObject_forKey_("2",         u'txtIndent')

        userdefaults.setObject_forKey_(False,        u'optIMLAutodetect')
        userdefaults.setObject_forKey_(False,        u'optOPMLAutodetect')
        userdefaults.setObject_forKey_(False,        u'optRSSAutodetect')
        userdefaults.setObject_forKey_(False,        u'optHTMLAutodetect')
        userdefaults.setObject_forKey_(False,        u'optPLISTAutodetect')

        userdefaults.setObject_forKey_(False,        u'optIMLImportSystemLibraries')

        NSUserDefaults.standardUserDefaults().registerDefaults_(userdefaults)
        self.preferenceController = None


    def awakeFromNib(self):
        defaults = NSUserDefaults.standardUserDefaults()
        self.visitedURLs = defaults.arrayForKey_( u"lastURLsVisited" )

    def applicationDidFinishLaunching_(self, notification):
        if kwlog:
            print "CactusAppDelegate.applicationDidFinishLaunching_()"
        self.documentcontroller = CactusDocumentController.alloc().init()
        app = NSApplication.sharedApplication()
        app.activateIgnoringOtherApps_(True)

    @objc.IBAction
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

    """
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
    """

    # menu "New Table"
    @objc.IBAction
    def newTable_(self, sender):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.newTable_()"
        doc = Document("Untitled Table", None)
        CactusWindowController.alloc().initWithObject_type_(doc, typeTable)

    ####

    # menu "New Outline"
    @objc.IBAction
    def newOutline_(self, sender):
        if kwlog:
            print "DEPRECATED CactusAppDelegate.newOutline_()"

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
            print "CactusAppDelegate.newBrowser_()"
        # The CactusWindowController instance will retain itself,
        # so we don't (have to) keep track of all instances here.
        doc = Document("Untitled Outline", None)
        CactusWindowController.alloc().initWithObject_type_(doc, typeOutline)

    @objc.IBAction
    def openOutlineDocument_(self, sender):
        if kwlog:
            print "CactusAppDelegate.openOutlineDocument_()"
        docctrl = NSDocumentController.sharedDocumentController()
        docctrl.openDocument_(sender)

    @objc.IBAction
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
                body.addChild_( node )
                if len(children) > 0:
                    try:
                        getChildrenforNode( node, children )
                    except Exception, err:
                        print err
                        # pdb.set_trace()
                        pp(children)
                        pp(item)
        return root

    @objc.IBAction
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

    @objc.IBAction
    def outlineMenuExpand_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuExpand_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.expandSelection_(sender)

    @objc.IBAction
    def outlineMenuExpandAll_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuExpandAll_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.expandAllSelection_(sender)

    @objc.IBAction
    def outlineMenuCollapse_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuCollapse_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseSelection_(sender)

    @objc.IBAction
    def outlineMenuCollapseAll_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuCollapseAll_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseAllSelection_(sender)

    @objc.IBAction
    def outlineMenuCollapseToParent_(self, sender):
        if kwlog:
            print "CactusAppDelegate.outlineMenuCollapseToParent_()"
        ov = self.getCurrentOutlineView()
        if ov:
            ov.collapseToParent_(sender)

