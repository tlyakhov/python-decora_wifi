# python-decora_wifi
Python Library for Interacting with [Leviton Decora](http://www.leviton.com/en/products/lighting-controls/decora-smart-with-wifi) Smart WiFi Switches &amp; Dimmers.

The code is reverse engineered from the myLeviton Android app and includes an "API scraper" python script that generates model classes for invoking Leviton Cloud Services REST APIs.

See `cli-test.py` for a usage example.

Create a session first:
```
session = DecoraWiFiSession()
session.login(decora_email, decora_pass)
```

After that, the logged in user is accessible in `session.user`.

To get the user's residences, go through the ResidentialPermissions model like this:
```
perms = session.user.get_residential_permissions() # Usually just one of these

for permission in perms:
  acct = ResidentialAccount(session, permission.residentialAccountId)
  residences = acct.get_residences()
```

Now from each residence, you can get a list of switches:
```
  for residence in residences:
    switches = residence.get_iot_switches()
    for switch in switches:
      print(switch)
```

Other useful methods:
* `switch.update_attributes({'power': 'ON', 'brightness': 75})` - Turn switch ON or OFF, change brightness. Print out your switch attributes to see what's available.
* `switch.refresh()` - Refresh this model's data from the server.
* `Person.logout(session)` - Log out from LCS.

Notes:
* Create/delete methods are untested. I was only interested in get/update methods for HASS integration. Feel free to submit a pull if something doesn't work.
* This code uses the HTTPS interface to LCS, I believe there's also a websocket one, but I haven't investigated it.
