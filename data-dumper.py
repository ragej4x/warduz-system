import os
import time
import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
#access nyo ung dropbox @aczontongao
TOKEN_FILE = 'access_token.txt'

def authenticate_dropbox_oauth():
    APP_KEY = '3pms6miqqdm0p9r' 
    APP_SECRET = '1e0loz2tlln027w'  

    auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

    authorize_url = auth_flow.start()
    print("1. Go to: " + authorize_url)
    print("2. Click 'Allow' (you might need to log in).")
    print("3. Copy the authorization code.")

    auth_code = input("Enter the authorization code here: ").strip()

    try:
        auth_result = auth_flow.finish(auth_code)
        access_token = auth_result.access_token
        print("New access token obtained.")

        with open(TOKEN_FILE, 'w') as token_file:
            token_file.write(access_token)
        return access_token
    except Exception as e:
        print(f"Failed to authenticate with Dropbox: {e}")
        return None

def get_access_token():
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token_file:
            token = token_file.read().strip()
            if token:
                return token
    return authenticate_dropbox_oauth()

def delete_access_token():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print("Invalid or expired access token deleted.")


'''test code'''

def upload_file_to_dropbox(file_path, dropbox_path, access_token):
    try:
        dbx = dropbox.Dropbox(access_token)

        dbx.users_get_current_account()

        if not os.path.exists(file_path):
            print(f"Error: Local file {file_path} does not exist.")
            return

        with open(file_path, "rb") as f:
            dbx.files_upload(f.read(), dropbox_path, mode=dropbox.files.WriteMode('overwrite'), mute=True)
            print(f"Uploaded: {file_path} to {dropbox_path}")
    except dropbox.exceptions.AuthError:
        print("Access token expired or invalid. Deleting token and reauthenticating...")
        delete_access_token()
        new_token = authenticate_dropbox_oauth()

        if new_token:
            upload_file_to_dropbox(file_path, dropbox_path, new_token)
        else:
            print("Failed to reauthenticate. Skipping upload.")

def main():
    access_token = get_access_token()
    if not access_token:
        print("Unable to retrieve or generate access token. Exiting...")
        return

    files_to_upload = {
        'live-monitor/ph_log_live.txt': '/live-monitor/ph_log_live.txt',
        'live-monitor/ph_log.txt': '/live-monitor/ph_log.txt',
        'live-monitor/temperature_log_live.txt': '/live-monitor/temperature_log_live.txt',
        'live-monitor/temperature_log.txt': '/live-monitor/temperature_log.txt',
        'access_token.txt': '/live-monitor/access_token.txt'
    }

    for local_path, dropbox_path in files_to_upload.items():
        upload_file_to_dropbox(local_path, dropbox_path, access_token)

if __name__ == '__main__':
    try:
        while True:
            print(f"Starting upload cycle at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            main()
            print(f"Upload cycle completed. Next cycle starts in 5 seconds.\n")
            time.sleep(5)
    except KeyboardInterrupt:
        print("Script interrupted. Exiting...")
