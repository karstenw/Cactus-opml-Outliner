
# -*- coding: utf-8 -*-


"""Some tools which are needed by most files.
"""

import sys
import os

import traceback

import time
import datetime
import unicodedata

import struct

import mactypes
import appscript
asc = appscript
import Finder10

import CactusVersion
kwdbg = CactusVersion.developmentversion
kwlog = CactusVersion.developmentversion

import pdb

import re
import requests
import urllib
import urllib2
import urlparse
import StringIO
import gzip

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType
CactusPLISTType = CactusDocumentTypes.CactusPLISTType
CactusIMLType = CactusDocumentTypes.CactusIMLType

CactusDocumentTypesSet = CactusDocumentTypes.CactusDocumentTypesSet
CactusDocumentXMLBasedTypesSet = CactusDocumentTypes.CactusDocumentXMLBasedTypesSet

import CactusXMLProperties
re_bogusCharacters = CactusXMLProperties.re_bogusCharacters

import feedparser

import objc

import Foundation
NSURL = Foundation.NSURL
NSFileManager = Foundation.NSFileManager
NSUserDefaults = Foundation.NSUserDefaults
NSString = Foundation.NSString

import AppKit
NSOpenPanel = AppKit.NSOpenPanel
NSAlert = AppKit.NSAlert
NSSavePanel = AppKit.NSSavePanel
NSFileHandlingPanelOKButton  = AppKit.NSFileHandlingPanelOKButton



#
# tools
#

def num2ostype( num ):
    if num == 0:
        return '????'
    s = struct.pack(">I", num)
    return makeunicode(s, "macroman")


def ostype2num( ostype ):
    return struct.pack('BBBB', list(ostype))


def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    try:
        if type(s) not in (unicode, objc.pyobjc_unicode):
            s = unicode(s, srcencoding)
    except TypeError:
        print "makeunicode type conversion error"
        print "FAILED converting", type(s), "to unicode"
    s = unicodedata.normalize(normalizer, s)
    return s




def detectFileTypeAtURL( nsfileurl ):
    """Not yet sure how to autodetect without reading some files twice.

    So far the parsers used are:
        OPML: cElementTree (opens string)
        RSS: feedparser (opens string)
        XML: cElementTree (opens string)
        HTML: lxml (opens URL)
        PLIST: NSDictionary.dictionaryWithContentsOfURL_ (opens URL)
    """
    pass


def detectFileTypeLocalFile( path ):
    # this needs to be checked against the binary string
    xmlre = re.compile( r'''^<?xml\s+version\s*="1.0"\s+encoding\s*=\s*"''' )




