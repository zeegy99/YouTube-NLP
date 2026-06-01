import feedparser
import csv
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import sys 
import re 

channels = [
    {"name": "Atrioc", "channel_id": "UCgv4dPk_qZNAbUW9WkuLPSA"}

]

def new_video_transcript(channel_id):
    channel_link = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    d = feedparser.parse(channel_link)
 
    link = d.entries[0].link 

    video_id = get_video_id(link)

    video_transcript = YouTubeTranscriptApi().fetch(video_id)
 
    return video_transcript

def get_video_id(link):
    watch = link.find('?v=')
    video_id = link[watch + 3:]




if __name__ == "__main__":
    a = check_new_videos('', channels['name' == 'atrioc']['channel_id'])
    print(a)