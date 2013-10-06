## This is the Cactus-opml outline editor. ##


It is an outline editor based on the PythonBrowser example from PyObjC.

Developed on OSX 10.6 with Python 2.7, Xcode 3.2, pyobjc 2.5 and py2app 0.8

It's still in development but gets better and better.

Use it to explore OPML, RSS, XML, PLIST, HTML and iTunes XMLfiles. Nodes can be opened in the webbrowser, in Quicktime Player or in Cactus depending on node type. See the shortcuts section at the end.

## Mailing list ##

<http://groups.google.com/group/cactus-outliner-dev>

## Downloads ##

<http://goo.gl/EALQi>




## A Warning ##

Due to the way how Cactus writes it's files you might be surprised at what you get after a save. For example, the RSS file type writes only RSS 2.0 files even though you perhaps read in an atom feed.

Each file write generates a new file. If your HTML file had a doctype of HTML3 or XHTML, after saving it will have the doctype selected in the HTML preferences and an utf-8 encoding.

The mappings are:
<table>
<tr><th>source</th><th></th><th>result</th></tr>

<tr><td>OPML</td><td>&#x21d2;</td><td>OPML 2.0</td></tr>
<tr><td>RSS</td><td>&#x21d2;</td><td>RSS 2.0</td></tr>
<tr><td>atom</td><td>&#x21d2;</td><td>RSS 2.0</td></tr>
<tr><td>PLIST xml</td><td>&#x21d2;</td><td>PLIST xml</td></tr>
<tr><td>PLIST binary</td><td>&#x21d2;</td><td>PLIST xml</td></tr>
<tr><td>HTML</td><td>&#x21d2;</td><td>HTML 4.1strict or html5</td></tr>

</table>



RSS, XML PLIST and HTML document types are new and still in the make so please be cautious with Cactus generated files of these kinds. For example Cactus doesn't know about namespaces in RSS. They sure get lost if you save a RSS file in Cactus.

XML and HTML Files had writing errors which are fixed now. Be cautios anyway.

The element text for XML and HTML files is stored currently in the "Comment" column. A possibly present tail part is stored as an attribute.  This is a temporary solution that will be fixed with the refactoring of the outline node attribute system.

OPML files seem stable. In fact Cactus repairs some damaged OPML files.

RSS reading is very good since it uses feedparser.

RSS writing omits namespaces.

XML reading is good.

HTML reading and writing looks good.

Currently Cactus can open "iTunes Music Library.xml" files. This is incomplete (the playlists are not parsed) and was a proof of concept since opening large libraries consumed too much memory and generated several 100000 outline nodes. Perhaps it will become a subtype of PLIST.

## Quickstart ##

Download the latest binary from
http://goo.gl/EALQi
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

With the new "Open As..." option in the file dialogs, it is now possible to load an OPML or RSS file as XML. OPML as RSS and vice versa makes no sense but try to see why. Some files can only be openened as opml because they are buggy and opening as OPML does some repairs. Opening as XML needs a clean XML file.

## Latest changes ##

Updated development environment to 10.6.

Open iTunes Library.xml file as their own type since .xml is already used.

XML and HTML writing are back.

PLIST file type. Read and write apple property lists.

Preferences.

Cactus now reads and saves the window position of OPML files.

Cactus now reads and saves the expansion state of OPML files.

A bug in the RSS generation that ommited the channel description has been corrected.

A bug in the previous version which ommitted all OPML head values has been corrected.

New shortcuts:
ctrl-left select parents of current selection
ctrl-alt-left select parents of current selection and collapse children

ctrl-right select children of current selection
ctrl-alt-right select children of current selection and expand children

Cactus has now big icons up to 512 pixels.

HTML is now a document type but only for reading.

There is now a context menu. The only item is "Include" which will include linked OPML files of the types 'include', 'outline', 'thumbList', 'code', 'thumbListVarCol' and 'thumbList'.

The Outline window now shows which file type was loaded. I.e. one of "OPML File", "RSS File" or "XML File".

The "Expand", "Expand All Subheads", "Collapse", "Collapse Everything", "Collapse To Parent" items of the "Outline" menu have been activated.

The Open and OpenURL dialogs now have an extension to force the filetype; i.e. Open As...

XML is now a document type.

RSS and OPML are now a document types.

Document icons for local files.

Added a recent URLs menu to the open URL dialog. Holds the last 30 visited URLs.

Cactus now tries to correct some common errors in OPML files.

