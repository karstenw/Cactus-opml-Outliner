# -*- coding: utf-8 -*-

# the different document types

#
# ATTENTIOON: changing the string here (CactusOPMLType = u'OPML File') needs to 
# change the string in "OpenURL.nib" window too!
#


# works
CactusOPMLType = u'OPML File'
# CactusOPMLFileExtensions = [ 'opml', 'xml']
CactusOPMLFileExtensions = [ 'opml' ]
CactusOPMLOSTypes = [ 'OPML', '****' ]


# works --- so far
CactusRSSType = u'RSS File'
# CactusRSSFileExtensions = [ 'rss', 'xml']
CactusRSSFileExtensions = [ 'rss' ]
CactusRSSOSTypes = [ '****' ]


# an outliner as a general xml editor
CactusXMLType = u'XML File'
CactusXMLFileExtensions = [ 'xml', ]
CactusXMLOSTypes = [ '****' ]


CactusDocumentTypesSet = set( (CactusOPMLType, CactusRSSType, CactusXMLType) )


#
# from here on it's wishful thinking
#


# don't know yet, if this is useful
CactusTEXTType = u'Cactus Text'
CactusTEXTFileExtensions = [ 'txt', ]
CactusTEXTOSTypes = [ 'TEXT', 'utxt' ]


# I want to have...
CactusSQLITEType = u'Cactus Sqlite'
CactusSQLITEFileExtensions = [ 'sqlite', ]
CactusSQLITEOSTypes = [ '****' ]


# I want to have...
CactusXOXOType = u'Cactus XOXO'
CactusXOXOFileExtensions = [ 'xoxo', 'xml', 'html']
CactusXOXOOSTypes = [ '****' ]


# haven't looked into it yet
CactusEMACSORGType = u'Cactus Emacs ORG'
CactusEMACSORGFileExtensions = [ 'org', ]
CactusEMACSORGOSTypes = [  ]


# this is on the delete list
CactusTABLEType = u'Cactus Table'
CactusTABLEFileExtensions = [ 'table', ]
CactusTABLEOSTypes = [ '****' ]

