## This is the Cactus-opml outline editor. ##


It is an outline editor based on the PythonBrowser example from PyObjC.

Developed on OSX 10.4 with Python 2.7, Xcode 2.5, pyobjc 1.4 and py2app 0.53

It's still in development but gets better and better.

Don't use it to save your current OPML files. I've seen no errors so far but there is the possibility of attribute omission.

Use it to explore an OPML file.

Mailing list: http://groups.google.com/group/cactus-outliner-dev


## Quickstart ##



## Lates changes ##

RSS is now a document type

Document icons for local files.

Added a recent URLs menu to the open URL dialog. Holds the last 30 visited URLs.

Cactus now tries to correct some common errors in opml files.

Corrections applied are:
+ wrong xml declarations ( "<?xml encoding...?>" instead of "<?xml version...?>"
+ illegal characters (chrs 0-8,11,12,14-31) are replaced with "???"
+ some opml files had a <directiveCache> tag instead of </outline> at the top level


Take a look at the updated shortcuts section. The ctrl-up/down keys were previously undocumented.


Links in outline nodes which end in one of (aac,aifc,aiff,aif,au,ulw,snd,caf,
gsm,kar,mid,smf,midi,mp3,swa,wav,3gp,3g2,amc,avi,vfw,dif,dv,fli,mp2,m1s,m75,
m15,m2p,mpg,mpeg,mp4,mpg4,mqv,qtz,mov,qt,qtl,rtsp,sd2,sdp,sml,m1a,mpa,mpm,
m1v,m2v,m4a,m4p,m4b,m4v,amr,cdda,dvd,atr,sdv,pls,qmed) are now open in Quicktime-Player

rss parser should be toleranter now.

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
<tr><td>cmd-alt-O</td><td>open URL dialog</td>
<tr><td>cmd-shift-S</td><td>save as dialog</td>
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


