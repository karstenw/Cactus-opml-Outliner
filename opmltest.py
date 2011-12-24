
import pdb

import pprint
pp=pprint.pprint

import opml

# pdb.set_trace()

f=open("./+testfiles/root_5.opml", 'r')
s=f.read()
f.close()


d = opml.from_string(s)

