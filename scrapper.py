import spacy
from googleapiclient.discovery import build
import operator
import argparse
import os

api_key = 'YOUR_API_KEY'
youtube = build('youtube', 'v3', developerKey=api_key)
def fetch_top_videos(query):
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        order='relevance',  
        type='video',
        maxResults=10,
    ).execute()
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    
    video_response = youtube.videos().list(
        part='statistics',
        id=','.join(video_ids)
    ).execute()
    
    videos_with_likes = {}
    for item in video_response['items']:
        video_id = item['id']
        like_count = int(item['statistics'].get('likeCount', 0))  
        videos_with_likes[video_id] = like_count

    sorted_videos = sorted(videos_with_likes.items(), key=operator.itemgetter(1), reverse=True)
    # print(sorted_videos) to check out the video ids
    return [video[0] for video in sorted_videos[:3]]  



def fetch_comments_from_video(video_id, max_results=100):
    comments_with_likes = []
    # Fetch comments from the video
    response = youtube.commentThreads().list(
        part='snippet,replies',
        videoId=video_id,
        textFormat='plainText',
        maxResults=max_results,
        order='relevance'  # This brings pertinent comments to the top but not necessarily sorted by likes
    ).execute()
    # Collect all comments with their like counts
    for item in response['items']:
        comment_text = item['snippet']['topLevelComment']['snippet']['textDisplay']
        like_count = item['snippet']['topLevelComment']['snippet']['likeCount']
        comments_with_likes.append((comment_text, like_count))
    return comments_with_likes

def store_comments_to_file(comments, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        for comment_tuple in comments:
            comment_text = comment_tuple[0].replace('\n', ' ')  
            like_count = str(comment_tuple[1])  
            file.write(f"{comment_text}\t{like_count}\n")  
def run_scraper(query):
    
    top_videos = fetch_top_videos(query)
    return top_videos  
