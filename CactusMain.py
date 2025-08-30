
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


