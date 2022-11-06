
# -*- coding: utf-8 -*-

from __future__ import print_function


"""
"""

import sys
import os

import datetime
import urllib

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import pprint
pp = pprint.pprint

import pdb


import Foundation
NSObject = Foundation.NSObject
NSURL = Foundation.NSURL


import AppKit
NSDocument = AppKit.NSDocument
NSDocumentController = AppKit.NSDocumentController
NSWorkspace = AppKit.NSWorkspace

import PyObjCTools
#import PyObjCTools.NibClassBuilder
#extractClasses = PyObjCTools.NibClassBuilder.extractClasses
#AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass


import CactusOutline
OutlineViewDelegateDatasource = CactusOutline.OutlineViewDelegateDatasource

import CactusOutlineNode
OutlineNode = CactusOutlineNode.OutlineNode


'''
class TableWindowController(AutoBaseClass):

    #
    # Can this be made for dual-use? outlines and tables?
    
    # the actual base class is NSWindowController
    # outlineView


    def init(self):
        # outline or table here
        # tables are outlines with no children
        doc = Document("Untitled", None)
        return self.initWithObject_type_(doc, typeOutline)


    def initWithObject_type_(self, obj, theType):
        """This controller is used for outline and table windows."""

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
        # see comment in self.initWithObject_()
        #
        # check model.dirty
        #
        self.autorelease()


    def doubleClick_(self, sender):
        # Open a new browser window for each selected expandable item
        print( "doubleClick_()" )

    def reloadData_(self, item=None, children=False):
        if item == None:
            self.outlineView.reloadData() #reloadItem_reloadChildren_( item, True )
        else:
            self.outlineView.reloadItem_reloadChildren_( item, children )

    def loadFile_(self, sender):
        pass
            

    def applySettings_(self, sender):
        """target of the apply button. sets some tableview settings.
        """
        # rowHeight
        self.variableRowHeight = self.optVariableRow.state()

        # menus - NOT YET USED
        formatChoice = self.menFormat.state()
        behaviourChoice = self.menBehaviour.state()

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
'''
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

