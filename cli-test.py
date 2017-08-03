#!/usr/bin/python

from decora_wifi import *
import sys


if len(sys.argv) < 4:
    print('Usage: ./cli-test.py [email] [pass] [ON|OFF] [BRIGHTNESS 0-100]')

decora_email = sys.argv[1]
decora_pass = sys.argv[2]
decora_cmd = sys.argv[3]
if len(sys.argv) >= 5:
    decora_bright = int(sys.argv[4])
else:
    decora_bright = None

session = decora_wifi()
session.login(decora_email, decora_pass)

# Gather all the available devices...

perms = ResidentialPermission()
all_residences = []
for permission in perms:
    print("Permission: {}".format(permission))
    for res in session.residences(permission['residentialAccountId']):
        print("Residence: {}".format(res))
        all_residences.append(res)
all_switches = []
for residence in all_residences:
    for switch in session.iot_switches(residence['id']):
        print("Switch: {}".format(switch))
        attribs = {}
        if decora_bright is not None:
            attribs['brightness'] = decora_bright
        if decora_cmd == 'ON':
            print('ON!')
            attribs['POWER'] = 'ON'
            session.iot_switch_update(switch['id'], attribs)
        else:
            print('OFF!')
            attribs['POWER'] = 'OFF'
            session.iot_switch_update(switch['id'], attribs)

session.logout()

