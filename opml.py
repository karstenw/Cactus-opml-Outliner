# -*- coding: utf-8 -*-

import os
import datetime

import xml.etree.cElementTree
etree = xml.etree.cElementTree

import cStringIO

import PyRSS2Gen

import pprint
pp = pprint.pprint

kwdbg = True
kwlog = False
import pdb



import CactusVersion

import CactusExceptions
OPMLParseErrorException = CactusExceptions.OPMLParseErrorException

# some globals for opml analyzing
keyTypes = {}
opmlTags = {}
nodeTypes = {}
urls = {}


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
            'noofchildren': nchild,
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
        raise OPMLParseErrorException, "The OPML file could not be parsed."
    return getOPML( s )


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
        'summary': 'description',
        'title': 'title',
        'published': 'pubDate',
        'id': 'guid'
    }

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    creator = "Created by Cactus v0.2.0 on %s." % (now,)

    head_d = {
        'title': "No Channel Title",
        'description': "No Channel description.",
        'link':  ""}


    headOP = rootNode.findFirstChildWithName_( "head" )

    if headOP:
        for headsub in headOP.children:
            name = headsub.name
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
                else:
                    if len(value) == 1:
                        head_d[name] = value.values()[0]
                    else:
                        head_d[name] = value
        print "HEAD:"
        pp(head_d)
    body_l = []
    bodyOP = rootNode.findFirstChildWithName_( "body" )

    # pdb.set_trace()

    if bodyOP:
        # pdb.set_trace()
        for bodysub in bodyOP.children:
            name = bodysub.name
            value = bodysub.getValueDict()
            d = {
                'title': "No Item Title",
                'description': "No Item description."}

            for key in value:
                k = backTranslator.get(key, key)
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
                        d[ k ] = value[key]
            print "ITEM:"
            pp( d )
            body_l.append( PyRSS2Gen.RSSItem( **d ) )

    head_d[ 'items' ] = body_l

    # pdb.set_trace()

    rss = PyRSS2Gen.RSS2( **head_d )
    f = cStringIO.StringIO()
    rss.write_xml( f, encoding='utf-8')
    s = f.getvalue()
    f.close()
    return s


def generateOPML( rootNode, indent=2 ):
    """Generate an OPML/XML tree from OutlineNode rootNode.
    
    parameters:
     filepath - unused since file writing has been factored out
     indent   - if > 0 indent with indent spaces per level
    return
     etree.Element of rootNode
    """
    # pdb.set_trace()

    rootOPML = etree.Element("opml")
    rootOPML.attrib["version"] = "2.0"

    now = str(datetime.datetime.now())
    now = now[:19]
    now = now.replace(" ", "_")

    c = etree.Comment( CactusVersion.document_creator + " on %s." % (now,))
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
                node.text = unicode(value.get('value', ''))
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


def photo_from_string( photo_text ):
    return getPhotoXML( etree.fromstring(photo_text) )


def getPhotoXML( rootNode ):
    # pdb.set_trace()
    title = rootNode.find("title")
    title = title.text

    description = rootNode.find("description")
    description = description.text

    whenUploaded = rootNode.find("whenUploaded")
    whenArchived = rootNode.find("whenArchived")
    license = rootNode.find("license")

    urlFolder = rootNode.find("urlFolder")
    urlFolder = urlFolder.text

    sizes = rootNode.find("sizes")
    picts = {}
    if urlFolder:
        for size in list(sizes):
            attr = size.attrib.keys()
            if 'fname' in attr:
                name = size.attrib['fname']
                url = urlFolder + name
                picts[ name ] = url
    return picts
