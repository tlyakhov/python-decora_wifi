#!/usr/bin/python

from decora_wifi import DecoraWiFiSession
from decora_wifi.models.person import Person
from decora_wifi.models.residential_account import ResidentialAccount
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

session = DecoraWiFiSession()
session.login(decora_email, decora_pass)

# Gather all the available devices...

perms = session.user.get_residential_permissions()
all_residences = []
for permission in perms:
    print("Permission: {}".format(permission))
    acct = ResidentialAccount(session, permission.data['residentialAccountId'])
    for res in acct.get_residences():
        print("Residence: {}".format(res))
        all_residences.append(res)
all_switches = []
for residence in all_residences:
    for switch in residence.get_iot_switches():
        print("Switch: {}".format(switch))
        attribs = {}
        if decora_bright is not None:
            attribs['brightness'] = decora_bright
        if decora_cmd == 'ON':
            print('ON!')
            attribs['POWER'] = 'ON'
        else:
            print('OFF!')
            attribs['POWER'] = 'OFF'
        switch.update_attributes(attribs)

Person.logout(session)

