#!/usr/bin/env python
import Globals
import sys
from Products.ZenUtils.ZenScriptBase import ZenScriptBase
from transaction import commit

usage = 'prodStateFixer.py <check|fix> \n'

# check args
if len(sys.argv) != 2:
    print usage
    sys.exit(1)
elif sys.argv[1] not in ['check', 'fix']:
    print usage
    sys.exit(1)
   
   
# connect to ZenScriptBase once args are confirmed valid
dmd = ZenScriptBase(connect=True).dmd

# check to see if devices except out when trying to fetch prodState, add them to a list if they do
print 'Checking devices...'
broken_devices = []
for d in dmd.Devices.getSubDevicesGen():
    try:
      dps = d.getProductionState()
    except:
      print '>>> Device %s is missing its production state' % d.id
      broken_devices.append(d)

if len(broken_devices) == 0:
    print 'No devices to fix.'
    sys.exit(1)
      
# if the arg is 'fix' then set their prodState to 1000 (production)
if sys.argv[1] == 'fix':
    print 'Cleaning devices...'
    for d in broken_devices:
        print 'Setting %s to production' % d.id
        d._setProductionState(1000)
        commit()