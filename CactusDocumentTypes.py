# -*- coding: utf-8 -*-

# the different document types

#
# ATTENTIOON: changing the string here (CactusOPMLType = u'OPML File') needs to 
# change the string in "OpenURL.nib" window too!
#


# works
CactusOPMLType = u'OPML File'
CactusOPMLFileExtensions = [ 'opml' ]
CactusOPMLOSTypes = [ 'OPML', '****' ]


# works --- so far
CactusRSSType = u'RSS File'
CactusRSSFileExtensions = [ 'rss' ]
CactusRSSOSTypes = [ '****' ]


# an outliner as a xml editor
CactusXMLType = u'XML File'
CactusXMLFileExtensions = [ 'xml' ]
CactusXMLOSTypes = [ '****' ]

# an outliner as a html editor
CactusHTMLType = u'HTML File'
CactusHTMLFileExtensions = [ 'html', 'htm' ]
CactusHTMLOSTypes = [ '****' ]

# an outliner as a property list editor
CactusPLISTType = u'PLIST File'
CactusPLISTFileExtensions = [ 'plist' ]
CactusPLISTOSTypes = [ '****' ]

# an outliner as a iTunes Library editor
CactusIMLType = u'iTunes XML File'
# CactusIMLFileExtensions = [ 'xml' ]
CactusIMLOSTypes = [ '****' ]


CactusDocumentTypesSet = set( (CactusOPMLType,
                               CactusRSSType,
                               CactusXMLType,
                               CactusHTMLType,
                               CactusPLISTType) )

# plists don't need to be xml files
CactusDocumentXMLBasedTypesSet = set( (CactusOPMLType,
                                       CactusRSSType,
                                       CactusXMLType) )

#
# from here on it's wishful thinking
#

# don't know yet, if this is useful
#
# seems like a useful export format
# prefs indent spaces/tabs, encoding, columns
CactusTEXTType = u'Text File'
CactusTEXTFileExtensions = [ 'txt', ]
CactusTEXTOSTypes = [ 'TEXT', 'utxt' ]


# I want to have... but is it useful?
#
# seems like a useful export format
CactusSQLITEType = u'Sqlite File'
CactusSQLITEFileExtensions = [ 'sqlite', ]
CactusSQLITEOSTypes = [ '****' ]


# I want to have...
#
# after researching it a bit, this seems like a lost art...
#CactusXOXOType = u'XOXO File'
#CactusXOXOFileExtensions = [ 'xoxo', 'xml', 'html']
#CactusXOXOOSTypes = [ '****' ]


# haven't looked into it yet
CactusEMACSORGType = u'ORG File'
CactusEMACSORGFileExtensions = [ 'org', ]
CactusEMACSORGOSTypes = [  ]


# this is on the delete list; to be replaced by an outline
#CactusTABLEType = u'Cactus Table'
#CactusTABLEFileExtensions = [ 'table', ]
#CactusTABLEOSTypes = [ '****' ]

