
# -*- coding: utf-8 -*-


"""A unsorted collection of items regarding XML properties which are needed in
different places.
"""


import re


# in XML the only valid characters in the range 0-32 are:
# 09 - tab
# 0a - newline
# 0d - carriage return
re_bogusCharacters = re.compile( r'[\x00-\x08\x0b\x0c\x0e-\x1f]' )


# py3 stuff
punicode = str
pstr = bytes
py3 = True
punichr = chr
long = int

