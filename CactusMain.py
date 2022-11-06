
# -*- coding: utf-8 -*-


import PyObjCTools

import PyObjCTools.AppHelper
AppHelper = PyObjCTools.AppHelper


import CactusVersion
devVersion = CactusVersion.developmentversion

import CactusOutline
import CactusAppDelegateClass

import CactusOutlineWindow

import CactusOutlineDoc
import CactusTableDocument
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

if CactusVersion.developmentversion:
    import PyObjCTools.Debugging
    PyObjCTools.Debugging.installVerboseExceptionHandler()

if __name__ == "__main__":
    AppHelper.runEventLoop(pdb=devVersion)