def readURL( nsurl, type_="" ):
    """Read a file. May be local, may be http"""
    url = NSURL2str(nsurl)
    if kwlog:
        print "CactusTools.readURL( '%s', '%s' )" % (url, type_)


    translateType = {
        CactusOPMLType: "opml",
        CactusHTMLType: "html",
        CactusXMLType: "xml",
        CactusRSSType: "rss",
        CactusPLISTType: "plist",
        CactusIMLType: "xml"
    }

    fileext = translateType.get( type_, ".bin")

    defaults = NSUserDefaults.standardUserDefaults()
    cache = False
    try:
        cache = bool(defaults.objectForKey_( u'optCache'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)
    
    # pdb.set_trace()
    
    if cache:
        if not nsurl.isFileURL():
            nsurl = cache_url(nsurl, fileext)

    url = NSURL2str(nsurl)

    if 0:
        # does not work with file urls
        r = requests.get( url )
        s = r.content
        headers = r.headers
        r.close()
    else:
        # fob = feedparser._open_resource(url, None, None, CactusVersion.user_agent, None, [], {})
        fob = feedparser._open_resource(url, None, None, None, None, [], {})
        s = fob.read()
        fob.close()

    # check for gzip compressed opml file
    # pdb.set_trace()
    try:
        if len(s) > 2:
            if ord(s[0]) == 0x1f:
                if ord(s[1]) == 0x8b:
                    unzipped = gzip.GzipFile( fileobj=StringIO.StringIO(s) ).read()
                    s = unzipped
    except Exception:
        pass

    if type_ == CactusOPMLType:
        # this is a quick & dirty approach and should be applied much more carefully
        # than it is now... perhaps those errors get corrected and <directivecache>
        # will be a propper node.

        # clean up bogative xml declaration. OPML-Editor, I'm looking at you...
        if s.startswith("""<?xml encoding="ISO-8859-1" version="1.0"?>"""):
            s = s.replace("""<?xml encoding="ISO-8859-1" version="1.0"?>""",
                          """<?xml version="1.0" encoding="ISO-8859-1"?>""")

            if kwlog:
                print "\nBOGUS XML DELARATION REPLACED\n"

        # this error occurs up until now only combined with the previous one
        if "<directiveCache>" in s:
            s = s.replace( "<directiveCache>", "</outline>")
            if kwlog:
                print "\nBOGUS <directiveCache> XML TAG REPLACED\n"

        #
        # opmleditor rules error
        #
        startrule = """text="&lt;rules <"""
        endrule = """&gt;">"""

        if startrule in s:
            n = s.count(startrule)
            if kwlog:
                print "BOGUS OPML RULE SECTION: %i SUBSTITUTIONS" % n
            idx = s1 = s2 = 0
            for i in range(1, n+1):
                # get location o next start- ans endrule
                s1 = s.find( startrule,s2 )
                s2 = s.find( endrule, s1 )
                s2 = s2 + len(endrule)

                # save stuff before, location and after bogative rule
                pre = s[:s1]
                defectiveSnippet = s[s1:s2]
                post = s[s2:]

                if kwlog:
                    print "\nOLD", repr(defectiveSnippet)

                # clear out false markers
                defectiveSnippet = defectiveSnippet.replace( startrule, "<")
                defectiveSnippet = defectiveSnippet.replace( endrule, "")

                defectiveSnippet = defectiveSnippet.replace( '<', "&lt;")
                defectiveSnippet = defectiveSnippet.replace( '>', "&gt;")
                defectiveSnippet = defectiveSnippet.replace( '"', "&quot;")

                # restore start and end
                defectiveSnippet = 'text="' + defectiveSnippet + '">'

                # advance pointer
                s2 = len(pre) + len(defectiveSnippet)

                # restore s
                s = pre + defectiveSnippet + post

                if kwlog:
                    print "\nNEW", repr(defectiveSnippet)

    if type_ in CactusDocumentXMLBasedTypesSet:
        # this apllies to all since cactus currently only reads xml files
        if s.startswith("<?xml ") or s.startswith("<opml") or s.startswith("<rss"):
            re_bogusCharacters = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')

            # TBD: perhaps an effort to preserve the replaced character should be made here
            # use urlescape
            t = re.sub( re_bogusCharacters, "???", s)
            if s != t:
                print "Bogus characters in XML..."
            s = t
    return s


# UNUSED
def classifyAndReadUrl( url ):
    """TBD

    Read in an URL and try to classify it as opml, bogative opml, rss, xml.
    """

    s = readURL( url )

    # check for bogative OPML editor xml declaration
    bogus = re.compile( """<?xml encoding=["']ISO-8859-1["'] version=["']1.0["']?>""" )
    if s.startswith("""<?xml encoding="ISO-8859-1" version="1.0"?>"""):
        pass


    # the type should be determinable within the first 250 bytes
    checkpart = s[:250]

    xmlre = re.compile( "^<?xml\W+version" )
    rspre = re.compile( "<reallySimplePhoto" )
    opmlre = re.compile( "<opml version" )

    if checkpart.startswith( "<?xml version" ):
        pass
        # we have a xml based document

    if checkpart.startswith( "<?xml version" ):
        pass
        # check for opml
        # check for rss


#
# dialogs
#
def cancelContinueAlert(title, message, butt1="OK", butt2=False):
    """Run a generic Alert with buttons "Weiter" & "Abbrechen".

       Returns True if "Weiter"; False otherwise
    """
    alert = NSAlert.alloc().init()
    alert.setAlertStyle_( 0 )
    alert.setInformativeText_( title )
    alert.setMessageText_( message )
    alert.setShowsHelp_( False )
    alert.addButtonWithTitle_( butt1 )

    if butt2:
        # button 2 has keyboard equivalent "Escape"
        button2 = alert.addButtonWithTitle_( butt2 )
        button2.setKeyEquivalent_( unichr(27) )

    f = alert.runModal()
    return f == AppKit.NSAlertFirstButtonReturn


def errorDialog( message="Error", title="Some error occured..."):
    return cancelContinueAlert(title, message)



#
# should be obsolete
#

#
# Open File
#
def getFileDialog(multiple=False):
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(True)
    panel.setCanChooseDirectories_(False)
    panel.setAllowsMultipleSelection_(multiple)
    rval = panel.runModalForTypes_( None )
    if rval:
        return [t for t in panel.filenames()]
    return []


def getFolderDialog(multiple=False):
    panel = NSOpenPanel.openPanel()
    panel.setCanChooseFiles_(False)
    panel.setCanChooseDirectories_(True)
    panel.setAllowsMultipleSelection_(multiple)
    rval = panel.runModalForTypes_([])
    if rval:
        return [t for t in panel.filenames()]
    return []


def NSURL2str( nsurl ):
    if isinstance(nsurl, NSURL):
        return str(nsurl.absoluteString())
    return nsurl

#
# File save dialog
#
# SHOULD NOT BE USED ANYMORE (NSDocument handling)
def saveAsDialog(path):
    panel = NSSavePanel.savePanel()

    if path:
        panel.setDirectory_( path )

    panel.setMessage_( u"Save as OPML" )
    panel.setExtensionHidden_( False )
    panel.setCanSelectHiddenExtension_(True)
    panel.setRequiredFileType_( u"opml" )
    if path:
        if not os.path.isdir( path ):
            folder, fle = os.path.split(path)
        else:
            folder = path
            fle = "Untitled.opml"
        rval = panel.runModalForDirectory_file_(folder, fle)
    else:
        rval = panel.runModal()

    if rval == NSFileHandlingPanelOKButton:
        return panel.filename()
    return False


def getFileProperties( theFile ):
    """
    """
    sfm = NSFileManager.defaultManager()
    props = sfm.fileAttributesAtPath_traverseLink_( theFile, True )
    if not props:
        return {}
    mtprops = props.mutableCopy()
    mtprops.removeObjectsForKeys_( [
        u"NSFileExtensionHidden",
        u"NSFileGroupOwnerAccountID",
        u"NSFileGroupOwnerAccountName",
        u"NSFileOwnerAccountID",
        u"NSFileOwnerAccountName",
        #u"NSFilePosixPermissions",
        #u"NSFileReferenceCount",
        # u"NSFileSize",
        #u"NSFileSystemFileNumber",
        u"NSFileSystemNumber",
        u"NSFileType",
        # u"NSFileHFSCreatorCode",
        # u"NSFileHFSTypeCode",
        #u"NSFileCreationDate"
        ] )
    return mtprops

def setFileProperties( theFile, props ):
    sfm = NSFileManager.defaultManager()
    return sfm.changeFileAttributes_atPath_( props, theFile )

def datestring_nsdate( dt=datetime.datetime.now() ):
    now = str(dt)
    now = now[:19]
    now = now + " +0000"
    return now


def getDownloadFolder( nsurl ):
    defaults = NSUserDefaults.standardUserDefaults()
    cacheFolder = CactusVersion.cachefolder
    try:
        cacheFolder = unicode(defaults.objectForKey_( u'txtCacheFolder'))
    except StandardError, err:
        print "CactusTools.getDownloadFolder(%s) -> False" % NSURL2str(nsurl)
        print "ERROR reading defaults.", repr(err)

    cacheFolder = os.path.expanduser( cacheFolder )

    # parent folder must exists; minimal plausibility
    parent, foldername = os.path.split( cacheFolder )
    if not os.path.exists( parent ):
        print "CactusTools.getDownloadFolder(%s) -> False" % NSURL2str(nsurl)
        return False, False

    if not os.path.exists(cacheFolder):
        os.makedirs( cacheFolder )
    #
    localpath = makeunicode( nsurl.relativePath() )
    s = nsurl.absoluteString()
    if '#' in s:
        n = s.count( '/' )
        if n >= 3:
            l = s.split( '/' )
            filename = l[-1]
            filename = urllib.unquote( filename )
            base , fname = os.path.split( localpath )

            localpath = os.path.join( base, filename )

    if localpath.startswith( u'/' ):
        localpath = localpath[1:]
    localpath = os.path.join( makeunicode(nsurl.host()), localpath)

    if localpath:
        localrelfolder, localname = os.path.split( localpath )
        localpath = os.path.join( cacheFolder, localpath )
        if kwdbg:
            print "CactusTools.getDownloadFolder(%s) -> %s" % (NSURL2str(nsurl), repr(localpath) )
        return localpath, localname
    return False, False


def getRemotefilemodificationDate( url ):

    try:
        f = urllib.urlopen( url )
    except IOError, err:
        print "ERROR: Could not open url (%s) for date reading." % url
        return False

    rinfo = f.info()
    f.close()

    remotemodfdate = rinfo.getdate('last-modified')
    if remotemodfdate:
        try:
            rmodfdate = datetime.datetime( *remotemodfdate[:6] )
            #rmodfdate = datetime.datetime( *rinfo.getdate('last-modified')[:6] )
        except TypeError, err:
            print "Could not get remote file(%s) modification date." % url
            return False
        return rmodfdate
    return False

def setFileModificationDate( filepath, modfdt ):
    l = getFileProperties( filepath )
    date = Foundation.NSDate.dateWithString_( datestring_nsdate( modfdt ) )
    l['NSFileModificationDate'] = date
    setFileProperties( filepath, l)
    folder, filename = os.path.split( filepath )
    print "Setting file(%s) modification date to %s" % (filename, repr(modfdt))


def cache_url( nsurl, fileextension ):
    if 1:
        print "CactusTools.cache_url( %s, %s )" % (nsurl, fileextension)

    if not nsurl:
        return False

    returnURL = nsurl
    url = NSURL2str( nsurl )

    # pdb.set_trace()

    try:
        localpath, localname = getDownloadFolder(nsurl)

        # perhaps we are not caching
        if not localpath:
            return nsurl

        if not localpath.endswith(localname):
            localfullpath = os.path.join(localpath, localname)

        folder, filename = os.path.split( localpath )
        if not os.path.exists(folder):
            os.makedirs( folder )

        dodownload = False
        if os.path.exists( localpath ):
            # file already downloaded; perhaps set file modification date
            lmodfdate = os.stat( localpath ).st_mtime
            lmodfdate = datetime.datetime.utcfromtimestamp( lmodfdate )
            rmodfdate = getRemotefilemodificationDate( url )

            if not rmodfdate:
                # remote modification date could not be determined
                pass
            elif rmodfdate and rmodfdate < lmodfdate:
                setFileModificationDate( localpath, rmodfdate )
            elif rmodfdate and rmodfdate == lmodfdate:
                pass
            else:
                dodownload = True
        else:
            dodownload = True

        if dodownload:
            #
            if os.path.isdir( localpath ):
                if not localname:
                    localname = "file"
                    localpath = os.path.join( localpath, localname + "." + fileextension )

            if fileextension:
                if not localpath.lower().endswith( "." + fileextension.lower() ):
                    localpath = localpath + '.' + fileextension

            print "LOAD: %s..." % url
            headers = {}
            r = requests.get( url )
            s = r.content
            headers = r.headers
            r.close()
            fob = open(localpath, 'w')
            fob.write( s )
            fob.close()
            
            dt = datetime.datetime.now()
            dts = feedparser._parse_date( headers.get( 'last-modified', '' ) )
            dts = time.mktime( dts )
            if dts:
                dt = datetime.datetime.fromtimestamp( dts )

            try:
                finder = asc.app(u'Finder.app', terms=Finder10)
                hfspath = mactypes.File( localpath ).hfspath
                finder.files[hfspath].comment.set( url )
            except StandardError, v:
                print "SET COMMENT FAILED ON '%s'" % localpath
            # get file date
            lmodfdate = os.stat( localpath ).st_mtime
            lmodfdate = datetime.datetime.utcfromtimestamp( lmodfdate )
            try:
                # rmodfdate = datetime.datetime( *headers.getdate('last-modified')[:6] )
                # setFileModificationDate( localpath, rmodfdate )
                setFileModificationDate( localpath, dt )
            except TypeError as err:
                # do not cache if modification date cannot be determined
                print "NOCACHE: Could not get remote file(%s) modification date." % url
                print( err )
            print "LOAD: %s...done" % url
            print "LOCAL:", repr(localpath)

        returnURL = NSURL.fileURLWithPath_( unicode(localpath) )

    except Exception, err:
        tb = unicode(traceback.format_exc())
        print tb
        print

    return returnURL

def mergeURLs( base, rel ):
    """create an url with base as the base, updated by existing parts of rel."""
    s = u"CactusTools.mergeURLs(%s, %s) ->  %s"

    prel = urlparse.urlparse( rel )
    if prel.scheme and prel.netloc:
        return prel.geturl()

    if type(base) in (NSURL,):
        base = NSURL2str(base)
    
    # it's a relative path

    pbase = urlparse.urlparse( base )

    path = pbase.path
    folder, filename = os.path.split( path )
    basename, ext = os.path.splitext( filename )
    if ext != "" and path[-1] != '/':
        path = os.path.join(folder, rel)
    else:
        path = os.path.join(path, rel)
    

    target = urlparse.ParseResult(
        scheme = pbase.scheme,
        netloc = pbase.netloc,
        path = path,
        params = prel.params if (prel.params) else pbase.params,
        query = prel.query if (prel.query) else pbase.query,
        fragment = prel.fragment if (prel.fragment) else pbase.fragment)

    target = urlparse.urlunparse( target )
    try:
        s = s % ( base, rel, target)
        print s.encode("utf-8")
    except Exception, err:
        print
        print "ERROR in mergeURL"
        print err
        print "base:", repr(base)
        print "rel:", repr(rel)
        print "target:", repr(target)
        print
    return target


def getURLExtension( url ):
    purl = urlparse.urlparse( url )
    path = purl.path
    folder, filename = os.path.split( path )
    basename, ext = os.path.splitext( filename )
    if kwdbg:
        print "CactusTools.getURLExtension(%s) -> '%s' . '%s'" % ( url, basename, ext )
    return (basename, ext)
