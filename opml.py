# -*- coding: utf-8 -*-

import os
import datetime

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import StringIO

import pprint
pp = pprint.pprint

kwdbg = False
import pdb

keyTypes = {}
opmlTags = {}
nodeTypes = {}
urls = {}


def getfolder(node):
    global keyTypes, opmlTags, nodeTypes, urls
    result = []
    for n in list(node):
        keys = n.attrib.keys()

        if kwdbg:
            keys.sort()
            keys = tuple(keys)
            if not keys in keyTypes:
                keyTypes[ keys ] = 1
            else:
                keyTypes[ keys ] += 1
            for key in keys:
                if not key in opmlTags:
                    opmlTags[ key ] = 1
                else:
                    opmlTags[ key ] += 1
            if 'type' in keys:
                typ = n.attrib['type']
                if typ not in nodeTypes:
                    nodeTypes[typ] = 1
                else:
                    nodeTypes[typ] += 1
        name = n.attrib.get('text', '')
        nchild = len(n)
        b = {'name': name, 'children': [], 'noofchildren': nchild, 'attributes': {}}
        for k in keys:
            b['attributes'][k] = n.attrib.get(k, "")
        subs = list(n)
        if subs:
            s = getfolder(n)
            b['children'] = s
        result.append(b)
    return result


def getOPML( rootnode ):
    global keyTypes, opmlTags, nodeTypes, urls
    
    d = {'head': [], 'body':[]}

    # get head
    head = rootnode.find("head")

    # get body
    body = rootnode.find("body")
    

    if head:
        for item in list(head):
            #print "head:", item.tag, item.text
            d['head'].append( (item.tag, item.text) )

    if body:
        for item in list(body):
            tag = item.tag
            name = item.attrib.get('text', '')
            keys = item.attrib.keys()
    
            if 'children' in keys:
                print "CHILDREN ATTRIBUTE"
                # pdb.set_trace()
                print "CHILDREN ATTRIBUTE"
    
            if kwdbg:
                keys.sort()
                keys = tuple(keys)
                if not keys in keyTypes:
                    keyTypes[ keys ] = 1
                else:
                    keyTypes[ keys ] += 1
                for key in keys:
                    if not key in opmlTags:
                        opmlTags[ key ] = 1
                    else:
                        opmlTags[ key ] += 1
            nchild = len(item)
            b = {'name': name, 'children': [], 'noofchildren': nchild, 'attributes': {}}
            for k in keys:
                b['attributes'][k] = item.attrib.get(k, "")
    
            #print "Item:", item.attrib['text'], nchild
            b['children'] = getfolder(item)
            d['body'].append( b )

    if kwdbg:
        print
        print "KeyTypes", len(keyTypes)
        pp(keyTypes)
        print
        print "OPMPTags", len(opmlTags)
        pp(opmlTags)
        print
        print "types", len(nodeTypes)
        pp(nodeTypes)
        
    return  d


def from_string(opml_text):
    return getOPML(etree.fromstring(opml_text))

def parse(opml_url):
    return getOPML(etree.parse(opml_url))


def indentXML(elem, level=0, width=2):
    i = "\n" + level * (" " * width)
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indentXML(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def createSubNodes(OPnode, ETnode, level):
    # do attributes
    name = OPnode.name
    value = OPnode.getValueDict()
    comment = OPnode.comment

    # update attributes
    if ETnode.tag != "body":
        #d = dictFromValue( value )
        ETnode.attrib['text'] = name
        
        # don't have an empty value: tag
        if len(value) == 1:
            if 'value' in value:
                value.pop('value')

        ETnode.attrib.update( value )
        if comment != "":
            ETnode.attrib['comment'] = comment

    if len(OPnode.children) > 0:
        
        # do children
        for child in OPnode.children:
            ETSub = etree.SubElement( ETnode, "outline")
            s = createSubNodes( child, ETSub, level+1 )
    return ETnode
    
def generateOPML( rootNode, filepath, indent=2 ):

    # pdb.set_trace()

    rootOPML = etree.Element("opml")
    rootOPML.attrib["version"] = "2.0"

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    c = etree.Comment("Created by Cactus v0.2.0 on %s." % (now,))
    rootOPML.append(c)

    headOP = rootNode.findFirstChildWithName_( "head" )

    head = etree.SubElement(rootOPML, "head")
    
    if headOP:
        # pdb.set_trace()
        for headsub in headOP.children:
            name = headsub.name
            value = headsub.getValueDict()
            comment = headsub.comment
            node = etree.SubElement( head, name)
            if value: # != "":
                # node.text = value
                node.text = value['value']
            if comment != "":
                node.attrib["comment"] = comment
            print "HEAD: ", name
    else:
        # create generic head here
        pass

    body = etree.SubElement(rootOPML, "body")
    bodyOP = rootNode.findFirstChildWithName_( "body" )

    if bodyOP:
        nodes = createSubNodes(bodyOP, body, 1)
    else:
        # an outline without body
        # pdb.set_trace()
        nodes = createSubNodes(rootNode, body, 1)


    if indent:
        indentXML(rootOPML, 0, indent)

    return rootOPML


opmplnodetypes = {
    'blogpost': ('url', ),
    'code': (),
    'howto': (),
    'html': (),
    'include': (),
    'link': (),
    'outline': (),
    'photo': (),
    'redirect': (),
    'river': (),
    'rss': (),
    'scripting2Post': (),
    'thumbList':()
    }

