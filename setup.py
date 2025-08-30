"""
Script for building the example.

Usage:
    python setup.py py2app
"""
import os

from distutils.core import setup
import py2app

import CactusVersion

iconpath = "+icon/large/"

import CactusDocumentTypes



appname = CactusVersion.appname
appnameshort = CactusVersion.appnameshort

copyright = CactusVersion.copyright

version = CactusVersion.version

infostr = appname + ' ' + version + ' ' + copyright

aeusage = "Cactus uses Apple events to coax Safari to get info about webpages."


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
                    'CFBundleTypeExtensions': CactusDocumentTypes.CactusXMLFileExtensions,
                    'CFBundleTypeIconFile': 'XMLDocument.icns',
                    'CFBundleTypeName': CactusDocumentTypes.CactusXMLType,
                    'CFBundleTypeOSTypes': CactusDocumentTypes.CactusXMLOSTypes,
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': u'CactusOutlineDocument',
                },
                {
                    'CFBundleTypeExtensions': CactusDocumentTypes.CactusHTMLFileExtensions,
                    'CFBundleTypeIconFile': 'HTMLDocument.icns',
                    'CFBundleTypeName': CactusDocumentTypes.CactusHTMLType,
                    'CFBundleTypeOSTypes': CactusDocumentTypes.CactusHTMLOSTypes,
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': u'CactusOutlineDocument',
                },
                {
                    'CFBundleTypeExtensions': CactusDocumentTypes.CactusPLISTFileExtensions,
                    'CFBundleTypeIconFile': 'PLISTDocument.icns',
                    'CFBundleTypeName': CactusDocumentTypes.CactusPLISTType,
                    'CFBundleTypeOSTypes': CactusDocumentTypes.CactusPLISTOSTypes,
                    'CFBundleTypeRole': 'Editor',
                    'NSDocumentClass': u'CactusOutlineDocument',
                },
                {
                    # 'CFBundleTypeExtensions': CactusDocumentTypes.CactusIMLFileExtensions,
                    'CFBundleTypeIconFile': 'IMLDocument.icns',
                    'CFBundleTypeName': CactusDocumentTypes.CactusIMLType,
                    'CFBundleTypeOSTypes': CactusDocumentTypes.CactusIMLOSTypes,
                    # 'CFBundleTypeRole': 'Editor',
                    'CFBundleTypeRole': 'Viewer',
                    'NSDocumentClass': u'CactusOutlineDocument',
                }
            ],
            'LSHasLocalizedDisplayName': False,
            'NSAppleScriptEnabled': False,
            'NSAppleEventsUsageDescription': aeusage,
            'NSHumanReadableCopyright': copyright}}],

    data_files=["English.lproj/MainMenu.nib",
                "English.lproj/OutlineEditor.nib",
                "English.lproj/TableEditor.nib",
                "English.lproj/NodeEditor.nib",
                "English.lproj/OpenURL.nib",
                "English.lproj/CalendarCreator.nib",
                "English.lproj/OpenAsAccessoryView.nib",
                "English.lproj/Preferences.nib",
                iconpath + "OPMLDocument.icns",
                iconpath + "XMLDocument.icns",
                iconpath + "RSSDocument.icns",
                iconpath + "PLISTDocument.icns",
                iconpath + "iXMLDocument.icns",
                iconpath + "Cowskull.icns" ],

    options={
        'py2app':{
            'iconfile': iconpath + 'Cowskull.icns',
            'packages' : ['lxml'],
            'frameworks' : ['/usr/local/lib/libxml2.2.dylib',
                            '/usr/local/lib/libxslt.1.dylib',
                            '/usr/local/lib/libexslt.0.dylib'],
            "excludes": [
                'TkInter', 'tkinter', 'tk', 'wx', 'sphinx',
                'pyqt5', 'qt5', 'PyQt5', 
                
                'setuptools', 'numba', 
                
                # 'certifi', 'pytz', 
                'notebook', 'nbformat', 'jedi', 'testpath', 'docutils',
                'ipykernel', 'parso', 'Cython', 'sphinx_rtd_theme', 'alabaster',
                'tornado', 'IPython', 'numpydoc', 'nbconvert', 
                'scipy', 'matplotlib', 
                'pandas', 'cv2', 'dlib', 'skimage', 'sklearn', 'mpl_toolkits',
                
                'PIL', #'cryptography'
            ],
        }
    }
)
