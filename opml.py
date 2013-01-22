# -*- coding: utf-8 -*-

import os
import datetime

import cStringIO
import binascii

import pprint
pp = pprint.pprint
import traceback

kwdbg = True
kwlog = True
import pdb


import lxml
import lxml.etree
lxmletree = lxml.etree

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import lxml.html
#import lxml.html.builder

import PyRSS2Gen

import CactusVersion

import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException
XMLParseErrorException = CactusExceptions.XMLParseErrorException
HTMLParseErrorException = CactusExceptions.HTMLParseErrorException
PLISTParseErrorException = CactusExceptions.PLISTParseErrorException


import Foundation
NSURL = Foundation.NSURL
NSDictionary = Foundation.NSDictionary
NSUserDefaults = Foundation.NSUserDefaults
NSMutableDictionary = Foundation.NSMutableDictionary
NSMutableArray = Foundation.NSMutableArray
NSData = Foundation.NSData
NSNumber = Foundation.NSNumber
NSMutableData = Foundation.NSMutableData
NSKeyedArchiver = Foundation.NSKeyedArchiver


# some globals for opml analyzing
keyTypes = {}
opmlTags = {}
nodeTypes = {}
urls = {}


# -----------------------------------------------

def getOutlineNodes(node):
    """Read the outline nodes in OPML/body
    """
    global keyTypes, opmlTags, nodeTypes, urls
    result = []
    for n in list(node):
        keys = n.attrib.keys()

        if kwlog:
            # gather some stuff for debugging and opml analyzing
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
                theType = n.attrib['type']
                if theType not in nodeTypes:
                    nodeTypes[theType] = 1
                else:
                    nodeTypes[theType] += 1
        name = n.attrib.get('text', '')
        nchild = len(n)
        b = {
            'name': name,
            'children': [],
            'attributes': {}}

        for k in keys:
            b['attributes'][k] = n.attrib.get(k, "")
        subs = list(n)
        if subs:
            s = getOutlineNodes(n)
            b['children'] = s
        result.append(b)
    return result


def getOPML( etRootnode ):
    global keyTypes, opmlTags, nodeTypes, urls
    
    d = {
        'head': [],
        'body':[]
        }

    # get head
    head = etRootnode.find("head")

    # get body
    body = etRootnode.find("body")
    

    if head:
        for item in list(head):
            #print "head:", item.tag, item.text
            d['head'].append( (item.tag, item.text) )

    if body:
        d['body'] = getOutlineNodes(body)

    if kwlog:
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


def opml_from_string(opml_text):
    try:
        s = etree.fromstring(opml_text)
    except StandardError, v:
        raise OPMLParseErrorException, "The OPML file could not be parsed.\n\n%s" % v
    return getOPML( s )


def parse_plist( nsurl ):
    try:
        nsdict = NSDictionary.dictionaryWithContentsOfURL_( nsurl )
    except StandardError, v:
        raise PLISTParseErrorException, "The PLIST file could not be parsed.\n\n%s" % v
    return nsdict
    

# UNUSED
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
            indentXML(elem, level+1, width)

        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


def createSubNodesOPML(OPnode, ETnode, level):
    # do attributes
    name = OPnode.name
    value = OPnode.getValueDict()
    for k, v in value.items():
        if type(v) not in (str, unicode):
            value[k] = unicode(v)
    comment = OPnode.comment

    # update attributes
    if ETnode.tag != "body":
        #d = dictFromValue( value )
        ETnode.attrib['text'] = name
        
        # don't have an empty value: tag
        if len(value) == 1:
            # if 'value' in value:
            if u'' in value:
                # value.pop('value')
                # value.pop( u'' )
                value = {}

        ETnode.attrib.update( value )
        if comment != "":
            ETnode.attrib['comment'] = comment

    if len(OPnode.children) > 0:
        
        # do children
        for child in OPnode.children:
            ETSub = etree.SubElement( ETnode, "outline")
            s = createSubNodesOPML( child, ETSub, level+1 )
    return ETnode


# -----------------------------------------------

stop = 1

