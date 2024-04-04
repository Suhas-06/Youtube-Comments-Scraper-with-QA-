import spacy
from googleapiclient.discovery import build
import operator
import argparse

# Initialize the YouTube API and sentiment analysis pipeline
api_key = 'YOUR API KEY'
youtube = build('youtube', 'v3', developerKey=api_key)

def fetch_top_videos(query):
    search_response = youtube.search().list(
        q=query,
        part='snippet',
        order='relevance',  # You might want to order by 'viewCount' or another metric
        type='video',
        maxResults=10,
    ).execute()
    # Extract video IDs from search response
    video_ids = [item['id']['videoId'] for item in search_response['items']]
    # Fetch video details to get likes
    video_response = youtube.videos().list(
        part='statistics',
        id=','.join(video_ids)
    ).execute()
    # Sort videos by likes and return top video IDs
    videos_with_likes = {
      item['id']: int(item.get('statistics', {}).get('likeCount', 0))
      for item in video_response['items']
    }
    sorted_videos = sorted(videos_with_likes.items(), key=operator.itemgetter(1), reverse=True)
    #print(sorted_videos)
    return [video[0] for video in sorted_videos[:3]]  # Return top 3 video IDs

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
            comment_text = comment_tuple[0].replace('\n', ' ').replace('\r', '').strip()  # Replace newline characters
            like_count = str(comment_tuple[1])  # Accessing the like count and converting it to a string
            file.write(f"{comment_text}\t{like_count}\n")  # Writing comment and like count in tab-separated format

def run_scraper(query):
    # Assuming fetch_top_videos is the function that initiates the scraping process
    top_videos = fetch_top_videos(query)
    return top_videos