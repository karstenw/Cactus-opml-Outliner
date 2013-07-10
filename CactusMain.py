
# -*- coding: utf-8 -*-


import PyObjCTools
#import PyObjCTools.NibClassBuilder
#extractClasses = PyObjCTools.NibClassBuilder.extractClasses
#AutoBaseClass = PyObjCTools.NibClassBuilder.AutoBaseClass

import PyObjCTools.AppHelper
AppHelper = PyObjCTools.AppHelper


#extractClasses("MainMenu")
#extractClasses("OpenURL")

#extractClasses("TableEditor")
#extractClasses("OutlineEditor")
#extractClasses("NodeEditor")
#extractClasses("OpenAsAccessoryView")

import CactusVersion
import Outline
import CactusAppDelegateClass

import CactusOutlineDoc
import CactusTableDocument



if CactusVersion.developmentversion:
    import PyObjCTools.Debugging
    PyObjCTools.Debugging.installVerboseExceptionHandler()

if __name__ == "__main__":
    AppHelper.runEventLoop()
