# CactusExceptions.py

#
# Exceptions
#

import sys

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



#
# Misc
class CancelledException(CactusBaseException):
    pass

class DoneException(CactusBaseException):
    pass

class DoneMessageException(CactusBaseException):
    pass
