
# -*- coding: utf-8 -*-


"""Some tools which are needed by most files.
"""

import sys
import os

import re

import urllib


#
# tools
#
def readURL( url ):
    """Read a file. May be local, may be http"""

    print "CactusTools.readURL( '%s' )" % repr(url)
    f = urllib.FancyURLopener()
    fob = f.open(url)
    s = fob.read()
    fob.close()

    # clear bogative opmleditor opml
    if s.startswith("""<?xml encoding="ISO-8859-1" version="1.0"?>"""):
        s = s.replace("""<?xml encoding="ISO-8859-1" version="1.0"?>""",
                      """<?xml version="1.0" encoding="ISO-8859-1"?>""")

        # this error occurs up until now only combined with the previous one
        #
        # this is a q&d approach and should be applied much more carefully than
        # it is now...
        if "<directiveCache>" in s:
            s = s.replace( "<directiveCache>", "</outline>")

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
        
