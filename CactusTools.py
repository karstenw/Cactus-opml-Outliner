
# -*- coding: utf-8 -*-


"""Some tools which are needed by most files.
"""

import sys
import os

import pdb

import re

import urllib

import CactusVersion

import feedparser

import AppKit
NSOpenPanel = AppKit.NSOpenPanel
NSAlert = AppKit.NSAlert
NSSavePanel = AppKit.NSSavePanel
NSFileHandlingPanelOKButton  = AppKit.NSFileHandlingPanelOKButton



#
# tools
#
def readURL( nsurl, type_="OPML" ):
    """Read a file. May be local, may be http"""

    # pdb.set_trace()
    url = str(nsurl.absoluteString())
    print "CactusTools.readURL( '%s', '%s' )" % (url, type_)
    # f = urllib.FancyURLopener()
    # f.addheader('User-Agent', CactusVersion.user_agent)
    fob = feedparser._open_resource(url, None, None, CactusVersion.user_agent, None, [], {})

    # fob = f.open(url)
    s = fob.read()
    fob.close()

    if type_ == "OPML":
        # clear bogative opmleditor opml
        if s.startswith("""<?xml encoding="ISO-8859-1" version="1.0"?>"""):
            s = s.replace("""<?xml encoding="ISO-8859-1" version="1.0"?>""",
                          """<?xml version="1.0" encoding="ISO-8859-1"?>""")
    
            # this error occurs up until now only combined with the previous one
            #
            # this is a quick & dirty approach and should be applied much more carefully than
            # it is now...
            if "<directiveCache>" in s:
                s = s.replace( "<directiveCache>", "</outline>")

    # this apllies to all since cactus currently only reads xml files
    if s.startswith("<?xml ") or s.startswith("<opml "):
        re_bogusCharacters = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f]')
        t = re.sub( re_bogusCharacters, "???", s)
        if s != t:
            print "Bogus characters in XML..."
        s = t
    return s


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
