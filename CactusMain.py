
# -*- coding: utf-8 -*-


import PyObjCTools
import PyObjCTools.NibClassBuilder
extractClasses = PyObjCTools.NibClassBuilder.extractClasses
AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass

import PyObjCTools.AppHelper
AppHelper = PyObjCTools.AppHelper


extractClasses("MainMenu")
extractClasses("OpenURL")

extractClasses("TableEditor")
extractClasses("OutlineEditor")
extractClasses("NodeEditor")
extractClasses("OpenAsAccessoryView")

import CactusOutlineDoc
import CactusTableDocument


import Outline
import Cactus

import CactusVersion

if CactusVersion.developmentversion:
    import PyObjCTools.Debugging
    PyObjCTools.Debugging.installVerboseExceptionHandler()

if __name__ == "__main__":
    AppHelper.runEventLoop()
