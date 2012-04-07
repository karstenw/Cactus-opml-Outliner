"""
Script for building the example.

Usage:
    python setup.py py2app
"""
import os

from distutils.core import setup
import py2app

import CactusVersion

appname = CactusVersion.appname
appnameshort = CactusVersion.appnameshort

copyright = CactusVersion.copyright

version = CactusVersion.version


infostr = appname + ' ' + version + ' ' + copyright


setup(
    app=[{

        # 'script': "Cactus.py",
        'script': "CactusMain.py",

        'plist':{
            'CFBundleGetInfoString': infostr,
            'CFBundleIdentifier': 'org.kw.Cactus',
            'CFBundleShortVersionString': version,
            'CFBundleDisplayName': appnameshort,
            'CFBundleName': appnameshort,
            'CFBundleSignature': 'KWCs',
            'LSHasLocalizedDisplayName': False,
            'NSAppleScriptEnabled': False,
            'NSHumanReadableCopyright': copyright}}],

    data_files=["English.lproj/MainMenu.nib",
                "English.lproj/OutlineEditor.nib",
                "English.lproj/TableEditor.nib",
                "English.lproj/NodeEditor.nib",
                "English.lproj/OpenURL.nib",
                ],

    options={
        'py2app':{
            'iconfile': './+icon/Cowskull.icns'}}
)
