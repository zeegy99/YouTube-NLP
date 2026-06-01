import feedparser
import csv
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import sys 
import re 
from pathlib import Path 
import os 

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

    return video_id

def write_to_transcript_csv(author, text, link):
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'csv', 'transcripts.csv')
    with open('transcripts.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([author, text, link])


if __name__ == "__main__":
    a = new_video_transcript(channels['name' == 'atrioc']['channel_id'])
  