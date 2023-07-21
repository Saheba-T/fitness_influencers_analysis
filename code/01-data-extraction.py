

import os
import pandas as pd
import youtube_scraping_functions as ytfuns  # Module to scrape channels and videos

from os.path import dirname, abspath
from googleapiclient.discovery import build  # Google API
from IPython.display import JSON             # Disply JSON
from functools import partial                # Use with Map to fix an argument


# API Key generated from Google Cloud
api_key = input("Please provide the API key generated from Google Console: ")

# List of channels ids of the 5 fitness channel which was found from their respective youtube channel url
channel_ids = ['UCpQ34afVgk8cRQBjSJ1xuJQ', # MadFit
               'UCvGEK5_U-kLgO6-AMDPeTUQ', # EmiWong
               'UCIJwWYOfsCfz6PjxbONYXSg', # Blogilates
               'UCCgLoMYIyP0U56dEhEL1wXQ', # ChloeTing
               'UCi0AqmA_3DGPFCu5qY0LLSg', # Rebecca-Louise
              ]

# Get credentials and create an API client
youtube = build("youtube", "v3", developerKey=api_key)

# get channel data and convert to dataframe
channels_df = pd.DataFrame(ytfuns.get_channel_stats(youtube, channel_ids))

# create empty dataframe to store video data
video_df = pd.DataFrame()

# Create a dataframe of video statistics of all videos from all the channels
for c in channels_df['ChannelName'].unique():
    print("Getting video information from channel: " + c)
    playlist_id = channels_df.loc[channels_df['ChannelName']== c, 'playlistID'].iloc[0]
    
    # get list of video ids of all videos in the channel
    video_ids = ytfuns.get_video_ids(youtube, playlist_id)
    
    # get video statistics of each video in the channel
    video_data = pd.DataFrame(ytfuns.get_video_stats(youtube, video_ids))

    # concat video data of the channel to the dataframe
    video_df = pd.concat([video_df,video_data], ignore_index=True)
    
# Save dataframes as csv files 
project_dir = project_dir = dirname(dirname(abspath("01-data-extraction.py")))
channels_df.to_csv(project_dir + "/data/raw/fitness_channels_2023_07_11.csv", index=False)
video_df.to_csv(project_dir + "/data/raw/fitness_videos_2023_07_11.csv", index=False)