from __future__ import print_function
from past.builtins import xrange
from StringIO import StringIO
import sys
import os
import pprint
import random

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '../')))
import mwclient

if len(sys.argv) < 3:
    print(sys.argv[0], 'username', 'password', '[host=test.wikipedia.org]', '[path=/w/]')
    sys.exit()
host = sys.argv[3] if len(sys.argv) > 3 else 'test.wikipedia.org'
path = sys.argv[4] if len(sys.argv) > 4 else '/w/'
site = mwclient.Site(host, path)
site.login(sys.argv[1], sys.argv[2])

name = (
    ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in xrange(8))
    + '.png'
)

print(f'Using http://{host}{path}index.php?title=File:{name}')
print('Regular upload test')

res = site.upload(open('test-image.png', 'rb'), name, 'Regular upload test', ignore=True)
pprint.pprint(res)
assert res['result'] == 'Success'
assert 'exists' not in res['warnings']

print('Overwriting; should give a warning')
res = site.upload(open('test-image.png', 'rb'), name, 'Overwrite upload test')
pprint.pprint(res)
assert res['result'] == 'Warning'
assert 'exists' in res['warnings']

ses = res['sessionkey']

print('Overwriting with stashed file')
res = site.upload(filename=name, filekey=ses)
pprint.pprint(res)
assert res['result'] == 'Warning'
assert 'duplicate' in res['warnings']
assert 'exists' in res['warnings']

print('Uploading empty file; error expected')
res = site.upload(StringIO(), name, 'Empty upload test')
