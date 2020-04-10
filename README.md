# PAN-GP-DisconnectUser
Disconnect user who connects to GP from multiple computer at a time

Run this script against your current Firewall, please prepare below information:
- Your Global Protect gateway name: Network > Global Protect > Gateway and mark down the name.
- Admin credential of the Firewall with full API permission (operation command API at least)

How to run it:
- python3 pangp-disconnect.py

Or you can hard coded the Firewall IP address, username, password and GP Gateway name, then set schedule to run this script periodically (e.g once every 15 minutes) to wipe all users who violate the policy.

Enjoy.
