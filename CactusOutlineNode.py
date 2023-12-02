
# -*- coding: utf-8 -*-

from __future__ import print_function

"""A collection of outline related stuff
"""

import sys
import os

import re

import traceback

import time
import datetime

import math
import feedparser

kwdbg = False
kwlog = True

import pdb
import pprint
pp = pprint.pprint

# debugging; gives nodes a serialnr
import itertools
counter = itertools.count()


import CactusOutlineTypes
typeOutline = CactusOutlineTypes.typeOutline

import objc
# super = objc.super
from objc._pythonify import OC_PythonFloat, OC_PythonLong
objc.options.deprecation_warnings=1



import CactusTools
makeunicode = CactusTools.makeunicode

import Foundation
NSObject = Foundation.NSObject

NSMutableArray = Foundation.NSMutableArray

NSNotFound = Foundation.NSNotFound
NSIndexSet = Foundation.NSIndexSet

NSNumber = Foundation.NSNumber


import AppKit
NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString

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

#
# NodeValue class
#

class NodeValue(object):
    """NodeValue is a helper with the value column which in some cases has
    a dual existence as a string or as a table.
    """

    def __init__(self, value):
        if type(value) != list:
            if type(value) in (pstr, punicode, NSString, bool, int, long,
                               NSMutableString, objc.pyobjc_unicode,
                               OC_PythonFloat, OC_PythonLong):
                value = self.listFromDisplayValue_( value )
            elif isinstance(value, dict):
                value = self.listFromDictionary_( value )
            else:
                print( "BOGATIVE VALUETYPE:", type(value) )

        if type(value) != list:
            print( "VALUE is not list" )

        self.value = value
        self.typ = len(value) > 1

    def displayValue(self):
        # maxlen = max([len(k) for k in self.value.keys()])
        l = []
        if not isinstance(self.value, list):
            print( "VALUE is not list" )
            print( repr(self.value) )
        for t in self.value:
            k, v = t
            if k != "":
                l.append(u"%s:\t%s" % (k, v) )
            else:
                l.append(u"%s" % (v,))
        return '\n'. join(l)

    def listFromDisplayValue_(self, displayValue):
        try:
            lines = displayValue.split('\n')
        except AttributeError as err:
            print( err )
            lines = [ makeunicode(displayValue) ]

        l = []
        for line in lines:
            if line.count(':\t') == 0:
                k = u""
                v = line
            else:
                k, v = line.split(':\t', 1)
            l.append( (k, v) )
            d = {}
            for item in l:
                k, v = item
                if k in d:
                    d[k] = d[k] + u'\n' + v
                else:
                    d[k] = v
            l = list( d.items() )
        return l

    def listFromDictionary_(self, value):
        l = []
        for k, v in value.items():
            l.append( (k,v) )
        return l

    def isSingleValue(self):
        if len(self.value) == 1:
            if self.value[0][0] in (u"", u"value"):
                return True
        return False

    def isMultiValue(self):
        return not self.isSingleValue()



#
# Outline Node class
#