def getXMLNodes( node ):
    """Read the outline nodes in XML
    """
    result = []
    for n in list(node):

        name = n.tag
        if not name:
            name = u""
        name = unicode(name)

        text = n.text
        if not text:
            text = u""
        text = unicode(text)
        fulltext = text
        #text = text.strip(u" \t\r\n")

        tail = n.tail
        if not tail:
            tail = u""
        tail = unicode(tail)
        fulltail = tail
        #tail = tail.strip(u" \t\r\n")

        if 0: #kwlog:
            if tail:
                if name == u"a":
                    print
                    print "NAME:", repr(name)
                    print "TEXT:", repr(text)
                    print "TAIL:", repr(tail)
                
        comment = False
        if name == u"<built-in function Comment>":
            name = u"COMMENT"
            comment = True
            # dont strip comments
            text = fulltext
            tail = fulltail

        b = {
            'name': name,
            'text': text,
            'tail': tail,
            'children': [],
            
            'attributes': {}}

        keys = n.attrib.keys()

        for k in keys:
            b['attributes'][k] = unicode(n.attrib.get(k, ""))

        if comment:
            b['attributes']['cactustype'] = u"comment"

        subs = list(n)
        if subs:
            s = getXMLNodes(n)
            b['children'] = s
        result.append(b)
    return result


def getXML_( etRootnode ):
    d = []
    # pdb.set_trace()
    keys = etRootnode.attrib.keys()

    b = {
        'name': unicode(etRootnode.tag),
        'text': unicode(etRootnode.text),
        'tail': unicode(etRootnode.tail),
        'children': [],
        
        'attributes': {}}

    for k in keys:
        b['attributes'][k] = etRootnode.attrib.get(k, "")
    subs = list(etRootnode)
    if subs:
        s = getXMLNodes(etRootnode)
        b['children'] = s
    d.append(b)
    return b


def getHTML_( etRootnode ):
    d = []
    # pdb.set_trace()
    docinfokeys = (
        'doctype',
        'encoding',
        'externalDTD',
        'internalDTD',
        'public_id',
        'root_name',
        'standalone',
        'system_url',
        'xml_version')
    docinfo = etRootnode.docinfo
    rootnode = etRootnode.getroot()
    keys = rootnode.attrib.keys()

    name = rootnode.tag
    if not name:
        name = u""
    name = unicode(name)

    comment = False
    if name == u"<built-in function Comment>":
        name = u"COMMENT"
        comment = True

    text = rootnode.text
    if not text:
        text = u""
    text = unicode(text)

    b = {
        'name': name,
        'text': text,
        'children': [],
        
        'attributes': {}}

    for k in keys:
        b['attributes'][k] = rootnode.attrib.get(k, "")
    if comment:
        b['attributes']['cactustype'] = u"comment"
    subs = list(rootnode)
    if subs:
        s = getXMLNodes(rootnode)
        b['children'] = s
    d.append(b)
    return b


# these should be unified
def xml_from_string(xml_text):
    # pdb.set_trace()
    try:
        s = etree.fromstring(xml_text)
    except StandardError, v:
        raise XMLParseErrorException, "The XML file could not be parsed.\n\n%s" % v
    return getXML_( s )


def html_from_url( htmlurl ):
    if isinstance(htmlurl, NSURL):
        htmlurl = str(htmlurl.absoluteString())
    parser = lxmletree.HTMLParser()
    try:
        s = lxmletree.parse(htmlurl, parser)
    except StandardError, v:
        raise HTMLParseErrorException, "The HTML file could not be parsed.\n\n%s" % v
    return getHTML_( s )


def createSubNodesXML(OPnode, ETnode, level):
    # do attributes

    attrib = OPnode.getValueDict()
    if 'cactustype' in attrib and attrib["cactustype"] == u"comment":
        ETnode.append( etree.Comment( OPnode.comment ) )
    else:
        ETnode.text = OPnode.comment
        for key in attrib:
            if key == u'tail':
                ETnode.tail = attrib[key]
            else:
                ETnode.attrib[key] = attrib[key]

        ETnode.attrib = attrib

    if len(OPnode.children) > 0:
        
        # do children
        for child in OPnode.children:
            attrib = child.getValueDict()
            ETSub = etree.SubElement( ETnode, child.name)
            s = createSubNodesXML( child, ETSub, level+1 )
    return ETnode


def reorderAttribKeys( d ):
    keys = d.keys()
    if 'name' in keys:
        keys.remove( 'name' )
        keys.insert( 0, 'name' )
    if 'content' in keys:
        keys.remove( 'content' )
        keys.append( 'content' )
    return keys    


