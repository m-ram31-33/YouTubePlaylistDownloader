from yt_dlp import YoutubeDL
import pandas as pd
import re

# Get playlist URL from user
p = input("Enter URL of Playlist: ")

# Initialize a list to store video metadata
data = []

try:
    # yt-dlp options to fetch playlist information
    ydl_opts = {
        'quiet': True,
        'extract_flat': True  # To list videos without downloading
    }

    # Fetch the playlist data
    with YoutubeDL(ydl_opts) as ydl:
        playlist_info = ydl.extract_info(p, download=False)

    if not playlist_info or 'entries' not in playlist_info:
        raise Exception("Failed to fetch playlist information. Ensure the URL is correct.")

    # Print playlist information
    print("\nPlaylist Name:", playlist_info['title'])
    print("No. of Videos:", len(playlist_info['entries']))

    # Sanitize playlist name for filename (remove illegal characters)
    sanitized_playlist_name = re.sub(r'[\\/*?:"<>|]', "", playlist_info['title'])

    # Iterate through each video entry
    for i, entry in enumerate(playlist_info['entries']):
        video_url = entry['url']
        try:
            # Fetch detailed video info
            with YoutubeDL() as ydl:
                video_info = ydl.extract_info(video_url, download=False)

            # Extract video metadata
            title = video_info.get('title', 'Unknown')
            views = video_info.get('view_count', 'Unknown')
            upload_date = video_info.get('upload_date', 'Unknown')
            channel_name = video_info.get('uploader', 'Unknown')

            # Format upload date
            if upload_date != 'Unknown':
                upload_date = f"{upload_date[:4]}-{upload_date[4:6]}-{upload_date[6:]}"

            # Append video information as a dictionary
            data.append({
                'Title': title,
                'Link': video_url,
                'Views': views,
                'Upload Date': upload_date,
                'Channel Name': channel_name
            })

            # Display progress
            print(f"Fetched {i + 1}/{len(playlist_info['entries'])}: {title} by {channel_name}")

        except Exception as e:
            print(f"Failed to fetch data for {video_url}: {e}")

    # Create DataFrame from the list of dictionaries
    dataframe = pd.DataFrame(data)

    # Automatically generate filename based on playlist name
    filename = sanitized_playlist_name + ".xlsx"

    # Save the DataFrame to an Excel file
    dataframe.to_excel(filename, index=False)

    print(f"\nPlaylist metadata extracted and saved to '{filename}' successfully.")

except Exception as e:
    print(f"Failed to process the playlist: {e}")
