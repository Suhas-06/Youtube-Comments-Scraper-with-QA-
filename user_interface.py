
from flask import Flask, request, render_template, url_for, redirect
from scrapper import run_scraper, fetch_comments_from_video, store_comments_to_file
from relc import process_file,just_keyword
from qa1 import generate_text_with_jurassic, load_comments
from flask import session, jsonify
import requests


app = Flask(__name__)
app.secret_key = 'sparsh'



@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    print(f"Comments stored for query: {query}")  
    video_ids = run_scraper(query)  # Fetch video IDs based on the query
    all_comments = []
    for video_id in video_ids:
        comments = fetch_comments_from_video(video_id)  # Fetch comments for each video
        all_comments.extend(comments)
    
    # Store comments to a file
    comments_file_path = ''
    store_comments_to_file(all_comments, comments_file_path)
    
    # Process and sort comments
    sorted_comments_file_path = ''
    process_file(comments_file_path, query, sorted_comments_file_path)
    
    # Redirect to a new route to display comments
    return redirect(url_for('display_comments'))


def load_comments(file_path):
    comments_with_likes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            
            parts = line.rsplit(' ', 1) 
            if len(parts) == 2:
                comment, likes = parts
                comments_with_likes.append((comment.strip(), likes.strip()))
    return comments_with_likes


def get_pexels_image_url(keyword):
    pexels_api_key = 'YOUR_PEXELS_API_KEY'
    headers = {
        'Authorization': pexels_api_key
    }
    url = f'https://api.pexels.com/v1/search?query={keyword}&per_page=1'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data['photos']:
            
            return data['photos'][0]['src']['original']
    return None 

@app.route('/display_comments')
def display_comments():
    
    sorted_comments = load_comments('')#path of sorted_comments
    return render_template('results.html', comments=sorted_comments)



@app.route('/ask_question', methods=['POST'])
def ask_question():
    
    question = request.form['question']
    theme=just_keyword(question) 
    return redirect(url_for('generate_answer', question=question,theme=theme))

@app.route('/generate_answer')
def generate_answer():
    
    question = request.args.get('question')
    api_key = "YOUR_AI21_API_KEY"
    theme = request.args.get('theme')  
    background_image_url = get_pexels_image_url(theme) 

    print(theme)#check out the theme being sent to pexels api
    context = load_comments('')#paste the cd
    prompt = f"Context: {context}\nQuestion: {question}" 
    answer = generate_text_with_jurassic(prompt, api_key)
    return render_template('answer.html', question=question, answer=answer,background_image_url=background_image_url)


if __name__ == '__main__':
    app.run(debug=True)
