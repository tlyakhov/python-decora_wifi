#!/usr/bin/python

from decora_wifi import DecoraWiFiSession
from decora_wifi.models.person import Person
from decora_wifi.models.residential_account import ResidentialAccount
from decora_wifi.models.residence import Residence
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
print('{} premissions'.format(len(perms)))
all_residences = []
for permission in perms:
    print("Permission: {}".format(permission))
    if permission.residentialAccountId is not None:
        acct = ResidentialAccount(session, permission.residentialAccountId)
        for res in acct.get_residences():
            print("Residence: {}".format(res))
            all_residences.append(res)
    elif permission.residenceId is not None:
        res = Residence(session, permission.residenceId)
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
            attribs['power'] = 'ON'
        else:
            print('OFF!')
            attribs['power'] = 'OFF'
        switch.update_attributes(attribs)

Person.logout(session)

