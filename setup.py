"""
Script for building the example.

Usage:
    python setup.py py2app
"""
import os

from distutils.core import setup
import py2app

version = "0.2.1"
infostr = 'Cactus OPML-Reader ' + version + ' Copyright 2011 Karsten Wolf'


setup(
    app=[{
        'script': "Cactus.py",
        'plist':{
            'CFBundleGetInfoString': infostr,
            'CFBundleIdentifier': 'org.kw.Cactus',
            'CFBundleShortVersionString': version,
            'CFBundleSignature': 'KWCs',
            'LSHasLocalizedDisplayName': False,
            'NSAppleScriptEnabled': False,
            'NSHumanReadableCopyright': 'Copyright 2011 Karsten Wolf'}}],
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
