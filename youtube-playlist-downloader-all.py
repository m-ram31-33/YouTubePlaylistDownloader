from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pandas as pd
import pytube
import re
import os

# Scopes for accessing YouTube account
SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']


def authenticate_youtube():
    # Authenticate and get credentials
    flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube


def get_playlists(youtube):
    # Get all playlists from the user's account
    request = youtube.playlists().list(
        part='snippet,contentDetails',
        mine=True,  # Gets the authenticated user's playlists
        maxResults=50  # Adjust as needed (pagination is possible)
    )
    response = request.execute()
    playlists = response.get('items', [])

    return playlists


def download_playlist_metadata(playlist_id, playlist_title):
    data = []
    vlinks = pytube.Playlist(f'https://www.youtube.com/playlist?list={playlist_id}')

    print(f"Fetching metadata for playlist: {playlist_title}")

    for i, link in enumerate(vlinks.video_urls):
        try:
            yt = pytube.YouTube(link)
            title = yt.title
            views = yt.views
            upload_date = yt.publish_date.strftime("%Y-%m-%d") if yt.publish_date else "Unknown"
            channel_name = yt.author  # Fetch channel name

            # Append video information as a dictionary
            data.append({
                'Title': title,
                'Link': link,
                'Views': views,
                'Upload Date': upload_date,
                'Channel Name': channel_name
            })

            print(f"Fetched {i + 1}/{len(vlinks.video_urls)}: {title} by {channel_name}")

        except Exception as e:
            print(f"Failed to fetch data for {link}: {e}")

    # Create DataFrame from the list of dictionaries
    dataframe = pd.DataFrame(data)

    # Sanitize playlist name for filename (remove illegal characters)
    sanitized_playlist_name = re.sub(r'[\\/*?:"<>|]', "", playlist_title)

    # Save the DataFrame to an Excel file
    filename = sanitized_playlist_name + ".xlsx"
    dataframe.to_excel(filename, index=False)

    print(f"Playlist metadata extracted and saved to {filename} successfully.")


def main():
    # Authenticate and build the API client
    youtube = authenticate_youtube()

    # Fetch all playlists from the account
    playlists = get_playlists(youtube)

    # Iterate through all playlists and download metadata
    for playlist in playlists:
        playlist_id = playlist['id']
        playlist_title = playlist['snippet']['title']
        download_playlist_metadata(playlist_id, playlist_title)


if __name__ == '__main__':
    main()
