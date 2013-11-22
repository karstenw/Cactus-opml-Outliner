
# -*- coding: utf-8 -*-


"""
"""

import sys
import os

import binascii

import traceback

import pdb
import pprint
pp = pprint.pprint
kwdbg = False
kwlog = True

import time

import feedparser

import objc

import AppKit
NSString = AppKit.NSString
NSMutableString = AppKit.NSMutableString
NSUserDefaults = AppKit.NSUserDefaults

import CactusTools
num2ostype = CactusTools.num2ostype
ostype2num = CactusTools.ostype2num

import CactusVersion

import outlinetypes
typeOutline = outlinetypes.typeOutline
typeTable = outlinetypes.typeTable
typeBrowser = outlinetypes.typeBrowser

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType
CactusPLISTType = CactusDocumentTypes.CactusPLISTType
CactusIMLType = CactusDocumentTypes.CactusIMLType

import CactusTools
NSURL2str = CactusTools.NSURL2str

import CactusOutlineNode
OutlineNode = CactusOutlineNode.OutlineNode



def openOPML_(rootOPML):
    if kwlog:
        print "openOPML_()"
    return openOPML_withURLTag_(rootOPML, False)

def openOPML_withURLTag_(rootOPML, urltag):
    if kwlog:
        print "CactusFileOpeners.openOPML_withURLTag_()"
    """This builds the node tree and returns the root node."""
    #
    #  Split this up.
    def getChildrenforNode(node, children, root):
        for c in children:
            name = c.get('name', '')
            childs = c.get('children', [])
            content = c.get('attributes', "")
            comment = ""
            if content == "":
                content = {u'value': ""}
            content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    if k == "comment":
                        comment = v
                    else:
                        l.append( (k, v) )
                content = l
            else:
                content = u""

            newnode = OutlineNode(name, content, node, typeOutline, root)
            if comment:
                newnode.setComment_( comment )
            node.addChild_( newnode )
            if len(childs) > 0:
                getChildrenforNode(newnode, childs, root)

    ######

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    # get opml head section
    if rootOPML['head']:

        # the outline head node
        head = OutlineNode("head", "", root, typeOutline, root)
        root.addChild_( head )
        headtags = set()
        for headnode in rootOPML['head']:
            k, v = headnode
            headtags.add( k )
            head.addChild_( OutlineNode(k, v, head, typeOutline, root) )

        if urltag:
            if 'cactusUrl' not in headtags:
                # add this url only once, not for every open
                head.addChild_(OutlineNode('cactusUrl', unicode(urltag), head, typeOutline, root))
    # fill in missing opml attributes here
    # created, modified
    #
    # how to propagate expansionstate, windowState?
    # make a document object and pass that to docdelegate?
    #
    # get opml body section
    if rootOPML['body']:
        # pdb.set_trace()
        # the outline body node
        body = OutlineNode("body", "", root, typeOutline, root)
        root.addChild_( body )

        for item in rootOPML['body']:
            name = item['name']
            children = item['children']
            comment = ""


            # make table here
            content = item.get('attributes', "")
            content.pop('text', None)
            if content:
                l = []
                for k, v in content.items():
                    if k == "comment":
                        comment = v
                    else:
                        l.append( (k, v) )
                content = l
            else:
                content = u""

            node = OutlineNode(name, content, body, typeOutline, root)
            if comment:
                node.setComment_( comment )
            # node.setValue_(content)
            body.addChild_( node )
            if len(children) > 0:
                try:
                    getChildrenforNode( node, children, root )
                except Exception, err:
                    print err
                    # pdb.set_trace()
                    pp(children)
                    pp(item)
    #title = os
    return root, CactusOPMLType

