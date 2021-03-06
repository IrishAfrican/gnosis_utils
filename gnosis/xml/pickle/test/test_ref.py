"Demonstrate what happens with/without DEEPCOPY  --fpm"

import gnosis.xml.pickle as xml_pickle
from gnosis.xml.pickle.util import setParanoia, setDeepCopy
from collections import UserList
import sys
from . import funcs

funcs.set_parser()

a = (1,2,3)
b = [4,5,6]
c = {'a':1,'b':2,'c':3,'d':[100,200,300]}
dd = c['d'] # make sure subitems get refchecked
uu = UserList([10,11,12])

u = UserList([[uu,c,b,a],[a,b,c,uu],[c,a,b,uu],dd])
#print u

# allow xml_pickle to read our namespace
setParanoia(0)

# by default, with references
x1 = xml_pickle.dumps(u)
#print x
#del u

g = xml_pickle.loads(x1)
#print g

if u != g:
    print("ERROR(1)")
    raise

# next, using DEEPCOPY
#print "------ DEEP COPY ------"
setDeepCopy(1)
x2 = xml_pickle.dumps(g)
#print x
#del g

z = xml_pickle.loads(x2)

# deepcopy version should be significantly larger
if (len(x2) - len(x1)) < 1000:
    print("ERROR(2)")
    raise

if z != g:
    print("ERROR(3)")
    raise

print("** OK **")


