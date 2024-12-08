from pytube import Playlist, YouTube
import pandas as pd
import re

p = input("Enter URL of Playlist: ")

# Initialize a list to store video metadata
data = []

try:
    # Fetch the playlist using pytube
    vlinks = Playlist(p)

    print("\nPlaylist Name:", vlinks.title)
    print("No. of Videos:", len(vlinks.video_urls))  # Fix here

    # Sanitize playlist name for filename (remove illegal characters)
    sanitized_playlist_name = re.sub(r'[\\/*?:"<>|]', "", vlinks.title)

    # Use video_urls to fetch links
    for i, link in enumerate(vlinks.video_urls):
        try:
            # Fetch individual video information using YouTube class
            yt = YouTube(link)
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

            # Display progress
            print(f"Fetched {i + 1}/{len(vlinks.video_urls)}: {title} by {channel_name}")

        except Exception as e:
            print(f"Failed to fetch data for {link}: {e}")

    # Create DataFrame from the list of dictionaries
    dataframe = pd.DataFrame(data)

    # Automatically generate filename based on playlist name
    filename = sanitized_playlist_name + ".xlsx"

    # Save the DataFrame to an Excel file
    dataframe.to_excel(filename, index=False)

    print(f"Playlist metadata extracted and saved to {filename} successfully.")

except Exception as e:
    print(f"Failed to process the playlist: {e}")
