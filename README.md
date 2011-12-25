## This is the Cactus-opml outliner/editor. ##



#### It is an outline editor based on the PythonBrowser example from PyObjC. ####


#### Developed on OSX 10.4, Xcode 2.5, pyobjc 1.4, py2app 0.53 ####


#### To build you need a 32-bit python.  ####

    python setup.py py2app


This will build the app in the dist folder.


## A universal binary is in the download section. ##



Prerequisites fro compiling:

+ python 2.7 - older versions may work
+ PyobjC
+ py2app
+ Apple developer tools



It's flakey, buggy and a lot of fun.

Don't use it to save your current OPML files. I've seen no errors so far but there is the possibility of attribute omission.

Use it to explore an OPML file.




## Things that work: ##

### files, outlines and tables ###
- open file (opml)
- open url (opml)
- new outline
- new table
- node movements up & down
- create new node (Return)


## Things that don't work: ##

- open document via open event or the dock
- rss
- save (only save as)
- saving when outline structure does not conform to opml (head & body element)
- cut, copy & paste
- nodetypes
- header nodes are saved untouched, no automatic data update
- honoring expansionstate, windowstate
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
<td>open node selection in new opml document or browser.</td></tr>

</table>
