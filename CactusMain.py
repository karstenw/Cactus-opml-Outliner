
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


import CactusOutlineDoc
import CactusTableDocument


import Outline
import Cactus


if __name__ == "__main__":
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()
