
# -*- coding: utf-8 -*-


"""Some tools which are needed by most files.
"""

import sys
import os

import traceback

import datetime
import unicodedata

import struct

import mactypes
import appscript
asc = appscript

kwdbg = False
kwlog = True
import pdb

import re

import urllib

import CactusDocumentTypes
CactusOPMLType = CactusDocumentTypes.CactusOPMLType
CactusRSSType = CactusDocumentTypes.CactusRSSType
CactusXMLType = CactusDocumentTypes.CactusXMLType
CactusHTMLType = CactusDocumentTypes.CactusHTMLType
CactusPLISTType = CactusDocumentTypes.CactusPLISTType
CactusIMLType = CactusDocumentTypes.CactusIMLType

CactusDocumentTypesSet = CactusDocumentTypes.CactusDocumentTypesSet
CactusDocumentXMLBasedTypesSet = CactusDocumentTypes.CactusDocumentXMLBasedTypesSet


import CactusVersion

import feedparser

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
    return struct.pack(">I", num)


def ostype2num( ostype ):
    return struct.pack('BBBB', list(ostype))


def makeunicode(s, srcencoding="utf-8", normalizer="NFC"):
    try:
        s = unicode(s, srcencoding)
    except TypeError:
        print type(s)
    s = unicodedata.normalize(normalizer, s)
    return s


def detectFileType( nsfileurl ):
    """Not yet sure how to autodetect without reading some files twice.

    So far the parsers used are:
        OPML: cElementTree (opens string)
        RSS: feedparser (opens string)
        XML: cElementTree (opens string)
        HTML: lxml (opens URL)
        PLIST: NSDictionary.dictionaryWithContentsOfURL_ (opens URL)
    """
    pass


def readURL( nsurl, type_="" ):
    """Read a file. May be local, may be http"""

    translateType = {
        CactusOPMLType: "opml",
        CactusHTMLType: "html",
        CactusXMLType: "xml",
        CactusRSSType: "rss",
        CactusPLISTType: "plist",
        CactusIMLType: "xml"
    }

    fileext = translateType.get( type_, "")

    url = NSURL2str(nsurl)
    print "CactusTools.readURL( '%s', '%s' )" % (url, type_)

    defaults = NSUserDefaults.standardUserDefaults()
    cache = False
    try:
        cache = bool(defaults.objectForKey_( u'optCache'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)

    if cache:
        if not nsurl.isFileURL():
            nsurl = cache_url(nsurl, fileext)

    url = NSURL2str(nsurl)

    fob = feedparser._open_resource(url, None, None, CactusVersion.user_agent, None, [], {})
    s = fob.read()
    fob.close()

    if type_ == CactusOPMLType:
        # this is a quick & dirty approach and should be applied much more carefully than
        # it is now...

        # clear bogative xml declaration. OPML-Editor, I'looking at you
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
                s1 = s.find( startrule,s2 )
                s2 = s.find( endrule, s1 )
                s2 = s2 + len(endrule)
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
    sfm = NSFileManager.defaultManager()
    props = sfm.fileAttributesAtPath_traverseLink_( theFile, True )

    mtprops = props.mutableCopy()
    mtprops.removeObjectsForKeys_( [
        u"NSFileExtensionHidden",
        u"NSFileGroupOwnerAccountID",
        u"NSFileGroupOwnerAccountName",
        u"NSFileOwnerAccountID",
        u"NSFileOwnerAccountName",
        u"NSFilePosixPermissions",
        u"NSFileReferenceCount",
        u"NSFileSize",
        u"NSFileSystemFileNumber",
        u"NSFileSystemNumber",
        u"NSFileType",
        u"NSFileHFSCreatorCode",
        u"NSFileHFSTypeCode",
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

    # pdb.set_trace()

    defaults = NSUserDefaults.standardUserDefaults()
    cacheFolder = CactusVersion.cachefolder
    try:
        cacheFolder = unicode(defaults.objectForKey_( u'txtCacheFolder'))
    except StandardError, err:
        print "ERROR reading defaults.", repr(err)

    cacheFolder = os.path.expanduser( cacheFolder )

    # parent folder must exists; minimal plausibility
    parent, foldername = os.path.split( cacheFolder )
    if not os.path.exists( parent ):
        return False, False

    if not os.path.exists(cacheFolder):
        os.makedirs( cacheFolder )
    #
    localpath = str( nsurl.relativePath() )
    s = nsurl.absoluteString()
    if '#' in s:
        # pdb.set_trace()
        n = s.count( '/' )
        if n >= 3:
            l = s.split( '/' )
            filename = l[-1]
            filename = urllib.unquote( filename )
            base , fname = os.path.split( localpath )

            localpath = os.path.join( base, filename )

    if localpath.startswith('/'):
        localpath = localpath[1:]
    localpath = os.path.join( str(nsurl.host()), localpath)

    if localpath:
        localrelfolder, localname = os.path.split( localpath )
        localpath = os.path.join( cacheFolder, localpath )
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

    try:
        rmodfdate = datetime.datetime( *rinfo.getdate('last-modified')[:6] )
    except TypeError, err:
        print "Could not get remote file(%s) modification date." % url
        return False
    return rmodfdate


def setFileModificationDate( filepath, modfdt ):
    l = getFileProperties( filepath )
    date = Foundation.NSDate.dateWithString_( datestring_nsdate( modfdt ) )
    l['NSFileModificationDate'] = date
    setFileProperties( filepath, l)
    folder, filename = os.path.split( filepath )
    print "Setting file(%s) modification date to %s" % (filename, repr(modfdt))


def cache_url( nsurl, fileextension ):
    returnURL = nsurl
    # pdb.set_trace()
    try:
        localpath, localname = getDownloadFolder(nsurl)
        if not localpath:
            return nsurl

        folder, filename = os.path.split( localpath )
        if not os.path.exists(folder):
            os.makedirs( folder )

        url = NSURL2str( nsurl )

        if kwlog:
            print "CactusTools.cache_url( %s, %s )" % (url, fileextension)

        dodownload = False
        if os.path.exists( localpath ):
            # file already downloaded; perhaps set file modification date
            lmodfdate = os.stat( localpath ).st_mtime
            lmodfdate = datetime.datetime.utcfromtimestamp( lmodfdate )
            rmodfdate = getRemotefilemodificationDate( url )

            if rmodfdate and rmodfdate < lmodfdate:
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
                if not localpath.endswith( "." + fileextension ):
                    localpath = localpath + '.' + fileextension
            print "LOAD: %s..." % url
            fname, info = urllib.urlretrieve(url, localpath)
            print "LOAD: %s...done" % url
            try:
                finder = asc.app(u'Finder.app')
                hfspath = mactypes.File( localpath ).hfspath
                # .files[u'Terra:Users:karstenwo:Desktop:Neuer Ordner:Untitled 2'].comment.set('Hello World')
                finder.files[hfspath].comment.set( url )
            except StadardError, v:
                print "SET COMMENT FAILED ON '%s'" % localpath
            # get file date
            lmodfdate = os.stat( localpath ).st_mtime
            lmodfdate = datetime.datetime.utcfromtimestamp( lmodfdate )
            try:
                rmodfdate = datetime.datetime( *info.getdate('last-modified')[:6] )
                setFileModificationDate( localpath, rmodfdate )
            except TypeError, err:
                print "Could not get remote file(%s) modification date." % fname

        returnURL = NSURL.fileURLWithPath_( unicode(localpath) )

    except Exception, err:
        # pdb.set_trace()
        tb = unicode(traceback.format_exc())
        print tb
        print

    return returnURL
