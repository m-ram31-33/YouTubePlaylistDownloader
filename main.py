# Used the following youtube link for this package
# https://www.youtube.com/watch?v=3jOBpLN_nAQ

# pip install pytube
# pip install openpyxl

from pytube import Playlist, YouTube
import pandas as pd

p=input("Enter URL of Playlist=")

vlinks=Playlist(p)

print("\n Playlist Name=", vlinks.title)
print("No. of Videos=", vlinks.length)
print("Playlist ID=", vlinks._playlist_id)
#print("Playlist Description=\n", vlinks.description)

dict={'Title': [], 'Link': []}
dataframe=pd.DataFrame(dict)

vtitles=[]

for link in vlinks:
    vtitles.append(YouTube(link).title)

#def new_func(vlinks, dataframe, vtitles):
dataframe['Title']=vtitles
dataframe['Link']=vlinks

dataframe.to_excel("playlist.xlsx")

print("Playlist Extracted Successfully")

#new_func(vlinks, dataframe, vtitles)

