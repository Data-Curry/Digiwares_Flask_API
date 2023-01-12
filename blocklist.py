"""
blocklist.py

This file contains the blocklist of the JWT tokens.
It's imported by the app and the logout resource so that tokens can be added to the blocklist when the user logs out.
"""

BLOCKLIST = set()