def createSubNodesHTML(OPnode, ETnode, level, indent=0):

    attrib = OPnode.getValueDict()
    attrib_keys = reorderAttribKeys( attrib )
    
    ETnode.text = OPnode.comment
    if indent:
        ETnode.text.rstrip(u" \t\r\n")

    for key in attrib_keys:
        if key == u'tail':
            ETnode.tail = attrib[key]
        else:
            ETnode.attrib[key] = attrib[key]
    if not ETnode.tail:
        ETnode.tail = u"\n"

    if len(OPnode.children) > 0:
        # do children
        for child in OPnode.children:
            attrib = child.getValueDict()
            if 'cactustype' in attrib and attrib["cactustype"] == u"comment":
                ETSub = lxmletree.Comment( child.comment )
                ETnode.append( ETSub )
            else:
                ETSub = lxmletree.SubElement( ETnode, child.name)
                s = createSubNodesHTML( child, ETSub, level+1, indent )
    return ETnode

def generateHTML( rootNode, doctype, encoding, indent=0 ):

    baseOP = rootNode.children[0]

    # pdb.set_trace()
    rootElement = lxmletree.Element("html")
    rootElement.tail = u"\n"

    page = lxmletree.ElementTree( rootElement )

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    c = lxmletree.Comment( CactusVersion.document_creator + " on %s." % (now,))
    c.tail = u"\n"
    
    rootElement.append(c)

    rootElement.attrib.update( baseOP.getValueDict() )

    comment = baseOP.comment
    if comment:
        rootElement.text = comment

    nodes = createSubNodesHTML(baseOP, rootElement, 1, indent)

    if indent:
        indentXML(rootElement, level=0, width=indent)

    return lxml.html.tostring( page,
                               pretty_print=False,
                               include_meta_content_type=True,
                               encoding=encoding,
                               doctype=doctype)
    # return page


def generateXML( rootNode, indent=False ):
    """Generate an OPML/XML tree from OutlineNode rootNode.
    
    parameters:
     indent   - if > 0 indent with indent spaces per level
    return
     etree.Element of rootNode
    """

    #
    # WARNING: The following dereference needs to be removed if the
    #          OPML code is ever cleaned up. Currently the rootNode
    #          is invisible and attached to the document.
    #
    #          That needs to change but not for now.
    #
    #   In the case of XML there are 2 chained roots
    #
    #   Cactus OPML files ommit the <opml> element!
    #

    # ignore the opml element
    baseOP = rootNode.children[0]

    rootXML = etree.Element( baseOP.name )

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    c = etree.Comment( CactusVersion.document_creator + " on %s." % (now,))
    rootXML.append(c)

    rootXML.attrib = baseOP.getValueDict()

    # value = baseOP.getValueDict()
    if 0: #value:
        # filter out empty {'value':""} items
        if len(value)>1:
            rootXML.attrib = value
        elif len(value) == 1:
            if value.keys()[0] == u"value" and value[ u"value" ] != u"":
                rootXML.attrib = value

    comment = baseOP.comment
    if comment:
        baseOP.text = comment
    
    nodes = createSubNodesXML(baseOP, rootXML, 1)

    indentXML(rootXML)

    return rootXML

# -----------------------------------------------

