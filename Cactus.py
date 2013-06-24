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
kwdbg = False
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

NSOutlineView = AppKit.NSOutlineView
NSWindowController = AppKit.NSWindowController

NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString

# grid styles
NSTableViewGridNone = AppKit.NSTableViewGridNone
NSTableViewSolidVerticalGridLineMask = AppKit.NSTableViewSolidVerticalGridLineMask
NSTableViewSolidHorizontalGridLineMask = AppKit.NSTableViewSolidHorizontalGridLineMask


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

import CactusVersion
cachefolder = CactusVersion.cachefolder

import opml

import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException


import CactusOpenURLController
OpenURLWindowController = CactusOpenURLController.OpenURLWindowController

import CactusPreferenceController
CactusPreferenceController = CactusPreferenceController.CactusPreferenceController

import CactusAppDelegate
CactusAppDelegate = CactusAppDelegate.CactusAppDelegate
CactusDocumentController = CactusAppDelegate.CactusDocumentController



class Document(object):
    # this should be replaced by NSDocument.
    def __init__(self, fileorurl, rootNode, parentNode=None):
        self.fileorurl = fileorurl
        if not rootNode:
            self.root = OutlineNode("__ROOT__", "", None, typeOutline)
        else:
            self.root = rootNode
        self.parentNode = parentNode


class CactusWindowController(NSWindowController):
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

    def reloadData_(self, item):
            self.outlineView.reloadItem_reloadChildren_( item, True )

    def reloadData_Children_(self, item, children):
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


class CactusOpenAsAccessoryController(NSObject):
    """Just a holder for some values and an action for a open panel accessory."""

    menuOpenAs = objc.IBOutlet()
    def __new__(cls):
        return cls.alloc()

    def init(self):
        panel = NSBundle.loadNibNamed_owner_( u"OpenAsAccessoryView", self)
        return self

    @objc.IBAction
    def menuOpenAsType_( self, sender ):
        return self.menuOpenAs.title()