def openXML_( rootXML):

    if kwlog:
        s = repr(rootXML)
        if len(s) > 90:
            s = s[:91]
        print "openXML_( %s )" % s

    """This builds the node tree and returns the root node."""

    #
    #  Split this up.
    def getChildrenforNode(node, children, root):
        for c in children:
            name = c.get('name', '')
            tail = c.get('tail', '')
            childs = c.get('children', [])
            content = c.get('attributes', "")
            txt = c.get('text', "")

            if content == "":
                content = {u'': ""}

            if content or tail:
                l = []
                for k, v in content.items():
                    l.append( (k, v) )
                if tail != u"":
                    l.append( (u'tail', tail) )
                content = l
            else:
                content = u""

            try:
                newnode = OutlineNode(name, content, node, typeOutline, root)
            except Exception, err:
                print "\n\nERROR in openXML_()"
                tb = unicode(traceback.format_exc())
                print err
                print
                print tb
                print

            if txt != "":
                newnode.setComment_( txt )

            node.addChild_( newnode )
            try:
                n = len(childs)
            except Exception, err:
                print
                # pdb.set_trace()
                print err
            if len(childs) > 0:
                getChildrenforNode(newnode, childs, root)
            newnode.release()
            del newnode

    ######

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    rootXML = rootXML
    name = rootXML['name']
    children = rootXML['children']
    content = rootXML.get('attributes', "")
    txt = rootXML.get('text', "")

    if content:
        l = []
        for k, v in content.items():
            l.append( (k, v) )
        content = l
    else:
        content = u""

    node = OutlineNode(name, content, root, typeOutline, root)
    if txt:
        node.setComment_( txt )

    root.addChild_( node )

    try:
        n = len(children)
    except Exception, err:
        print "CactusFileOpeners.openXML_() ERROR"
        print "childen has no length attribute!"
        print type(children)
        # pdb.set_trace()
        print err


    if n > 0:
        try:
            getChildrenforNode( node, children, root )
        except Exception, err:
            print "\n\nERROR in openXML_()"
            tb = unicode(traceback.format_exc())
            print err
            print
            print tb
            print
            # pp(children)
    #title = os
    return root, CactusXMLType


def openRSS_(url):

    url = NSURL2str(url)

    if kwlog:
        s = repr(url)
        if len(s) > 90:
            s = s[:91]
        print "openRSS_( %s )" % repr(s)
    d = feedparser.parse( url, agent=CactusVersion.user_agent )

    # make basic nodes
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    head = OutlineNode("head", "", root, typeOutline, root)
    root.addChild_( head )

    body = OutlineNode("body", "", root, typeOutline, root)
    root.addChild_( body )

    #
    # head
    #

    # feed = docs, generator, language, link, microblog_archive,
    # microblog_endday, microblog_filename, microblog_startday, microblog_url,
    # published, subtitle, title, updated, cloud
    if d.feed:
        keys = """author authors category comments cloud description docs enclosure generator
                  generator_detail guid image language link links microblog_archive
                  microblog_endday microblog_filename microblog_startday
                  microblog_url published pubDate source subtitle subtitle_detail
                  sy_updatefrequency sy_updateperiod title title_detail updated
                  updated_parsed""".split()

        feedkeys = d.feed.keys()
        feedkeys.sort()

        for k in feedkeys:

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
                    l = []
                    for key, val in v.items():
                        l.append( (key,val) )
                    v = l
                elif type(v) == time.struct_time:
                    v = time.asctime(v)
                else:
                    # if k in ('',)
                    if 1:
                        print "ATTENTION RSS Head values"
                        print "KEY:", k
                        print "TYPE:", type(v)
                        print "REPR:", repr(v)
                        print
                    v = repr(v)
            node = OutlineNode(k, v, head, typeOutline, root)
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
        node = OutlineNode(k, v, head, typeOutline, root)
        head.addChild_( node )

    if 0:
        # encoding
        if 'encoding' in d:
            node = OutlineNode('encoding', d.encoding, head, typeOutline, root)
            head.addChild_( node )

        # bozo
        if 'bozo' in d:
            node = OutlineNode('bozo', str(d.bozo), head, typeOutline, root)
            head.addChild_( node )

        # etag
        if 'etag' in d:
            node = OutlineNode('etag', d.etag, head, typeOutline, root)
            head.addChild_( node )

        # headers dict
        if 'headers' in d:
            node = OutlineNode('headers', d.headers, head, typeOutline, root)
            head.addChild_( node )

        # href
        if 'href' in d:
            node = OutlineNode('href', d.href, head, typeOutline, root)
            head.addChild_( node )

        # namespaces
        if 'namespaces' in d:
            # pdb.set_trace()
            node = OutlineNode('namespaces', d.namespaces, head, typeOutline, root)
            head.addChild_( node )

        # version
        if 'version' in d:
            node = OutlineNode('version', d.version, head, typeOutline, root)
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

        # extract enclosure
        if 'links' in value:
            links = value['links']
            for link in links:
                rel = link.get('rel', False)
                if rel == 'enclosure':
                    s = "%s<<<%s;%s" % (link.get('url',''),
                                        str(link.get('length','')),
                                        link.get('type', ""))
                    value['enclosure'] = s
        for k in killkeys:
            value.pop( k, None )

        node = OutlineNode(name, value, body, typeOutline, root)
        body.addChild_( node )
    return root, CactusRSSType