def generateRSS( rootNode, indent=2 ):
    """Generate an OPML/XML tree from OutlineNode rootNode.
    
    parameters:
     filepath - unused since file writing has been factored out
     indent   - if > 0 indent with indent spaces per level
    return
     etree.Element of rootNode
    """

    valid_RSSChannel = ( "title", "link", "description", "language",
            "copyright", "managingEditor", "webMaster", "pubDate",
            "lastBuildDate", "categories", "generator", "docs",
            "cloud", "ttl", "image", "rating", "textInput",
            "skipHours", "skipDays", "items")

    valid_RSSItems = ( "title", "link", "description", "author",
            "categories", "comments", "enclosure", "guid",
            "pubDate", "source" )

    backTranslator = {
        'subtitle': 'description',
        'title': 'title',
        'published': 'pubDate',
        'id': 'guid'
    }

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    creator = "Created by Cactus v0.2.0 on %s." % (now,)

    # defaults
    head_d = {
        'title': "No Channel Title",
        'description': "No Channel description.",
        'link':  ""}

    headOP = rootNode.findFirstChildWithName_( "head" )

    if headOP:
        for headsub in headOP.children:
            name = headsub.name
            name = backTranslator.get(name, name)
            if name in valid_RSSChannel:
                value = headsub.getValueDict()
                if name == 'cloud':
                    cloud = PyRSS2Gen.Cloud(
                            value.get('domain', ""),
                            value.get('port', ""),
                            value.get('path', ""),
                            value.get('registerProcedure', ""),
                            value.get('protocol', ""))
                    head_d[ 'cloud' ] = cloud
                elif name == 'image':
                    image = PyRSS2Gen.Image(
                            value.get('href', ""),
                            value.get('title', ""),
                            value.get('link', ""),
                            value.get('width', None),
                            value.get('height', None),
                            value.get('description', None))
                    head_d[ 'image' ] = image

                else:
                    if len(value) == 1:
                        head_d[name] = value.values()[0]
                    else:
                        
                        head_d[name] = value
        print "HEAD:"
        pp(head_d)
    body_l = []
    bodyOP = rootNode.findFirstChildWithName_( "body" )

    if bodyOP:
        for bodysub in bodyOP.children:
            name = bodysub.name
            value = bodysub.getValueDict()
            d = {'title': "No Item Title",
                 'description': "No Item description."}

            for key in value:
                v = value[key]
                k = backTranslator.get(key, key)
                if k == "summary":
                    k = "description"
                if k in valid_RSSItems:

                    if k == 'enclosure':
                        url, rest = value[key].split('<<<')
                        length, type_ = rest.split(';', 1)
                        try:
                            length = int(length)
                        except ValueError, err:
                            if kwlog:
                                print "BOGUS ENCLOSURE LENGTH: %s" % repr(length)
                            length = 0
                        enc = PyRSS2Gen.Enclosure( url, length, type_)
                        d[k] = enc
                    else:
                        # TODO: check for type here; dicts and lists may be bad
                        d[ k ] = v #value[key]
                        if type(d[ k ]) in (list, dict, tuple):
                            print "\ngenerateRSS() type error.\n"
                        
            #print "ITEM:"
            #pp( d )
            body_l.append( PyRSS2Gen.RSSItem( **d ) )

    head_d[ 'items' ] = body_l

    rss = PyRSS2Gen.RSS2( **head_d )
    f = cStringIO.StringIO()
    rss.write_xml( f, encoding='utf-8')
    s = f.getvalue()
    f.close()
    return s


def serializePLISTOutline_( rootNode ):
    nsdict = generatePLISTDict_( rootNode )
    p = "/tmp/tmp.plist"
    ok = nsdict.writeToFile_atomically_(p, True)
    if ok:
        f = open( p, 'rb')
        s = f.read()
        f.close()
        data = NSData.dataWithBytes_length_(s, len(s) )
        return data
    return False


def generatePLISTDict_( rootNode ):
    plist = NSMutableDictionary.dictionaryWithCapacity_(rootNode.noOfChildren())
    
    for child in rootNode.children:
        attrs = child.getValueDict()
        name = child.name
        cactusType = attrs.get( 'cactusNodeType', None)
        immediateValue = unicode(child.comment)
        if cactusType == 'bool':
            plist[ name ] = False
            if immediateValue != u"False":
                plist[ name ] = True
        elif cactusType == 'number':
            if '.' in str(immediateValue):
                plist[ name ] = NSNumber.numberWithFloat_( float(immediateValue) )
            else:
                # plist[ name ] = long(immediateValue)
                plist[ name ] = NSNumber.numberWithLongLong_( long(immediateValue) )
        elif cactusType == 'string':
            plist[ name ] = immediateValue
        elif cactusType == 'data':
            s = binascii.unhexlify(immediateValue)
            l = len(s)
            plist[ name ] = NSData.dataWithBytes_length_(s, l)
        elif cactusType == 'list':
            plist[ name ] = generatePLISTArray_( child )
        elif cactusType == 'dictionary':
            plist[ name ] = generatePLISTDict_( child )
    return plist


