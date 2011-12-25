
# -*- coding: utf-8 -*-



"""A collection of outline related stuff
"""

import sys
import os

import urllib
import urlparse

import pdb
import pprint
pp = pprint.pprint

kwdbg = False

# i prefer manual aliasing
import operator
getitem = operator.getitem
setitem = operator.setitem


import Foundation
NSObject = Foundation.NSObject
NSAutoreleasePool = Foundation.NSAutoreleasePool
NSMutableDictionary = Foundation.NSMutableDictionary
NSMakeRange = Foundation.NSMakeRange
NSAttributedString = Foundation.NSAttributedString
NSThread = Foundation.NSThread
NSNotificationCenter = Foundation.NSNotificationCenter
NSNotification = Foundation.NSNotification

NSMutableArray = Foundation.NSMutableArray

NSNotFound = Foundation.NSNotFound
NSIndexSet = Foundation.NSIndexSet
NSMutableIndexSet = Foundation.NSMutableIndexSet

NSNumber = Foundation.NSNumber

NSURL = Foundation.NSURL


import AppKit
NSUserDefaults = AppKit.NSUserDefaults
NSApplication = AppKit.NSApplication
NSOpenPanel = AppKit.NSOpenPanel
#NSAlert = AppKit.NSAlert
#NSPopUpButtonWillPopUpNotification = AppKit.NSPopUpButtonWillPopUpNotification
NSWorkspace = AppKit.NSWorkspace
#NSWorkspaceDidMountNotification = AppKit.NSWorkspaceDidMountNotification
#NSWorkspaceDidUnmountNotification = AppKit.NSWorkspaceDidUnmountNotification
#NSWorkspaceWillUnmountNotification = AppKit.NSWorkspaceWillUnmountNotification
#NSImage = AppKit.NSImage
#NSFont = AppKit.NSFont
#NSFontAttributeName = AppKit.NSFontAttributeName
#NSForegroundColorAttributeName = AppKit.NSForegroundColorAttributeName
#NSColor = AppKit.NSColor
NSString = AppKit.NSString
#NSMakePoint = AppKit.NSMakePoint
#NSBitmapImageRep = AppKit.NSBitmapImageRep
#NSPICTFileType = AppKit.NSPICTFileType
#NSTIFFFileType = AppKit.NSTIFFFileType
NSTableView = AppKit.NSTableView
NSText = AppKit.NSText

# the characters to test against
NSBackspaceCharacter = AppKit.NSBackspaceCharacter
NSDeleteCharacter = AppKit.NSDeleteCharacter
NSCarriageReturnCharacter = AppKit.NSCarriageReturnCharacter
NSEnterCharacter = AppKit.NSEnterCharacter
NSTabCharacter = AppKit.NSTabCharacter
NSBackTabCharacter = AppKit.NSBackTabCharacter

NSDownArrowFunctionKey = AppKit.NSDownArrowFunctionKey
NSLeftArrowFunctionKey = AppKit.NSLeftArrowFunctionKey
NSRightArrowFunctionKey = AppKit.NSRightArrowFunctionKey
NSUpArrowFunctionKey = AppKit.NSUpArrowFunctionKey
NSUpTextMovement = AppKit.NSUpTextMovement


# text movements
NSReturnTextMovement = AppKit.NSReturnTextMovement
NSTabTextMovement = AppKit.NSTabTextMovement
NSBacktabTextMovement = AppKit.NSBacktabTextMovement
NSIllegalTextMovement = AppKit.NSIllegalTextMovement
NSCancelTextMovement = AppKit.NSCancelTextMovement


# modifiers
# shift lock
NSAlphaShiftKeyMask = AppKit.NSAlphaShiftKeyMask

# shift key
NSShiftKeyMask = AppKit.NSShiftKeyMask

# control
NSControlKeyMask = AppKit.NSControlKeyMask

# alt
NSAlternateKeyMask = AppKit.NSAlternateKeyMask

# cmd
NSCommandKeyMask = AppKit.NSCommandKeyMask

# F
NSFunctionKeyMask = AppKit.NSFunctionKeyMask

NSDeviceIndependentModifierFlagsMask = AppKit.NSDeviceIndependentModifierFlagsMask


import PyObjCTools
import PyObjCTools.NibClassBuilder
extractClasses = PyObjCTools.NibClassBuilder.extractClasses
AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass


extractClasses("OutlineEditor")
extractClasses("TableEditor")
extractClasses("NodeEditor")