def getPLISTValue(nsvalue):
    valueType = type(nsvalue)
    value = ""
    valueTypeName = ""
    if valueType == bool:
        # print "BOOLVALUE: '%s' --> '%s'" % (repr(nsvalue), repr(bool(nsvalue)) )
        value = repr(bool(nsvalue))
        valueTypeName = [ ('cactusNodeType', "bool") ]

    # number
    elif hasattr(nsvalue, "descriptionWithLocale_"):
        value = unicode(nsvalue.descriptionWithLocale_( None ))
        valueTypeName = [ ('cactusNodeType', "number") ]

    # data
    elif hasattr(nsvalue, "bytes"):
        value = unicode( binascii.hexlify(nsvalue.bytes()) )
        valueTypeName = [ ('cactusNodeType', "data") ]

    # anything else
    elif hasattr(nsvalue, "description"):
        value = unicode(nsvalue.description())
        valueTypeName = [ ('cactusNodeType', "string") ]
    else:
        print "BOGATIVE VALUE TYPE:", repr(valueType)
        #pdb.set_trace()
        print
    return value, valueTypeName


#
cactusBool = [ ('cactusNodeType', "bool") ]
cactusString = [ ('cactusNodeType', "string") ]
cactusNumber = [ ('cactusNodeType', "number") ]
cactusDictionary = [ ('cactusNodeType', "dictionary") ]
cactusData = [ ('cactusNodeType', "data") ]


