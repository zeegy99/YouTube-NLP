import feedparser
import csv
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
import sys 
import re 
from pathlib import Path 
import os 
import json
import time 



def new_video_transcript(channel_id):
    channel_link = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    d = feedparser.parse(channel_link)
    
    if d:
        link = d.entries[0].link 

        video_id = get_video_id(link)
        video_title = d.entries[0].title

        video_transcript = YouTubeTranscriptApi().fetch(video_id)
    
        return video_transcript, video_title, link
    else:
        print(f'No Video Found For {channel_id}')
        return -1 

def get_video_id(link):
    watch = link.find('?v=')
    video_id = link[watch + 3:]

    return video_id

def write_to_transcript_csv(author, text, link):
    csv_path = os.path.join(os.path.dirname(__file__), '..', 'csv', 'transcripts.csv')
    with open(csv_path, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([author, text, link])

def transcript_to_text(transcript):
    transcript_text = ' '.join([snippet.text for snippet in transcript])
    return transcript_text

def edit_json(author, new_link):
   JSON_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache.json')
    
   with open(JSON_path, 'r') as file:
        cache = json.load(file)

   cache[author] = new_link

   with open(JSON_path, 'w') as file:
        json.dump(cache, file, indent=2)

def check_in_json(author, video_link):
    JSON_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache.json')
    with open(JSON_path, 'r') as file:
        cache = json.load(file)
        
        try:
            cache[author]
            return cache[author] == video_link

    
        except:
            return False 
        
if __name__ == "__main__":
    JSON_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'channels.json')
    with open(JSON_path, 'r') as file:
        channels = json.load(file)

        for channel in channels:
            time.sleep(2)

            channel_link = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel['channel_id']}"
            d = feedparser.parse(channel_link)
            if d.entries[0].link:
                video_link = d.entries[0].link
                

                if check_in_json(channel['name'], video_link):
                    print(f"{channel['name']}: no new video, skipping")
                    continue
                else:
                    video_transcript, video_title, video_link = new_video_transcript(channel["channel_id"])
                    edit_json(channel['name'], video_link)
                    write_to_transcript_csv(channel['name'], transcript_to_text(video_transcript), video_link)
