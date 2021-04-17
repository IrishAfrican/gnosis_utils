import string
from os import sep
s = string
d = sep.join(sep.split(__file__)[:-1])+sep
_ = lambda f: s.rstrip(open(d+f).read())
l = lambda f: s.split(_(f),'\n')

try:
    __doc__ = _('README')
except:
    pass
