import feedparser
import csv
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd


def check_new_videos(channel_name, channel_id):
    feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed = feedparser.parse(feed_url)
    if feed.entries:
        current_video = feed.entries[0]  
        df = pd.read_csv('C:/Users/fredy/Downloads/Stream Analyzer/for_tft/prev_vod.csv')
        df = df['YT Channel'] == channel_name
     
        video_id = (current_video.link[current_video.link.find('=') + 1:])

        return (video_id, current_video.link)

def write_into_csv():
    with open('prev_vod.csv', 'w', newline='') as file:
        writer = csv.writer(file)

        writer.writerow(['YT Channel', 'Link'])

def append_into_csv(channel_name, link):
    with open('prev_vod.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([channel_name, link])


def get_transcript(link):
    video_id = check_new_videos(link)

    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)
    return fetched_transcript

def write_to_csv(fetched_transcript, video_id):
    unfiltered = ''
    with open('new.csv', mode = 'w') as csvfile:
        fieldnames = ['text', 'start', 'duration']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for snippet in fetched_transcript:
            unfiltered += ' ' + snippet.text
            writer.writerow({"text": snippet.text, "start": snippet.start, "duration": snippet.duration})

    with open('storage.csv', mode='w') as csvfile:
        fieldnames = ['transcript', 'video_id', 'creator']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'transcript': unfiltered, 'video_id': video_id})

def break_into_games(): #How to determine when a game fully ends? Probably around 30 minutes, probably around some type of time-break?
    #Maybe through pure ML?
    #Maybe through some screen-capture?

    
    pass

# def content_analysis():
    
#     model_name = "bert-base-uncased" 
#     tokenizer = AutoTokenizer.from_pretrained(model_name)
#     model = AutoModelForMaskedLM.from_pretrained(model_name)

#     tft_terms = [
#         "reroll", "hyperroll", "slowroll", "econ", "carousel", 
#         "augment", "BiS", "3-star", "4-cost", "5-cost",
#         "frontline", "backline", "itemize", "positioning",
#         "comp", "synergy", "trait", "emblem", "spatula"
#     ]

#     num_added = tokenizer.add_tokens(tft_terms)
#     model.resize_token_embeddings(len(tokenizer))
#     print(f"Added {num_added} new tokens")

def clean_storage(enum):
    pass


def read_storage(enum): #starts at 0

    df = pd.read_csv('C:/Users/fredy/Downloads/Stream Analyzer/for_tft/storage.csv', encoding='latin-1')
    return (df.iloc[enum]['trasnscript'], df.iloc[enum]['video_id'], df.iloc[enum]['creator']) #transcript,video_id,creator

wasian = "UC_bm47pgX4DSl7k-nPYMOWw"

print('hi')