Corrections applied are:
+ wrong XML declarations ( "&lt;?xml encoding...?&gt;" instead of "&lt;?xml version...?>"
+ illegal characters (chrs 0-8,11,12,14-31) are replaced with "???"
+ some OPML files had a &lt;directiveCache&gt; tag instead of &lt;/outline&gt; at the top level


Take a look at the updated shortcuts section. The ctrl-up/down keys were previously undocumented.


Links in outline nodes which end in one of (aac,aifc,aiff,aif,au,ulw,snd,caf,
gsm,kar,mid,smf,midi,mp3,swa,wav,3gp,3g2,amc,avi,vfw,dif,dv,fli,mp2,m1s,m75,
m15,m2p,mpg,mpeg,mp4,mpg4,mqv,qtz,mov,qt,qtl,rtsp,sd2,sdp,sml,m1a,mpa,mpm,
m1v,m2v,m4a,m4p,m4b,m4v,amr,cdda,dvd,atr,sdv,pls,qmed) are now open in Quicktime-Player

RSS parser should be more tolerant now.

Internal stuff. Preparing for the NSDocument refactoring.

Updated feedparser to V5.1.1.


## Build ##

    python setup.py py2app


Will build the app in the dist folder.


#### A compiled binary can be downloaded from my dropbox. Versions >= 0.5.0 need Intel Macs and 10.6.####
http://goo.gl/EALQi


#### Prerequisites for compiling: ####


+ python 2.7 - older versions may work
+ PyObjC
+ py2app
+ Apple developer tools
+ lxml library installed (sudo pip install lxml)


## Recent versions ##

v0.5.4 More calendar options working

v0.5.3 Calendar outline generator

v0.5.1 Open enclosure in RSS items preference

v0.5.0 10.6 intel build

v0.4.2 Reading iTunes XML Libraries

v0.4.1 Status line, new select all subnodes (see shortcuts), better RSS write, reading and writing windowposition and expansionstate, maxRowHeight menu, better editing.

v0.4.0 HTML document type and big icons.

v0.3.8 Context menu

v0.3.7 Fixed a crashing bug.

v0.3.6 feedparser at 5.1.3.

v0.3.5b New document icons. "Open As..." with type select shortcuts. Five items of the "Outline" menu now working.

v0.3.3a XML is now a document type.

v0.3.2a RSS save as. Enclosures are now included in RSS documents.

v0.3.1 RSS opens as RSS document. Included PyRSS2Gen for RSS write.

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
- open file (OPML, RSS, XML, HTML, PLIST)
- some sub types:
-- open iTunes Library.xml as iXML
-- open Safari webarchives as PLIST
- open document via open event or by dragging files to the dock icon
- open url (OPML, RSS, XML, HTML)
- open outline from outline node (OPML & RSS)
- new outline
- new table
- node movements up & down
- create new node (Return)
- different styles in views. Grids, alternating background and variable row height.
- visibility of rows: value, type, comment


## Things that don't work: ##

- error messages can currently only be seen if Cactus is started from the command line: ```./Cactus.app/Contents/MacOS/Cactus```
- saving when outline structure does not conform to OPML (head & body element)
- cut, copy & paste
- OPML nodetypes
- header nodes are saved untouched, no automatic data update
- honoring expansionstate, windowstate (I don't intend to)
- freeing memory


## Shortcuts: ##
### open/save files ###
<table>
<tr><td>cmd-O</td><td>open file dialog</td></tr>
<tr><td>cmd-alt-O</td><td>open URL dialog</td></tr>
<tr><td>cmd-S</td><td>save (for OPML, RSS)</td></tr>
<tr><td>cmd-shift-S</td><td>save as dialog</td></tr>
</table>

### editing ###
<table>
<tr><td>Return</td><td>create a new node after the current and start editing</td></tr>
<tr><td>escape</td><td>start/end editing current node</td></tr>

<tr><td>tab</td><td>indent selection</td></tr>
<tr><td>shift-tab</td><td>outdent selection</td></tr>

<tr><td>ctrl-up</td><td>move selection up</td></tr>
<tr><td>ctrl-down</td><td>move selection down</td></tr>

<tr><td>ctrl-left</td><td>select parent node</td></tr>
<tr><td>ctrl-alt-left</td><td>select parent node and collapse</td></tr>
<tr><td>ctrl-right</td><td>select all children</td></tr>
<tr><td>ctrl-alt-right</td><td>select all children and expand</td></tr>
</table>


### deleting ###
<table>
<tr><td>backspace</td><td>delete selection</td></tr>
<tr><td>delete</td><td>delete selection</td></tr>
</table>


### opening nodes ###
<table>
<tr><td>control-enter</td><td>open node in a table (usefull if node has attributes)</td></tr>

<tr><td>control-alt-enter</td>
<td>open node selection in new OPML document, browser or movieplayer depending on nodetype.</td></tr>

</table>

### debugging ###
<table>
<tr><td>shift-enter</td><td>Dumps current document to Terminal. Cactus needs to be started via Terminal (./Cactus.app/Contents/MacOS/Cactus )</td></tr>
</table>
