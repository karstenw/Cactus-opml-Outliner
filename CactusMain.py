
# -*- coding: utf-8 -*-


import PyObjCTools

import PyObjCTools.AppHelper
AppHelper = PyObjCTools.AppHelper


import CactusVersion
import CactusOutline
import CactusAppDelegateClass

import CactusOutlineWindow

import CactusOutlineDoc
import CactusTableDocument



if CactusVersion.developmentversion:
    import PyObjCTools.Debugging
    PyObjCTools.Debugging.installVerboseExceptionHandler()

if __name__ == "__main__":
    AppHelper.runEventLoop()
