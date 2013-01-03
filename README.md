## This is the Cactus-opml outline editor. ##


It is an outline editor based on the PythonBrowser example from PyObjC.

Developed on OSX 10.4 with Python 2.7, Xcode 2.5, pyobjc 1.4 and py2app 0.53

It's still in development but gets better and better.

Use it to explore OPML, RSS, XML and HTML files. Nodes can be opened in the browser or in Quicktime Player. See the shortcuts section at the end.


## A Warning ##

RSS, XML and HTML files are new and still in the make so please be cautious with Cactus generated files of these kinds. For example Cactus doesn't know about namespaces in RSS. They sure get lost if you save a RSS file in Cactus.

HTML files can not yet be saved.

XML Text for XML files is stored currently in the "Comment" column. This is a temporary solution that will be fixed with the refactoring of the outline node attribute system.

OPML files seem stable. In fact Cactus repairs some of them.

RSS files can be as sloppy as feedparser lets them. After saving they should be clean XML.


## Quickstart ##

Download the latest binary from
https://www.dropbox.com/s/v4a3ayrut0mxil3/Cactus_v040.zip
unzip and launch.

Do a google search for "filetype:opml"

Copy a search result link, switch to Cactus, select file menu "open URL...", paste into the text field and click OK.

Play with the outline and the appearance checkboxes in the upper right corner.

Indent and Outdent selected nodes with TAB and SHIFT-TAB.

Move selections up and down with ctrl-up and ctrl-down.

Delete rows with delete. No undo. No row copying.

The menus are mostly not operable. You can use the "File", "Window" and "Help" menu. Some items of the "Outline" menu have been activated.

Selected text can be copied and pasted. The standard simple undo works for text editing.

Look for nodes with content in the Value column, select one or more and try ctrl-alt-enter (NOT the Return key, the one on the numeric keypad). Depending on the data in those rows, new windows might open in Cactus (for linked OPML and RSS), your standard browser (for websites and pictures) or the Quicktime Player (for movies and sounds).

RSS and XML types can be saved but currently I would advise against using the resulting files for anything serious.

OPML should be stable. If you find a bug, please report it on the mailing list.

With the new "Open As..." option in the file dialogs, it is now possible to load an opml or rss file as xml. opml as rss and vice versa makes no sense but try to see why. Some files can only be openened as opmlbecause they are buggy and opening as opml does some repairs. Opening as xml needs a clean xml file.

## Pointers ##

Mailing list: http://groups.google.com/group/cactus-outliner-dev

Downloads page: https://www.dropbox.com/sh/azysrf5pokzp26a/h2mFhfeM6M

Latest binary: https://www.dropbox.com/s/v4a3ayrut0mxil3/Cactus_v040.zip


## Latest changes ##

Cactus has now big icons up to 512 pixels.

HTML is now a document type but only for reading.

There is now a context menu. Only item is "Include" which will include linked opml files of the types 'include', 'outline', 'thumbList', 'code', 'thumbListVarCol' and 'thumbList'.

The Outline window now shows which file type was loaded. I.e. one of "OPML File", "RSS File" or "XML File".

The "Expand", "Expand All Subheads", "Collapse", "Collapse Everything", "Collapse To Parent" items of the "Outline" menu have been activated.

The Open and OpenURL dialogs now have an extension to force the filetype; i.e. Open As...

XML is now a document type.

RSS and OPML are now a document types.

Document icons for local files.

Added a recent URLs menu to the open URL dialog. Holds the last 30 visited URLs.

Cactus now tries to correct some common errors in opml files.