def generatePLISTArray_( rootNode ):
    plist = NSMutableArray.arrayWithCapacity_(rootNode.noOfChildren())
    
    for child in rootNode.children:
        attrs = child.getValueDict()
        name = child.name
        cactusType = attrs.get( 'cactusNodeType', None)
        immediateValue = unicode(child.comment)
        if cactusType == 'bool':
            b = False
            if immediateValue != u"False":
                b = True
            plist.append( b )
        elif cactusType == 'number':
            if '.' in str(immediateValue):
                plist.append( float(immediateValue) )
            else:
                plist.append( long(immediateValue) )
        elif cactusType == 'string':
            plist.append( immediateValue )
        elif cactusType == 'data':
            s = binascii.unhexlify(immediateValue)
            l = len(s)
            plist.append( NSData.dataWithBytes_length_(s, l) )
        elif cactusType == 'list':
            plist.append( generatePLISTArray_( child ) )
        elif cactusType == 'dictionary':
            plist.append( generatePLISTDict_( child ) )
    return plist

    
def generateOPML( rootNode, indent=2, expansion={} ):
    """Generate an OPML/XML tree from OutlineNode rootNode.
    
    parameters:
     filepath - unused since file writing has been factored out
     indent   - if > 0 indent with indent spaces per level
     expansion- a string that will be the value of head.expansionState 

    return
     etree.Element of rootNode
    """

    rootOPML = etree.Element("opml")
    rootOPML.attrib["version"] = "2.0"

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    c = etree.Comment( CactusVersion.document_creator + " on %s." % (now,))
    rootOPML.append(c)

    headOP = rootNode.findFirstChildWithName_( "head" )

    head = etree.SubElement(rootOPML, "head")

    expandCreated = set()
    if headOP:
        for headsub in headOP.children:
            name = headsub.name
            value = headsub.getValueDict()
            comment = headsub.comment
            v = ""

            if name in expansion:
                value = { u"": unicode(expansion[name]) }
                expandCreated.add(name)

            node = etree.SubElement( head, name)

            if value: # != "":
                v = value[ value.keys()[0] ]

                # node.text = value
                # node.text = unicode(value.get('value', ''))

                # node.text = unicode(value.get( u'', ''))
                node.text = unicode(v)
            
            if comment != "":
                node.attrib["comment"] = comment
            print "HEAD: '%s': '%s' " % (repr(name), repr(v))
        # add missing keys
        if expansion:
            for key in expansion:
                if key not in expandCreated:
                    node = etree.SubElement( head, key)
                    node.text = unicode(expansion[key])
                
    else:
        # create generic head here
        if expansion:
            for key in expansion:
                if key not in expandCreated:
                    node = etree.SubElement( head, key)
                    node.text = unicode(expansion[key])

    body = etree.SubElement(rootOPML, "body")
    bodyOP = rootNode.findFirstChildWithName_( "body" )

    try:
        if bodyOP:
            nodes = createSubNodesOPML(bodyOP, body, 1)
        else:
            # an outline without body
            nodes = createSubNodesOPML(rootNode, body, 1)
    except Exception, err:
        # pdb.set_trace()
        tb = unicode(traceback.format_exc())
        print tb
        print 

    if indent:
        # pdb.set_trace()
        indentXML(rootOPML, 0, indent)

    return rootOPML


def photo_from_string( photo_text ):
    return getPhotoXML( etree.fromstring(photo_text) )


def getPhotoXML( rootNode ):

    title = description = whenUploaded = whenArchived = license = urlFolder = ""

    node = rootNode.find("title")
    if node != None:
        title = node.text

    node = rootNode.find("description")
    if node != None:
        description = node.text

    node = rootNode.find("whenUploaded")
    if node != None:
        whenUploaded = node.text

    node = rootNode.find("whenArchived")
    if node != None:
        whenArchived = node.text

    node = rootNode.find("license")
    if node != None:
        license = node.text

    node = rootNode.find("urlFolder")
    if node != None:
        urlFolder = node.text

    sizes = rootNode.find("sizes")

    picts = {}

    picture = {
        'title': title,
        'urlFolder': urlFolder,
        'description': description,
        'whenUploaded': whenUploaded,
        'whenArchived': whenArchived,
        'license': license,
        'sizes': []
    }

    sortedSizes = []

    if urlFolder:
        for i, size in enumerate(list(sizes)):
            picture['sizes'].append(size.attrib)

            maxWH = max(int(size.attrib.get('width', 0)),
                        int(size.attrib.get('height', 0)) )

            sortedSizes.append( (maxWH, i) )

            if 'fname' in size.attrib:
                name = size.attrib['fname']
                url = urlFolder + name
                picts[ name ] = url

    sortedSizes.sort()
    sortedSizes.reverse()
    picture['sortedSizes'] = sortedSizes
    return picture