class KWOutlineView(AutoBaseClass):
    """Subclass of NSOutlineView; to catch keys."""

    def awakeFromNib(self):
        pass

    #
    # cell editor notifications
    #
    def textDidBeginEditing_(self, aNotification):
        """Notification."""
        userInfo = aNotification.userInfo()

        # textMovement = userInfo.valueForKey_( str("NSTextMovement") ).intValue()
        super( KWOutlineView, self).textDidBeginEditing_(aNotification)
        #self.window().makeFirstResponder_(self)


    def textDidChange_(self, aNotification):
        """Notification."""
        super( KWOutlineView, self).textDidChange_(aNotification)
        #self.window().makeFirstResponder_(self)
        

    def textDidEndEditing_(self, aNotification):
        """Notification."""

        if kwdbg:
            print "Edit END"
        userInfo = aNotification.userInfo()

        #pp(userInfo)

        #pdb.set_trace()
        #textMovement = userInfo.valueForKey_( str("NSTextMovement") ).intValue()

        cancelled = False

        # check for table/outline editing modes here
        if userInfo.valueForKey_( u"NSTextMovement" ).intValue() == NSReturnTextMovement:
            cancelled = True
            newInfo = NSMutableDictionary.dictionaryWithDictionary_(userInfo)
            newTextActionCode = NSNumber.numberWithInt_(NSCancelTextMovement)
            newInfo.setObject_forKey_( newTextActionCode, str("NSTextMovement"))
            aNotification = NSNotification.notificationWithName_object_userInfo_(aNotification.name(),
                                                                                aNotification.object(),
                                                                                newInfo)
        super( KWOutlineView, self).textDidEndEditing_(aNotification)
        if cancelled:
            self.window().makeFirstResponder_(self)


    #
    # event capture
    #
    def keyDown_(self, theEvent):
        """Catch events for the outline and tableviews. """

        eventCharacters = theEvent.characters()
        eventModifiers = int(theEvent.modifierFlags())
        eventCharNum = ord(eventCharacters)

        mykeys = (NSBackspaceCharacter, NSDeleteCharacter,
                  NSCarriageReturnCharacter, NSEnterCharacter,
                  NSTabCharacter, NSBackTabCharacter,
                  ord(NSUpArrowFunctionKey),
                  ord(NSDownArrowFunctionKey) )

        # tab has       0x09/0x00100
        # shift tab has 0x19/0x20102
        # alt   tab has 0x09/0x80120
        # shftalttab    0x19/0xa0122
        # ctrl up 0xf700 0xa40101
        # NSDownArrowFunctionKey
        # NSLeftArrowFunctionKey
        # NSRightArrowFunctionKey
        # NSUpArrowFunctionKey
        # NSUpTextMovement
        # 
        # NSBacktabTextMovement
        # NSCancelTextMovement
        # NSDownTextMovement
        # NSIllegalTextMovement
        # NSLeftTextMovement
        # NSOtherTextMovement
        # NSReturnTextMovement
        # NSRightTextMovement
        # NSTabTextMovement
        # NSUpTextMovement
        # 
        

        # pdb.set_trace()
        if kwdbg:
            print "Key: ", hex(eventCharNum), hex(eventModifiers)

        if eventCharNum not in mykeys:
            super(KWOutlineView, self).keyDown_( theEvent )
            return None

        delg = self.delegate()
        consumed = False

        cmdShiftAlt = NSCommandKeyMask | NSShiftKeyMask | NSAlternateKeyMask

        # filter out other stuff
        eventModifiers &= NSDeviceIndependentModifierFlagsMask

        ###########################################################################
        #
        # Deleting
        if eventCharNum in (NSBackspaceCharacter, NSDeleteCharacter):
            if 1: #kwdbg:
                print "DELETE"
            # while editing, will be handled elsewhere
            # outline: delete selection (saving to a pasteboard stack)
            # table: delete selection (saving to a pasteboard stack)
            deleteNodes(self, selection=True)
            # deselect all or find a good way to select the next item
            self.deselectAll_( None )

        ###########################################################################
        #
        # Create new node
        elif eventCharNum == NSCarriageReturnCharacter:
            #pdb.set_trace()
            if eventModifiers & NSShiftKeyMask:
                if kwdbg:
                    print "SHIFT Return"
            else:
                # open new line and start editing

                # TODO: if already editing, start new line, continue editing

                # 
                sel = self.getSelectedRow()
                createNode(self, sel)
                consumed = True

        ###########################################################################
        #
        # Start editing current node
        elif eventCharNum == NSEnterCharacter:
            # cmd+alt enter
            # cmd enter
            # cmd shift enter
            # cmd alt shift enter

            # pdb.set_trace()

            if eventModifiers & (cmdShiftAlt | NSControlKeyMask):
                # dive down or up
                appl = NSApplication.sharedApplication()
                appdelg = appl.delegate()
                workspace= NSWorkspace.sharedWorkspace()

                ###################################################################
                #
                # Control Enter
                if eventModifiers & NSControlKeyMask:


                    ###############################################################
                    #
                    # Control Alt Enter
                    if eventModifiers & NSAlternateKeyMask:
                        # ctrl alt enter
                        items = self.getSelectionItems()
                        for item in items:
                            name = item.name
                            url = u""
                            # pdb.set_trace()

                            #
                            # make a handler here
                            #
                            # opml, html, rss, js, xml(generic)
                            # 
                            # for generic xml make getOPML a getXML with params
                            #
                            
                            # in a table
                            if name in (u"url", u"htmlUrl", u"xmlUrl", u"xmlurl"):
                                #
                                # FIXING HACK
                                # url = item.value
                                # pdb.set_trace()
                                url = item.displayValue
                                url = cleanupURL( url )
                                if url.endswith(".opml"):
                                    appdelg.newOutlineFromURL_( url )
                                else:
                                    url = NSURL.URLWithString_( url )
                                    workspace.openURL_( url )

                            # in an outline
                            else:
                                #
                                v = item.getValueDict()
                                typ = v.get("type", "")
                                url = v.get("url", "")

                                url = cleanupURL( url )
                                if url.endswith(".opml"):
                                    appdelg.newOutlineFromURL_( url )
                                else:
                                    url = NSURL.URLWithString_( url )
                                    workspace.openURL_( url )
                            consumed = True
                    else:
                        # ctrl enter
                        items = self.getSelectionItems()
                        for item in items:
                            if item.value:
                                title = item.name

                                # stop it if we are in a table
                                if item.typ != 1:
                                    continue

                                root = OutlineNode(u"__root__", u"", None, typeOutline)
                                for t in item.value:
                                    name, value = t
                                    node = OutlineNode(name, value, root, typeTable)
                                    root.addChild_(node)
                                    
                                if 0:
                                    if len(item.value) == 1 and ('value' in item.value):
                                        # one element dummy dict
                                        # this one shouldnt be opened in an editor
                                        #
                                        # anyway
                                        name = item.name
                                        value = item.value['value']
                                        node = OutlineNode(name, value, root, typeTable)
                                        root.addChild_(node)
                                    else:
                                        for k, v in item.value:
                                            node = OutlineNode(k, v, root, typeTable)
                                            root.addChild_(node)
                                elif False: # was else:
                                    # old code
                                    items = item.value.split('\n')
                                    for item in items:
                                        name, val = item.split("\t")
                                        node = OutlineNode(name, val, root, typeTable)
                                        root.addChild_(node)
                                appdelg.newTableWithRoot_fromNode_(root, item)
                        consumed = True

                ###################################################################
                #
                # not control but some combination of cmdShiftAlt
                else:
                    pass

                ###################################################################
                #
                #
                if eventModifiers & NSShiftKeyMask:
                    if eventModifiers & NSAlternateKeyMask:
                        if kwdbg:
                            print "SHIFT ALT Enter"
                    else:
                        if kwdbg:
                            print "SHIFT Enter"
                        
                        nodes = visitOutline(delg.root)
                        consumed = True
            
            #######################################################################
            #
            # Enter
            else:
                # start editing
                # 
                # pdb.set_trace()
                index = self.getSelectedRowIndex()
                # editColumn:row:withEvent:select:,
                # the index of the column being edited; otherwise –1.
                # editedColumn
                # edited = self.editedRow()
                edited = self.editedRow()
                if edited == -1:
                    if index != -1:
                        #start editing
                        if kwdbg:
                            print "Edit START"
                        self.editColumn_row_withEvent_select_(0, index, None, True)
                    else:
                        # empty selection
                        pass
                else:
                    # editing in progreess with row 'edited'
                    # how to stop?
                    pass
        
        ###########################################################################
        #
        # Outdenting
        elif eventCharNum == NSBackTabCharacter:
            # shift tab has it's own character
            if eventModifiers & NSShiftKeyMask:
                if kwdbg:
                    print "SHIFT Tab"
                # dedent selection
                
                if delg.typ in hierarchicalTypes:
                    # get selected rows
                    sel = self.getSelectionItems()
                    
                    # working from the end
                    sel.reverse()
                    
                    # dedent each row one level
                    for item in sel:
                        item.moveLeft()
                    consumed = True
                    self.reloadData()
        
        ###########################################################################
        #
        # Indenting
        elif eventCharNum == NSTabCharacter:
            # indent selection
            
            # get selected rows
            if delg.typ in hierarchicalTypes:
                sel = self.getSelectionItems()
                # indent each row one level
                postselect = set()
                for item in sel:
                    parent = item.parent
                    previous = item.previous()
                    if previous != -1:
                        # ignore command if item is first Child
    
                        previous.addChild_( item )
                        parent.removeChild_(item)
                        postselect.add(item)
                        self.expandItem_( previous )
                        self.reloadItem_reloadChildren_( previous, True )
                postselect = [self.rowForItem_(i) for i in postselect]
                self.selectItemRows_( postselect )
                
                consumed = True
                self.reloadData()


        ###########################################################################
        #
        # Move selection up
        elif eventCharNum == ord(NSUpArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:
                # pdb.set_trace()
                # get selected rows
                if delg.typ in hierarchicalTypes:
                    items = self.getSelectionItems()
                    moveSelectionUp(self, items)
                    # 
                    self.reloadData()

                    selection = [self.rowForItem_(i) for i in items]
                    if selection:
                        self.selectItemRows_( selection )
                
                    self.setNeedsDisplay_( True )
                    consumed = True


        ###########################################################################
        #
        # Move selection up
        elif eventCharNum == ord(NSDownArrowFunctionKey):
            if eventModifiers & NSControlKeyMask:
                # pdb.set_trace()
                # get selected rows
                if delg.typ in hierarchicalTypes:
                    items = self.getSelectionItems()
                    moveSelectionDown(self, items)
                    # 
                    self.reloadData()
                    
                    selection = [self.rowForItem_(i) for i in items]
                    if selection:
                        self.selectItemRows_( selection )
                
                    self.setNeedsDisplay_( True )
                    consumed = True
                    


        if not consumed:
            super(KWOutlineView, self).keyDown_( theEvent )

    #
    # utilities
    #
    def getSelectionItems(self):
        """The actual nodes of the current selection are returned."""
        sel = self.selectedRowIndexes()
        n = sel.count()
        result = []
        if not n:
            return result
        next = sel.firstIndex()
        result.append( self.itemAtRow_(next) )

        for i in range(1, n):
            next = sel.indexGreaterThanIndex_(next)
            result.append( self.itemAtRow_(next) )
        return result

    def getSelectedRow(self):
        # pdb.set_trace()
        sel = self.getSelectedRowIndex()
        if sel == -1:
            return sel
        item = self.itemAtRow_(sel)
        return item

    def getSelectedRowIndex(self):
        sel = self.selectedRow()
        return sel

    def selectItemRows_( self, itemIndices ):
        s = NSMutableIndexSet.indexSet()
        for i in itemIndices:
            s.addIndex_( i )
        self.selectRowIndexes_byExtendingSelection_(s, False)

    def selectRowItem_(self, item):
        index = self.rowForItem_( item )
        s = NSIndexSet.indexSetWithIndex_( index )
        self.selectRowIndexes_byExtendingSelection_(s, False)


class NiceError:
    """Wrapper for an exception so we can display it nicely in the browser."""

    def __init__(self, exc_info):
        self.exc_info = exc_info

    def __repr__(self):
        from traceback import format_exception_only
        lines = format_exception_only(*self.exc_info[:2])
        assert len(lines) == 1
        error = lines[0].strip()
        return "*** error *** %s" %error

#
# Nodewalk
#
def stdAction( node, level ):
    # Debugging HACK
    s = "  " * level
    s = s + unicode(node)
    n = str(node.retainCount())
    n = n.ljust(4)
    s = n + s
    print s.encode("utf-8")
    

def visitOutline(startnode, startlevel=0, depthFirst=False, action=stdAction):
    # Debugging HACK
    # pdb.set_trace()
    action(startnode, startlevel)
    if len(startnode.children) > 0:
        for p in startnode.children:
            visitOutline(p, startlevel+1, depthFirst, action)
    return 

def dfid(T,children,callback=stdAction):
    # some ActiveState snippet
    def visit(node,i):
        if i == 0:
            callback(node, i)
        else:
            for c in node.children:
                visit(c,i-1)
    i = 0
    while 1:
        visit(T,i)
        i += 1


#
# Outline Document Model
#
class OutlineDocumentModel(NSObject):

    """This is a delegate as well as a data source for NSOutlineViews."""
    # 
    # instantiated from AppDelegate
    #
    # no bindings

    def initWithObject_parentNode_(self, obj, typ, parentNode):
        self = self.init()
        self.typ = typ
        self.parentNode = parentNode
        if not isinstance(obj, OutlineNode):
            obj = OutlineNode(unicode(obj), "", None, typeOutline)
        self.root = obj
        self.controller = None
        self.dirty = False
        return self

    def release():
        if kwdbg:
            print "MODEL_release"
        self.root.release()
        super(OutlineDocumentModel, self).release()

    def setController_(self, controller):
        self.controller = controller

    def reloadData_(self, item):
        if self.controller:
            self.controller.reloadData_(item)

    def isSubEditor(self):
        return self.parentNode != None

    def appendToRoot_Value_(self, name, value):
        n = OutlineNode(name, value, self.root, self.typ)
        self.root.addChild_( n )
        self.reloadData_( None )
        idx = self.controller.outlineView.rowForItem_(n)
        return idx

    #
    # tableview delegate
    #
    # numberOfRowsInTableView:
    def tableView_objectValueForTableColumn_row_(self, tv, column, row):
        c = col.identifier()
        item = self.root.childAtIndex_( row )
        if c == u"type":
            return item.displayType
        elif c == u"value":
            return item.displayValue
        elif c == u"name":
            return item.displayName
        elif c == u"comment":
            return item.displayComment

    def numberOfRowsInTableView_(self, tv):
        return self.root.children.count()

    def outlineViewColumnDidResize_(self, aNotification):
        userInfo = aNotification.userInfo()
        column = userInfo.valueForKey_( u"NSTableColumn" )
        oldWidth = userInfo.valueForKey_( u"NSOldWidth" ).intValue()
        newWidth = column.width()
        # print "COL: '%s' changed from: %i  to  %i" % (column.identifier(), oldWidth, newWidth)

    def tableViewColumnDidResize_(self, aNotification):
        # for some reaon only th outlineView delegate is called. Even for tables
        pass
    #
    # NSOutlineViewDataSource  methods
    #
    def outlineView_numberOfChildrenOfItem_(self, view, item):
        if not item:
            item = self.root
        n = item.noOfChildren()
        return n


    def outlineView_child_ofItem_(self, view, child, item):
        if not item:
            item = self.root
        return item.childAtIndex_( child )


    def outlineView_isItemExpandable_(self, view, item):
        return item.noOfChildren() > 0


    def outlineView_objectValueForTableColumn_byItem_(self, view, col, item):
        c = col.identifier()
        if not item:
            item = self.root
        if c == u"type":
            return item.displayType
        elif c == u"value":
            return item.displayValue
        elif c == u"name":
            return item.displayName
        elif c == u"comment":
            return item.displayComment


    def outlineView_setObjectValue_forTableColumn_byItem_(self, view, value, col, item):
        # pdb.set_trace()
        c = col.identifier()
        if not item:
            item = self.root
        if c == u"type":
            pass #return item.displayType
        elif c == u"value":
            if self.parentNode != None:
                name = item.name
                self.parentNode.updateValue_( (name, unicode(value)) )
                
            item.setValue_( value )
        elif c == u"name":
            item.setName_(value)
        elif c == u"comment":
            item.setComment_(value)


    # delegate method
    def outlineView_shouldEditTableColumn_item_(self, view, col, item):
        return item.editable


    def outlineView_heightOfRowByItem_(self, ov, item):
        # where to store this
        lineheight = 14

        if not self.controller.variableRowHeight:
            return lineheight
        if item.value:
            return len(item.value) * lineheight
        else:
            return lineheight

    # UNUSED
    def ovUpdateItem_Key_Value_(self, item, key, value):
        # update a single key value pair in the value dict
        pass

    #def outlineView_didClickTableColumn_(self, view, tablecolumn):
    #    pass


    # Delegate
    # outlineView:dataCellForTableColumn:item:
    # outlineView:didClickTableColumn:
    # outlineView:heightOfRowByItem: 
    # outlineView:isGroupItem: 10.5
    # outlineView:shouldCollapseItem:
    # outlineView:shouldEditTableColumn:item:
    # outlineView:shouldExpandItem:
    # outlineView:shouldSelectItem:
    # outlineView:shouldSelectTableColumn:
    # outlineView:shouldShowCellExpansionForTableColumn:item: 10.5
    # outlineView:shouldTrackCell:forTableColumn:item: 10.5
    # outlineView:toolTipForCell:rect:tableColumn:item:mouseLocation:
    # outlineView:willDisplayCell:forTableColumn:item:
    # outlineView:willDisplayOutlineCell:forTableColumn:item:
    # outlineViewColumnDidMove:
    # outlineViewColumnDidResize:
    # outlineViewItemDidCollapse:
    # outlineViewItemDidExpand:
    # outlineViewItemWillCollapse:
    # outlineViewItemWillExpand:
    # outlineViewSelectionDidChange:
    # outlineViewSelectionIsChanging:
    # selectionShouldChangeInOutlineView:

    # Notifications
    # NSOutlineViewColumnDidMoveNotification
    # NSOutlineViewColumnDidResizeNotification
    # NSOutlineViewItemDidCollapseNotification
    # NSOutlineViewItemDidExpandNotification
    # NSOutlineViewItemWillCollapseNotification
    # NSOutlineViewItemWillExpandNotification
    # NSOutlineViewSelectionDidChangeNotification
    # NSOutlineViewSelectionIsChangingNotification
    # 


import itertools
counter = itertools.count()
#
# Outline
#

typeOutline = 1
typeTable = 2
typeBrowser = 3
editorTypes = (typeOutline, typeTable, typeBrowser)
hierarchicalTypes = (typeOutline, typeBrowser)


class NodeValue(object):
    def __init__(self, value):
        # pdb.set_trace()
        if type(value) != list:
            value = self.listFromDisplayValue( value )

        if type(value) != list:
            # pdb.set_trace()
            print "VALUE is not list"

        self.value = value
        self.typ = len(value) > 1

    def displayValue(self):
        # maxlen = max([len(k) for k in self.value.keys()])
        l = []
        if type(self.value) != list:
            # pdb.set_trace()
            print "VALUE is not list"
        for t in self.value:
            k, v = t
            if k != "":
                l.append(u"%s:\t%s" % (k, v) )
            else:
                l.append(u"%s" % (v,))
        return '\n'. join(l)


    def listFromDisplayValue(self, displayValue):
        lines = displayValue.split('\n')
        l = []
        for line in lines:
            if line.count(':\t') != 1:
                k = u""
                v = line
            else:
                k, v = line.split(':\t', 1)
            l.append( (k, v) )
        return l

    def isSingleValue(self):
        if len(self.value) == 1:
            if self.value[0][0] in (u"", u"value"):
                return True
        return False

    def isMultiValue(self):
        return not self.isSingleValue()


class OutlineNode(NSObject):

    """Wrapper class for items to be displayed in the outline view."""

    # We keep references to all child items (once created). This is
    # neccesary because NSOutlineView holds on to OutlineNode instances
    # without retaining them. If we don't make sure they don't get
    # garbage collected, the app will crash. For the same reason this
    # class _must_ derive from NSObject, since otherwise autoreleased
    # proxies will be fed to NSOutlineView, which will go away too soon.

    def __new__(cls, *args, **kwargs):
        # "Pythonic" constructor
        return cls.alloc().init()

    def __repr__(self):
        return "<OutlineNode(%i, name='%s')" % (self.nodenr, self.name)

    def XXdealloc(self):
        if kwdbg:
            print "SELF_RELEASE:", self
        if self.children:
            for c in self.children:
                if kwdbg:
                    print "FAKE CHILDREN_RELEASE", c
                # c.release()
            self.children.dealloc()
        #super( OutlineNode, self).release()
        #self.release()
        
    def __init__(self, name, obj, parent, typ):
        self.typ = typ
        self.setParent_(parent)

        # debugging
        self.nodenr = counter.next()

        self.setName_( name )
        self.setValue_( obj )
        self.setComment_( "" )        

        self.children = NSMutableArray.arrayWithCapacity_( 10 )
        self.editable = True

    def setParent_(self, parent):
        if parent != None:
            # parent.retain()
            if kwdbg:
                print "setparent_RETAIN:", parent
        self.parent = parent
    
    def releaseParent(self):
        parent = self.parent
        if not parent == None:
            if kwdbg:
                print "setparent_RELEASE:", parent
            # parent.release()
        # self.parent = -1
    
    #
    def setName_(self, value):
        self.name = value
        s = unicode(value)
        if kwdbg:
            self.displayName = u"(%i)  - %s" % (self.nodenr, s)
        else:
            self.displayName = u"%s" % (s,)
    
    def setValue_(self, value):
        if value in (u"", {}, [], None, False):
            self.value = [(u"",u"")]
            self.displayValue = u""
            self.type = u"String"            
        else:
            nv = NodeValue( value )
            self.value = nv.value
            
            if nv.isMultiValue():
                self.type = u"Attributes"
            else:
                self.type = u"String"
            self.displayValue = nv.displayValue()
        self.displayType = self.type


    def addValue_(self, nameValue):
        self.value.append( nameValue )
        self.setValue_( self.value )
        r = self.findRoot()
        m = r.model
        m.reloadData_(self)


    def removeValue_(self, nameValue):
        # repeated myself; copied from updateValue_ ...
        # pdb.set_trace()
        newname, newvalue = nameValue
        updated = idx = False
        for i,t in enumerate(self.value):
            k, v = t
            if k == newname:
                idx = i
                break
        if idx >= 0:
            self.value.pop(idx)
            updated = True

        if updated:
            self.setValue_( self.value )
            r = self.findRoot()
            m = r.model
            m.reloadData_(self)
        return updated


    def updateValue_(self, nameValue):
        # pdb.set_trace()
        newname, newvalue = nameValue
        updated = idx = None
        for i,t in enumerate(self.value):
            k, v = t
            if k == newname:
                idx = i
                break

        if idx != None:
            self.value.pop(idx)
            self.value.insert(idx, nameValue)
            updated = True

        if not updated:
            self.value.append( nameValue )
        self.setValue_( self.value )

        r = self.findRoot()
        m = r.model
        m.reloadData_(self)


    def getValueDict(self):
        if len(self.value) == 0:
            return {}
        elif len(self.value) == 1:
            if self.value[0][0] == "":
                return {'value': self.value[0][1] }
            else:
                return {self.value[0][0]: self.value[0][1] }
        else:
            d = {}
            for t in self.value:
                k, v = t
                d[k] = v
            return d


    def setComment_(self, comment):
        self.comment = comment
        self.displayComment = unicode( self.comment )
        
    #
    def noOfChildren(self):
        return self.children.count()
    
    #
    def addChild_(self, child):
        if isinstance(child, OutlineNode):
            if kwdbg:
                print "addChild_setParent", child
            child.setParent_(self)
            self.children.addObject_( child )


    def addChild_atIndex_(self, child, index):
        # child.retain()
        self.children.insertObject_atIndex_( child, index)
        if kwdbg:
            print "addChild_atIndex_setParent", child
        child.setParent_(self)


    def childAtIndex_( self, index ):
        # delegeate child getter
        if index <= self.children.count():
            return self.children.objectAtIndex_( index )
        return None


    def removeChild_(self, child):
        # perhaps this should return the orphan

        # root is always outlineType
        index = self.children.indexOfObject_(child)
        if index != NSNotFound:
            c = self.children.objectAtIndex_( index )
            self.children.removeObjectAtIndex_( index )
            c.releaseParent()
            if kwdbg:
                print "removeChild_RELEASE:", c
            #c.release()
            return index
        return False

    def isEditable(self):
        return self.editable

    def isExpandable(self):
        return self.children.count() > 0

    def isRoot(self):
        return self.parent == None

    def findRoot(self):
        s = self
        while True:
            if s.parent == None:
                return s
            s = s.parent

    def pathFromRoot(self):
        l = []
        s = self
        while True:
            if s.parent == None:
                return l
            s = s.parent
            l.append( s.name )

    #
    # node math
    #
    def siblingCount(self):
        """How many are there me and my siblings?"""
        if self.parent == None:
            # i am root
            return -1
        p = self.parent
        # should work for tables too since root node is outline type
        l = p.children.count()
        return l
        

    def siblingIndex(self):
        """What is my index in this sibling group?"""
        if self.parent == None:
            # i am root
            return -1
        p = self.parent
        index = p.children.indexOfObject_(self)
        if index == NSNotFound:
            return -1
        return index

    def previousIndex(self):
        """The index of the sibling before me."""
        n = self.siblingIndex()
        if n >= 0:
            if n > 0:
                # not first, so there's one before me
                return n-1

            # is first
            return -1

        # no parent
        return -1


    def nextIndex(self):
        """The index of the sibling after me."""
        n = self.siblingIndex()
        if n >= 0:
            l = self.siblingCount()
            if n < l - 1:
                # last index is allowed since it will be appended to the array
                return n+1
            # is last
            # perhaps left here
            return -1
        # no parent
        return n


    def isFirst(self):
        """Am I the first sibling."""
        n = self.siblingIndex()
        return n == 0


    def isLast(self):
        """Am I the last sibling."""
        n = self.siblingIndex()
        l = self.siblingCount()
        return n == (l - 1)


    def next(self):
        """Return my immediate next sibling or -1."""
        n = self.nextIndex()
        if n >= 0:
            return self.parent.children.objectAtIndex_(n)
        return -1
            
    def previous(self):
        """Return my immediate previous sibling or -1."""
        n = self.previousIndex()
        if n >= 0:
            return self.parent.children.objectAtIndex_(n)
        return -1


    def isChildOf_(self, other):
        p = self
        i = 0
        while not p.isRoot():
            p = p.parent
            i += 1
            if p == other:
                return i
        return -1
            

    def findFirstChildWithName_(self, name):
        for child in self.children:
            if child.name == name:
                return child

    #
    # node movements
    #
    def makeChildOf_(self, other):
        """Move self to be latest child of other."""

        # parent needs to be saved since it's lost in addChild_
        parent = self.parent
        if parent == None:
            return -1
        other.addChild_(self)
        parent.removeChild_(self)


    def moveLeft(self):
        # noveAfterParent
        """For dedenting."""
        if not self.typ in hierarchicalTypes:
            return
        parent = self.parent
        if parent == None:
            return -1

        grandparent = parent.parent
        if parent.isLast():
            # append after parent
            self.makeChildOf_(grandparent)
            #grandparent.addChild_(self)
            #parent.removeChild_(self)

        else:
            # insert after parent
            parentIndex = parent.siblingIndex()
            grandparent.addChild_atIndex_(self, parentIndex+1)
            parent.removeChild_(self)

    def moveRight(self):
        # make self child of previous
        if not self.typ in hierarchicalTypes:
            return

        previous = self.previous()
        if previous != -1:
            self.makeChildOf_(previous)        


#
# node editing
#
# TODO: deleting does not update correctly.
# line stays visible in parent view. needsRedraw_?
#
def deleteNodes(ov, nodes=(), selection=False):
    if selection:
        sel = ov.getSelectionItems()
    else:
        sel = nodes
    delg = ov.delegate()
    parentNode = delg.parentNode
    for item in sel:
        p = item.parent
        deleted = True
        if parentNode:
            deleted = parentNode.removeValue_( (item.name, item.value) )
        if deleted:
            p.removeChild_( item )
    ov.reloadData()


def createNode(ov, selection, startEditing=True):
    # create node at selection and start editing
    
    # open new line and start editing
    # if already editing, start new line, continue editing
    typ = ov.delegate().typ
    if selection == -1:
        rowIndex = ov.delegate().appendToRoot_Value_(u"", u"")
    else:
        # pdb.set_trace()
        p = selection.parent
        node = OutlineNode(u"", "", selection.parent, typ)
        targetIdx = selection.nextIndex()
        if targetIdx == -1:
            p.addChild_( node )
        else:
            p.addChild_atIndex_( node, targetIdx )
        ov.reloadData()
        ov.selectRowItem_( node )
        rowIndex = ov.rowForItem_( node )
        consumed = True
    
    if startEditing:
        s = NSIndexSet.indexSetWithIndex_( rowIndex )
        ov.selectRowIndexes_byExtendingSelection_(s, False)
        ov.reloadData()
        ov.editColumn_row_withEvent_select_(0, rowIndex, None, True)


def moveSelectionUp(ov, items):
    for item in items:
        # move item before previous
        #  get grandparent
        #  insert at index of previous
        previous = item.previous()
        if previous == -1:
            return
        parent = item.parent
        if parent == None:
            return
        previousIndex = previous.siblingIndex()
        parent.removeChild_( item )
        parent.addChild_atIndex_(item, previousIndex)


def moveSelectionDown(ov, items):
    #

    # this really needs to be sorted down; use indices
    # otherwise there will be overlapping moves destroying
    # sortorder
    items.reverse()
    # pdb.set_trace()
    for item in items:

        parent = item.parent
        if parent == None:
            return
        next = item.next()
        if next == -1:
            return
        parent.removeChild_( item )
        # pdb.set_trace()
        # after removal of item, nexitndex changes
        nextIndex = next.nextIndex()
        if nextIndex == -1:
            parent.addChild_( item )
        else:
            parent.addChild_atIndex_(item, nextIndex)

def moveSelectionLeft(ov, selection):
    pass

def moveSelectionRight(ov, selection):
    pass


def cleanupURL( url ):
    # lots of URLs contain spaces, &, '
    purl = urlparse.urlparse( url )
    purl = list(purl)
    path = purl[2]
    path = urllib.unquote( 'http://' + path )
    path = urllib.quote( path )
    path = path[9:]
    purl[2] = path
    purl = urlparse.urlunparse( purl )
    purl = unicode(purl)
    return purl
        