Corrections applied are:
+ wrong xml declarations ( "&lt;?xml encoding...?&gt;" instead of "&lt;?xml version...?>"
+ illegal characters (chrs 0-8,11,12,14-31) are replaced with "???"
+ some opml files had a &lt;directiveCache&gt; tag instead of &lt;/outline&gt; at the top level


Take a look at the updated shortcuts section. The ctrl-up/down keys were previously undocumented.


Links in outline nodes which end in one of (aac,aifc,aiff,aif,au,ulw,snd,caf,
gsm,kar,mid,smf,midi,mp3,swa,wav,3gp,3g2,amc,avi,vfw,dif,dv,fli,mp2,m1s,m75,
m15,m2p,mpg,mpeg,mp4,mpg4,mqv,qtz,mov,qt,qtl,rtsp,sd2,sdp,sml,m1a,mpa,mpm,
m1v,m2v,m4a,m4p,m4b,m4v,amr,cdda,dvd,atr,sdv,pls,qmed) are now open in Quicktime-Player

rss parser should be more tolerant now.

Internal stuff. Preparing for the NSDocument refactoring.

Updated feedparser to V5.1.1.


## Build ##

    python setup.py py2app


Will build the app in the dist folder.


#### A compiled universal binary can be downloaded from my dropbox. ####
http://goo.gl/EALQi


#### Prerequisites for compiling: ####


+ python 2.7 - older versions may work
+ PyobjC
+ py2app
+ Apple developer tools


## Recent versions ##

v0.4.0 HTML document type and big icons.

v0.3.8 Context menu

v0.3.7 Fixed a crashing bug.

v0.3.6 feedparser at 5.1.3.

v0.3.5b New document icons. "Open As..." with type select shortcuts. Five items of the "Outline" menu now working.

v0.3.3a XML is now a document type.

v0.3.2a RSS save as. Enclosures are now included in RSS documents.

v0.3.1 rss opens as rss document. Included PyRSS2Gen for RSS write.

v0.3.0 document icons, recent URLs menu

v0.2.7 m4a & mov files & urls now open in movieplayer. feedparser at v5.1.1.

v0.2.6 Corrected a bug in method naming. License added

v0.2.5 RSS nodes can be openend now, new outline adds basic structure to outline, help menu opens github/mailing list

v0.2.4 Table rows can be moved up/down; Table/Outlineview styles now apply directly from the checkboxes. Deleted "Apply" button.

v0.2.3 Corrected a bug introduced with node movements and preventing nodes to be manually created at the end of a level.

v0.2.2 Row height option

v0.2.1 Node movements

v0.2.0 Initial release.



## Things that work: ##

### files, outlines and tables ###
- open file (opml)
- open document via open event or by dragging files to the dock icon
- open url (opml)
- open outline from outline node (opml & rss)
- new outline
- new table
- node movements up & down
- create new node (Return)
- different styles in views. Grids, alternating background and variable row height.
- visibility of rows: value, type, comment


## Things that don't work: ##

- error messages can currently only be seen if Cactus is started from the command line: ```./Cactus.app/Contents/MacOS/Cactus```
- save (only save as)
- saving when outline structure does not conform to opml (head & body element)
- cut, copy & paste
- nodetypes
- header nodes are saved untouched, no automatic data update
- honoring expansionstate, windowstate (I don't intend to)
- freeing memory (take anything you get, give nothing back ;-)


## Shortcuts: ##
### open/save files ###
<table>
<tr><td>cmd-O</td><td>open file dialog</td></tr>
<tr><td>cmd-alt-O</td><td>open URL dialog</td></tr>
<tr><td>cmd-shift-S</td><td>save as dialog</td></tr>
</table>

### editing ###
<table>
<tr><td>Return</td><td>create a new node after the current and start editing</td></tr>
<tr><td>enter</td><td>start/end editing current node</td></tr>

<tr><td>tab</td><td>indent selection</td></tr>
<tr><td>shift-tab</td><td>outdent selection</td></tr>

<tr><td>ctrl-up</td><td>move selection up</td></tr>
<tr><td>ctrl-down</td><td>move selection down</td></tr>
</table>


### deleting ###
<table>
<tr><td>backspace</td><td>delete selection</td></tr>
<tr><td>delete</td><td>delete selection</td></tr>
</table>


### opening nodes ###
<table>
<tr><td>control-enter</td><td>open node in a table view (usefull if node has attributes)</td></tr>

<tr><td>control-alt-enter</td>
<td>open node selection in new opml document, browser or movieplayer.</td></tr>

</table>

### debugging ###
<table>
<tr><td>shift-enter</td><td>Dumps current document to Terminal. Cactus needs to be started via Terminal (./Cactus.app/Contents/MacOS/Cactus )</td></tr>
</table>
