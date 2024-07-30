import os
from dateutil import parser
from dotenv import load_dotenv
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
load_dotenv()

DEVELOPER_KEY = os.environ['YT_API_KEY']
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'


def ytsearch(query: str) -> str:
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                    developerKey=DEVELOPER_KEY)

    try:
        search_response = youtube.search().list(
            q=query,
            part='id,snippet',
            maxResults=3,
            type='video',
            order='relevance'
        ).execute()

    except HttpError as e:
        if e.resp.status == 403:
            raise Exception(
                "You have exceeded your daily quota for the YouTube API. Please try again tomorrow.")

    videos = []

    for response in search_response['items']:
        vidid = response['id']['videoId']

        video = youtube.videos().list(
            id=vidid,
            part='snippet,statistics'
        ).execute()

        videos.append(video['items'][0])

    return {
        'videos': videos,
    }