class OutlineNode(NSObject):

    """Wrapper class for items to be displayed in the outline view."""

    # We keep references to all child items (once created). This is
    # neccesary because NSOutlineView holds on to OutlineNode instances
    # without retaining them. If we don't make sure they don't get
    # garbage collected, the app will crash. For the same reason this
    # class _must_ derive from NSObject, since otherwise autoreleased
    # proxies will be fed to NSOutlineView, which will go away too soon.

    # attributes of OutlineNode:
    # name
    # value
    # comment
    # type
    # parent
    # children
    #
    # displayValue
    #

    #
    # to be added
    #
    # nodeAttributes

    # that's the deal
    def __new__(cls, *args, **kwargs):
        return cls.alloc().init()

    def __init__(self, name, obj, parent, typ, rootNode):

        self.typ = objc.ivar()
        self.attributes = objc.ivar()
        self.name = objc.ivar()
        self.comment = objc.ivar()
        self.maxHeight = objc.ivar()
        
        self.rootNode = objc.ivar()
        self.nodenr = objc.ivar()
        self.children = objc.ivar()
        self.maxHeight = objc.ivar()
        self.controller = objc.ivar()
        
        # this is outlinetype, not valueType
        self.typ = typ
        self.attributes = ""
        self.name = ""
        self.comment = ""
        self.maxHeight = 1
        self.setParent_(parent)
        self.rootNode = rootNode

        # debugging
        self.nodenr = next( counter ) #counter.next()

        # these must exists before any name/value is set
        self.children = NSMutableArray.arrayWithCapacity_( 0 )
        self.maxHeight = 1

        self.setName_( name )
        self.setValue_( obj )


        self.setAttributes_( obj )
        self.setComment_( "" )

        # self.setMaxLineHeight()

        self.controller = None
        #if rootNode != None:
        #    self.controller = rootNode.controller

        # leave this here or bad things will happen
        self.retain()

    def __repr__(self):
        return "<OutlineNode(%i, name='%s')" % (self.nodenr, self.name)

    def dealloc(self):
        print( "OutlineNode.dealloc()" )
        # pp(self.__dict__)
        try:
            self.children.release()
        except Exception as err:
            print( "EXCEPTION: OutlineNode.dealloc()" + str(err) )

        # 2013-05-15
        # currently crashes during dict dealloc.
        # seems like I'm on the right way to deallocation...
        psolved = False
        if psolved:
            objc.super(OutlineNode, self).dealloc()


    def setMaxLineHeight(self):
        items = [
            self.calcAttributesHeight(),
            self.lineHeight_( self.name ),
            self.lineHeight_( self.comment )]
        self.maxHeight = max(items)

    def setAttributes_(self, attrs):
        d = {}
        t = type(attrs)
        if t in (pstr, punicode, NSString, bool, int, long,
                 NSMutableString, objc.pyobjc_unicode):
            # stringtype
            d[ u"" ] = makeunicode(attrs)
        elif t in (list, tuple):
            #listtype
            for item in attrs:
                key, val = item
                key = makeunicode(key)
                val = makeunicode(val)
                d[ key ] = val
        elif t in (dict, feedparser.FeedParserDict):
            for key in attrs:
                val = makeunicode(attrs[key])
                key = makeunicode(key)
                d[ key ] = val
        else:
            # ???
            pass
        self.attributes = d
        self.setMaxLineHeight()


    def lineHeight_(self, val):
        lines = 0
        try:
            lines += val.count( u"\r" )
            lines += val.count( u"\n" )
        except Exception as err:
            print( "\n\nERROR in lineHeight_()" )
            tb = makeunicode(traceback.format_exc())
            print( err )
            print()
            print( tb )
            print()
        vallength = len( val )
        if vallength > 100:
            pass
        lines += int(math.ceil(vallength / 55.0))
        return max(1, lines)

    def calcAttributesHeight(self):
        lineheight = 0
        for key in self.attributes:
            lineheight += self.lineHeight_( self.attributes[ key ] )
        return lineheight


    def setParent_(self, parent):
        self.parent = parent

    #
    def setName_(self, value):
        self.name = makeunicode(value)
        self.setMaxLineHeight()

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

    # UNUSED
    def addValue_(self, nameValue):
        self.value.append( nameValue )
        self.setValue_( self.value )
        r = self.findRoot()
        c = r.controller
        c.outlineView.reloadData()

    # used in attribute editor
    def removeValue_(self, nameValue):
        # repeated myself; copied from updateValue_ ...
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
            c = r.controller
            c.outlineView.reloadData()
        return updated

    # used in attribute editor
    def updateValue_(self, nameValue):
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
        try:
            c = r.controller
            c.outlineView.reloadData()
        except Exception as err:
            pass

    # essential
    def getValueDict(self):
        """Create a dictionary from the value."""
        if len(self.value) == 0:
            return {}
        elif len(self.value) == 1:
            if self.value[0][0] == "":
                if self.value[0][1] != "":
                    return {'value': self.value[0][1] }
                else:
                    return {}
            else:
                return {self.value[0][0]: self.value[0][1] }
        else:
            d = {}
            for t in self.value:
                k, v = t
                d[k] = v
            return d

    def setComment_(self, comment):
        self.comment = makeunicode( comment )
        self.setMaxLineHeight()

    #
    def noOfChildren(self):
        return self.children.count()

    #
    def addChild_(self, child):
        if kwlog and 0:
            print( "OutlineNode.addChild_", child )
        # retain: child+1
        if isinstance(child, OutlineNode):
            if child.parent != self:
                child.setParent_(self)
            self.children.addObject_( child )
            # child.release()

    def addChild_atIndex_(self, child, index):
        if kwdbg:
            print( "addChild_atIndex_setParent", child )
        # retain: child+1

        self.children.insertObject_atIndex_( child, index)
        if child.parent != self:
            child.setParent_(self)
        child.setParent_(self)
        # child.release()

    def childAtIndex_( self, index ):
        # delegeate child getter
        if index <= self.children.count():
            return self.children.objectAtIndex_( index )
        return None

    def removeChild_(self, child):
        # retain: child-1
        # perhaps this should return the orphan

        # root is always outlineType
        index = self.children.indexOfObject_(child)
        if index != NSNotFound:
            self.children.removeObjectAtIndex_( index )
            return index
        return False

    def isExpandable(self):
        return self.children.count() > 0

    def isRoot(self):
        return self.parent == None

    # this is used too excessively, make it a var
    def findRoot(self):
        if self.rootNode != None:
            return self.rootNode
        s = self
        while True:
            if s.parent == None:
                if s != self:
                    self.rootNode = s
                return s
            s = s.parent

    def pathFromRoot(self):
        l = []
        s = self
        while True:
            if s.parent == None:
                return l
            s = s.parent
            l.append( s )

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
        """Move self to be last child of other."""

        # parent needs to be saved since it's lost in addChild_
        parent = self.parent
        if parent == None:
            return -1
        other.addChild_(self)
        parent.removeChild_(self)

    def moveLeft(self):
        # noveAfterParent
        """For dedenting."""
        if not self.typ in CactusOutlineTypes.hierarchicalTypes:
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
        if not self.typ in CactusOutlineTypes.hierarchicalTypes:
            return

        previous = self.previous()
        if previous != -1:
            self.makeChildOf_(previous)

    def copyPython(self):
        result = []
        start = {
            'name': makeunicode(self.name),
            'value': self.getValueDict(),
            'typ': self.typ,
            'children': result}
        for i in self.children:
            result.append( i.copyPython() )
        return start


    def copyNodesWithRoot_(self, root):
        result = []
        node = OutlineNode(self.name, self.getValueDict(), root, typeOutline, None)
        node.setComment_( self.comment )
        for i in self.children:
            node.addChild_( i.copyNodesWithRoot_(root) )
        return node

