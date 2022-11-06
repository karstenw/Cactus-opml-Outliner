
# the outline. what else?
typeOutline = 1

# the still used tableview. to be merged with outline
typeTable = 2

# an alternate view. exists only as an idea
typeBrowser = 3

# are these still used?
editorTypes = (typeOutline, typeTable, typeBrowser)
hierarchicalTypes = (typeOutline, typeBrowser)

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

