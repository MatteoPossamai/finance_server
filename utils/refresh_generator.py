#!/usr/bin/env python3

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dotenv import load_dotenv
import os

"""
Populate your app key in order to run this locally
"""

load_dotenv()
APP_KEY = os.getenv("DROPBOX_APP_KEY")
APP_SEC = os.getenv("DROPBOX_APP_SECRET")

auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, use_pkce=True, token_access_type="offline")

authorize_url = auth_flow.start()
print("1. Go to: " + authorize_url)
print('2. Click "Allow" (you might have to log in first).')
print("3. Copy the authorization code.")
auth_code = input("Enter the authorization code here: ").strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception as e:
    print("Error: %s" % (e,))
    exit(1)

print(oauth_result.refresh_token)
with dropbox.Dropbox(
    oauth2_refresh_token=oauth_result.refresh_token, app_key=APP_KEY, app_secret=APP_SEC
) as dbx:
    dbx.users_get_current_account()
    print("Successfully set up client!")
