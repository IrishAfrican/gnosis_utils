"Test handling of Unicode strings and plain Python strings"

from gnosis.xml.pickle import loads,dumps
from gnosis.xml.pickle.util import setInBody
from types import bytes, str
from . import funcs

funcs.set_parser()

#-- Create some unicode and python strings (and an object that contains them)
ustring = "Alef: %s, Omega: %s" % (chr(1488), chr(969))
pstring = "Only US-ASCII characters"
estring = "Only US-ASCII with line breaks\n\tthat was a tab"
class C:
    def __init__(self, ustring, pstring, estring):
        self.ustring = ustring
        self.pstring = pstring
        self.estring = estring
o = C(ustring, pstring, estring)

#-- Try standard pickling cycle (default setInBody() settings)
#print '\n------------* Pickle with Python and Unicode strings *------------------'
xml = dumps(o)
#print xml,
#print '------------* Restored attributes from different strings *--------------'
o2 = loads(xml)
# check types explicitly, since comparison will coerce types
if not isinstance(o2.ustring,str):
    print("AAGH! Didn't get str")
    raise
if not isinstance(o2.pstring,bytes):
    print("AAGH! Didn't get bytes for pstring")
    raise
if not isinstance(o2.estring,bytes):
    print("AAGH! Didn't get bytes for estring")
    raise

#print "UNICODE:", `o2.ustring`, type(o2.ustring)
#print "PLAIN:  ", o2.pstring, type(o2.pstring)
#print "ESCAPED:", o2.estring, type(o2.estring)

if o.ustring != o2.ustring or \
   o.pstring != o2.pstring or \
   o.estring != o2.estring:
    print("ERROR(1)")
    raise

#-- Pickle with Python strings in body
#print '\n------------* Pickle with Python strings in body *----------------------'
setInBody(bytes, 1)
xml = dumps(o)
#print xml,
#print '------------* Restored attributes from different strings *--------------'
o2 = loads(xml)
# check types explicitly, since comparison will coerce types
if not isinstance(o2.ustring,str):
    print("AAGH! Didn't get str")
    raise
if not isinstance(o2.pstring,bytes):
    print("AAGH! Didn't get bytes for pstring")
    raise
if not isinstance(o2.estring,bytes):
    print("AAGH! Didn't get bytes for estring")
    raise

#print "UNICODE:", `o2.ustring`, type(o2.ustring)
#print "PLAIN:  ", o2.pstring, type(o2.pstring)
#print "ESCAPED:", o2.estring, type(o2.estring)

if o.ustring != o2.ustring or \
   o.pstring != o2.pstring or \
   o.estring != o2.estring:
    print("ERROR(1)")
    raise

#-- Pickle with Unicode strings in attributes (FAIL)
#print '\n------------* Pickle with Unicode strings in XML attrs *----------------'
setInBody(str, 0)
try:
    xml = dumps(o)
    print("FAIL: We should not be allowed to put Unicode in attrs")
    raise
except TypeError:
    #print "As intended, a TypeError is encountered putting Unicode in attrs"
    pass	

print("** OK **")
