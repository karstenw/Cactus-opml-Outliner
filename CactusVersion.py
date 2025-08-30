
import os

appname ="Cactus Outline-Editor"
appnameshort = "Cactus"

copyright = 'Copyright 2011-2023 Karsten Wolf'

version = "0.8.1"

# 
user_agent = "%s/%s +https://github.com/karstenw/Cactus-opml-Outliner" % (appname, version)

document_creator = "Created by %s %s" % (appname, version)

cachefolder = os.path.expanduser("~/Library/Application Support/%s" % appname )

developmentversion = False

# py3 stuff
py3 = False
try:
    unicode('')
    punicode = unicode
    pstr = str
    punichr = unichr
except NameError:
    punicode = str
    pstr = bytes
    py3 = True
    punichr = chr
    long = int

