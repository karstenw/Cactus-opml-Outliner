# CactusExceptions.py

#
# Exceptions
#

import sys

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

class CactusBaseException(StandardError):
    def __init__(self, *args):
        Exception.__init__(self, *args)
        self.wrapped_exc = sys.exc_info()

#
# parsing documents

class OPMLParseErrorException(CactusBaseException):
    """An OPML source could not be parsed."""
    pass

class RSSParseErrorException(CactusBaseException):
    """A RSS source could not be parsed."""
    pass

class XMLParseErrorException(CactusBaseException):
    """A XML source could not be parsed."""
    pass

class HTMLParseErrorException(CactusBaseException):
    """A HTML source could not be parsed."""
    pass

class PLISTParseErrorException(CactusBaseException):
    """A PLIST source could not be parsed."""
    pass



#
# Misc
class CancelledException(CactusBaseException):
    pass

class DoneException(CactusBaseException):
    pass

class DoneMessageException(CactusBaseException):
    pass
