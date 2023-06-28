"""
This file contains functions that uses the YouTube Data API v3 
to scrape data from a given list of provided channels.

Adapted from: https://github.com/thu-vu92/youtube-api-analysis
"""

def get_channel_stats(youtube,channel_ids):
    """
    Get channel statistics of given channels
    Params: youtube: build object from googleapiclient.discovery,
            channel_ids: list of youtube channel ids.
    Returns: list containing channel statistics for all channels provided in the lists.
             the statistics are: title, published date, view count, subscriber count, video count, uploads playlist
             
    """
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=','.join(channel_ids))
    response = request.execute()
    
    all_data = []
    for item in response['items']:
        data = dict(ChannelName = item['snippet']['title'],
                    ChannelDescription = item['snippet']['description'],
                    PublishedDate = item['snippet']['publishedAt'],
                    TotalSubscribers = item['statistics']['subscriberCount'],
                    TotalViews = item['statistics']['viewCount'],
                    TotalVideos = item['statistics']['videoCount'],
                    playlistID = item['contentDetails']['relatedPlaylists']['uploads']
                    )
        all_data.append(data)
    
    return all_data


def get_video_ids(youtube,playlist_id):
    
    """
    Get list of video ids of all videos in the provided playlist
    Params: youtube: build object of googleapiclient.discovery
            playlist_id: playlist Id of the channel
    Returns: list of video ids of all videos in the playlist
    
    """
    request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=50,
            playlistId = playlist_id)
    response = request.execute()
    
    video_ids = []
    for item in response['items']:
        video_ids.append(item['contentDetails']['videoId'])
        
    next_page_token = response.get('nextPageToken')
    more_pages = True
    
    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part="contentDetails",
                maxResults=50,
                playlistId = playlist_id,
                pageToken = next_page_token)
            response = request.execute()
        
            for item in response['items']:
                video_ids.append(item['contentDetails']['videoId'])
                
            next_page_token = response.get('nextPageToken')
    
    return video_ids


def get_video_stats(youtube, list_video_ids):
    
    """
    Get all desired video stats of given video
    Params: youtube: build object from googleapiclient.discovery
            list_of_video_ids: list of videos ids
    Returns: list containing the following video stats: 
                'channelTitle', 'title', 'description', 'tags', 'publishedAt',
                'viewCount', 'likeCount', 'favouriteCount', 'commentCount', 'duration', 'definition'
            None value is given for any stat not available for a given video
    
    """
    all_video_stats = []
    
    for i in range(0,len(list_video_ids),50):
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id = ','.join(list_video_ids[i:i+50]))
        response = request.execute()
    
        for video in response['items']:
            stats_to_keep = {'snippet': ['channelTitle', 'title', 'description', 'tags', 'publishedAt'],
                             'statistics': ['viewCount', 'likeCount', 'favouriteCount', 'commentCount'],
                             'contentDetails': ['duration', 'definition']
                            }
            video_stats = {}
            video_stats['video_id'] = video['id']
            
            for k in stats_to_keep.keys():
                for v in stats_to_keep[k]:
                    try:
                        video_stats[v] = video[k][v]
                    except:
                        video_stats[v] = None
        
            all_video_stats.append(video_stats)
                             
    return all_video_stats



