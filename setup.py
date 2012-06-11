"""
Script for building the example.

Usage:
    python setup.py py2app
"""
import os

from distutils.core import setup
import py2app

import CactusVersion
import CactusDocumentTypes


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
            'CFBundleDocumentTypes': [
                {
                    'CFBundleTypeExtensions': CactusDocumentTypes.CactusOPMLFileExtensions,
                    'CFBundleTypeIconFile': 'OPMLDocument.icns',
                    'CFBundleTypeName': CactusDocumentTypes.CactusOPMLType,
                    'CFBundleTypeOSTypes': CactusDocumentTypes.CactusOPMLOSTypes,
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': u'CactusOutlineDocument',
                },
                {
                    'CFBundleTypeExtensions': CactusDocumentTypes.CactusRSSFileExtensions,
                    'CFBundleTypeIconFile': 'RSSDocument.icns',
                    'CFBundleTypeName': CactusDocumentTypes.CactusRSSType,
                    'CFBundleTypeOSTypes': CactusDocumentTypes.CactusRSSOSTypes,
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': u'CactusOutlineDocument',
                },
                {
                    'CFBundleTypeExtensions': [ 'rss', 'xml', 'php' ],
                    'CFBundleTypeIconFile': 'OPMLDocument.icns',
                    'CFBundleTypeName': 'Cactus RSS',
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': 'CactusOutlineDocument'
                }
            ],
            'LSHasLocalizedDisplayName': False,
            'NSAppleScriptEnabled': False,
            'NSHumanReadableCopyright': copyright}}],

    data_files=["English.lproj/MainMenu.nib",
                "English.lproj/OutlineEditor.nib",
                "English.lproj/TableEditor.nib",
                "English.lproj/NodeEditor.nib",
                "English.lproj/OpenURL.nib",
                "+icon/OPMLDocument.icns"
                ],

    options={
        'py2app':{
            'iconfile': './+icon/Cowskull.icns'}}
)