def openIML_( nsdict ):
    if kwlog:
        s = repr(nsdict)
        if len(s) > 90:
            s = s[:91]
        print "openPLIST_( %s )" % s

    """This builds the node tree and returns the root node."""

    ######

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    progressCount = 0

    def getTracks( nsdict, parent ):
        # pdb.set_trace()
        i = 0
        id_trackname = {}
        for trackItem in nsdict:
            trackData = nsdict.objectForKey_( trackItem )
            trackNode = OutlineNode("", "", parent, typeOutline, root)
            trackAttributes = []
            trackName = ""
            trackAlbum = ""
            trackArtist = ""
            trackID = ""
            for trackAttribute in trackData:
                nsvalue = trackData.objectForKey_( trackAttribute )
                value, valueType = getPLISTValue( nsvalue)

                if trackAttribute == u"Track ID":
                    trackID = value

                elif trackAttribute == u"Name":
                    trackName = value

                elif trackAttribute == u"Album":
                    trackAlbum = value

                elif trackAttribute in (u"File Creator", u"File Type"):
                    value = num2ostype( long(value) )

                elif trackAttribute == u"Total Time":
                    # formatted duration hack
                    secondsTotal = int(value) / 1000.0
                    minutes = secondsTotal // 60
                    seconds = round(secondsTotal % 60, 1)
                    seconds = "0%.1f" % seconds
                    value = u"%i:%s" % (minutes, seconds[-4:])

                trackAttributes.append( (trackAttribute, value) )
                id_trackname[ trackID ] = trackName

            # itemName = u"%s - %s" % (trackAlbum, trackName)
            itemName = trackName

            # print repr(itemName)
            trackNode.setName_( itemName )
            trackNode.setValue_( trackAttributes )
            trackNode.setMaxLineHeight()
            parent.addChild_( trackNode )
            i += 1
            if i % 1000 == 0:
                sys.stdout.write('.')
                sys.stdout.flush()
                if i % 100000 == 0:
                    sys.stdout.write('\n')
                    sys.stdout.flush()
        print
        print "%i Tracks." % i
        return id_trackname

    def makePlaylistNode( name, curPlaylist, value, parent, root, type_):
        if name in curPlaylist:

            if type_ == cactusData:
                value = unicode( binascii.hexlify(value.bytes()) )
            elif type_ == cactusBool:
                value = repr(bool(value))
            elif type_ == cactusNumber:
                value = unicode(value.descriptionWithLocale_( None ))
            # elif type_ == cactusDictionary:

            node = OutlineNode( name,
                                type_,
                                parent,
                                typeOutline,
                                root)
            if value != "":
                node.setComment_( unicode(value) )
            parent.addChild_( node )
            return node

    def getPlaylists( nsdict, parent, id_track_dict ):
        # pdb.set_trace()

        defaults = NSUserDefaults.standardUserDefaults()
        optIMLImportSystemLibraries = defaults.objectForKey_( u'optIMLImportSystemLibraries')
        systemLibraries = (
            u"Library",
            u"Music",
            u"Movies",
            u"Podcasts",
            u"iTunes U",
            u"Books")

        root = parent.rootNode
        # add the standard playlist attributes
        i = 0
        for playlist in nsdict:

            #
            # check for keys not listed here
            #

            playlistName = playlist.get( u"Name", "")

            playlistNode = OutlineNode( playlistName, "", parent, typeOutline, root)
            parent.addChild_( playlistNode )

            # drop out if AllItems pref is false
            if playlistName in systemLibraries:
                if not optIMLImportSystemLibraries:
                    continue

            makePlaylistNode( u"Name", playlist,
                              playlistName,
                              playlistNode, root, cactusString)

            makePlaylistNode( u"Master", playlist,
                              playlist.get( u"Master", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Playlist ID", playlist,
                              playlist.get( u"Playlist ID", "0"),
                              playlistNode, root, cactusNumber)

            makePlaylistNode( u"Playlist Persistent ID", playlist,
                              playlist.get( u"Playlist Persistent ID", ""),
                              playlistNode, root, cactusString)

            makePlaylistNode( u"Parent Persistent ID", playlist,
                              playlist.get( u"Playlist Persistent ID", ""),
                              playlistNode, root, cactusString)

            makePlaylistNode( u"Distinguished Kind", playlist,
                              playlist.get( u"Distinguished Kind", 0),
                              playlistNode, root, cactusNumber)

            makePlaylistNode( u"Movies", playlist,
                              playlist.get( u"Movies", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Podcasts", playlist,
                              playlist.get( u"Podcasts", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"iTunesU", playlist,
                              playlist.get( u"iTunesU", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Audiobooks", playlist,
                              playlist.get( u"Audiobooks", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Smart Info", playlist,
                              playlist.get( u"Smart Info", ""),
                              playlistNode, root, cactusData)

            makePlaylistNode( u"Smart Criteria", playlist,
                              playlist.get( u"Smart Criteria", ""),
                              playlistNode, root, cactusData)

            makePlaylistNode( u"Visible", playlist,
                              playlist.get( u"Visible", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"All Items", playlist,
                              playlist.get( u"All Items", "False"),
                              playlistNode, root, cactusBool)

            makePlaylistNode( u"Folder", playlist,
                              playlist.get( u"Folder", "False"),
                              playlistNode, root, cactusBool)

            plnode = makePlaylistNode( u"Playlist Items", playlist,
                                       "",
                                       playlistNode, root, cactusDictionary)

            i += 7
            j = 0

            if not u"Playlist Items" in playlist:
                continue

            for item in playlist[ u"Playlist Items" ]:
                id_ = item[u"Track ID"]
                attrs = {
                    u"Track ID": id_
                }

                name = id_track_dict.get(unicode(id_), "###Noname###")

                node = OutlineNode( name, attrs, plnode, typeOutline, root)
                plnode.addChild_( node )

                i += 1
                j += 1
                if i % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    if i % 100000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
            print
            print "%s has %i Playlist Items." % (repr(playlistName), j)
        print
        print "A total of %i Playlist Items." % i


    def dispatchLevel( nsdict, parent, root, progressCount ):
        # array or dict
        i = 0
        selfTypeName = "None"
        if hasattr(nsdict, "objectForKey_"):
            selfTypeName = "dictionary"
        elif hasattr(nsdict, "objectAtIndex_"):
            selfTypeName = "list"

        selfType = [ ('cactusNodeType', selfTypeName) ]

        parent.setValue_( selfType )

        id_track_dict = {}
        for key in nsdict:
            i += 1

            typeAttribute = ""
            value = ""

            if selfTypeName == "list":
                itemName = str(i)
                nsvalue = nsdict.objectAtIndex_( i-1 )
            else:
                itemName = unicode(key)
                nsvalue = nsdict.objectForKey_(key)

            valueType = type(nsvalue)

            node = OutlineNode(itemName, "", parent, typeOutline, root)

            if itemName == u"Tracks":
                id_track_dict = getTracks( nsvalue, node )
            elif itemName == u"Playlists":
                getPlaylists( nsvalue, node, id_track_dict )
            else:
                # dict
                if hasattr(nsvalue, "objectForKey_"):
                    progressCount = dispatchLevel(nsvalue, node, root, progressCount)

                # list
                elif hasattr(nsvalue, "objectAtIndex_"):
                    progressCount = dispatchLevel(nsvalue, node, root, progressCount)

                else:
                    value, valueType = getPLISTValue( nsvalue )
                    node.setValue_( valueType )
            node.setComment_( value )
            parent.addChild_(node)
            progressCount += 1
            if kwlog:
                if progressCount % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    if progressCount % 100000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
        return progressCount

    dispatchLevel(nsdict, root, root, progressCount)
    return root, CactusIMLType

###
#
# plist tools
#
###

def openPLIST_( nsdict ):

    if kwlog:
        s = repr(nsdict)
        if len(s) > 90:
            s = s[:91]
        print "openPLIST_( %s )" % s

    """This builds the node tree and returns the root node."""

    ######

    # check for itunes xml file
    defaults = NSUserDefaults.standardUserDefaults()
    optIMLAutodetect = defaults.objectForKey_( u'optIMLAutodetect')

    if optIMLAutodetect:
        isIML = True
        for key in (u"Music Folder", u"Application Version",
                    u"Tracks", u"Playlists",
                    u"Minor Version", u"Major Version"):
            if key not in nsdict:
                isIML = False
                break
        if isIML:
            return openIML_( nsdict )

    # root node for document; never visible,
    # always outline type (even for tables)
    root = OutlineNode("__ROOT__", "", None, typeOutline, None)

    progressCount = 0

    def dispatchLevel( nsdict, parent, root, progressCount ):
        # array or dict
        i = 0

        if hasattr(nsdict, "objectForKey_"):
            selfTypeName = "dictionary"
        elif hasattr(nsdict, "objectAtIndex_"):
            selfTypeName = "list"
        else:
            selfTypeName = "None"
        selfType = [ ('cactusNodeType', selfTypeName) ]

        parent.setValue_( selfType )

        for key in nsdict:
            i += 1

            typeAttribute = ""
            value = ""

            if selfTypeName == "list":
                itemName = str(i)
                nsvalue = nsdict.objectAtIndex_( i-1 )
            else:
                itemName = unicode(key)
                nsvalue = nsdict.objectForKey_(key)

            valueType = type(nsvalue)

            node = OutlineNode(itemName, "", parent, typeOutline, root)

            if valueType == bool:
                # print "BOOLVALUE: '%s' --> '%s'" % (repr(nsvalue), repr(bool(nsvalue)) )
                value = repr(bool(nsvalue))
                node.setValue_( [ ('cactusNodeType', "bool") ] )

            # dict
            elif hasattr(nsvalue, "objectForKey_"):
                dispatchLevel(nsvalue, node, root, progressCount)

            # list
            elif hasattr(nsvalue, "objectAtIndex_"):
                dispatchLevel(nsvalue, node, root, progressCount)

            # number
            elif hasattr(nsvalue, "descriptionWithLocale_"):
                value = unicode(nsvalue.descriptionWithLocale_( None ))
                node.setValue_( [ ('cactusNodeType', "number") ] )

            # data
            elif hasattr(nsvalue, "bytes"):
                # pdb.set_trace()
                value = unicode( binascii.hexlify(nsvalue.bytes()) )
                node.setValue_( [ ('cactusNodeType', "data") ] )

            # anything else
            elif hasattr(nsvalue, "description"):
                value = unicode(nsvalue.description())
                node.setValue_( [ ('cactusNodeType', "string") ] )
            else:
                print "BOGATIVE VALUE TYPE:", repr(valueType)
                #pdb.set_trace()
                print

            node.setComment_( value )
            parent.addChild_(node)
            progressCount += 1
            if kwlog:
                if progressCount % 1000 == 0:
                    sys.stdout.write('.')
                    sys.stdout.flush()
                    if progressCount % 100000 == 0:
                        sys.stdout.write('\n')
                        sys.stdout.flush()
    dispatchLevel(nsdict, root, root, progressCount)
    return root, CactusPLISTType
