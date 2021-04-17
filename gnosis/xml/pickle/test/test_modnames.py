"Demonstrate that on-the-fly and gnosis.xml.* namespaces not saved in XML file --fpm"

import gnosis.xml.pickle as xml_pickle
from collections import UserList
from . import funcs
import re

funcs.set_parser()

# handcoded object to load Foo (i.e. without the pickler having
# seen it before)
ud_xml = """<?xml version="1.0"?>
<!DOCTYPE PyObject SYSTEM "PyObjects.dtd">
<PyObject module="__main__" class="Foo">
</PyObject>
"""

class myfoo: pass
class Foo: pass

# print "On-the-fly -- SHOULD *NOT* SEE MODULE NAME IN XML"
p = xml_pickle.loads(ud_xml)
# print it so we can see the modname
#print "Fullname = "+str(p)
if str(p.__class__) != 'gnosis.xml.pickle.util._util.Foo':
    print("ERROR(1)")
    raise

# dump and make sure modname doesn't stick
s = xml_pickle.dumps(p)
#print s
if re.search(s,'module'):
    print("ERROR(2)")
    raise

#print "From (old) xml_pickle namespace -- SHOULD *NOT* SEE MODULE NAME IN XML"
# put Foo into xml_pickle namespace
xml_pickle.Foo = myfoo
p = xml_pickle.loads(ud_xml)
# print it so we can see the modname
#print "Fullname = "+str(p)
if str(p.__class__) != '__main__.myfoo':
    print("ERROR(3)")
    raise

# dump it and make sure modname doesn't stick
s = xml_pickle.dumps(p)
#print s
if re.search(s,'module'):
    print("ERROR(4)")
    raise

# delete so it won't be found again below
del xml_pickle.Foo

# explicitly add to class store
xml_pickle.add_class_to_store('Foo',myfoo)

#print "From class store -- SHOULD *NOT* SEE MODULE NAME IN XML"
p = xml_pickle.loads(ud_xml)
# print it so we can see the modname
#print "Fullname = "+str(p)
if str(p.__class__) != '__main__.myfoo':
    print("ERROR(5)")
    raise

# dump & make sure modname doesn't stick
s = xml_pickle.dumps(p)
#print s
if re.search('module',s):
    print("ERROR(6)")
    raise

# remove so it won't be found again below
xml_pickle.remove_class_from_store('Foo')

# now, make sure we haven't broken modnames showing up when they SHOULD :-)
#print "My namespace (__main__) -- SHOULD SEE MODULE NAME IN XML"
# allow it to load my Foo
xml_pickle.setParanoia(0)
p = xml_pickle.loads(ud_xml)
# print it so we can see the modname
#print "Fullname = "+str(p)
if str(p.__class__) != '__main__.Foo':
    print("ERROR(7)")
    raise

# dump & make sure module name is written
s = xml_pickle.dumps(p)
#print s
if not re.search('PyObject\s+module="__main__"\s+class="Foo"',s):
    print("ERROR(8)")
    raise

print("** OK **")


