from flask import Flask, request, render_template, url_for, redirect
from Scraper import run_scraper, fetch_comments_from_video, store_comments_to_file
from Relevant_comment import process_file
from qa import generate_text_with_jurassic, load_comments
from flask import session, jsonify

app = Flask(__name__, template_folder='YOUR TEMPLATE FOLDER PATH')
app.secret_key = ''

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the search
@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    video_ids = run_scraper(query)  # Fetch video IDs based on the query
    all_comments = []
    for video_id in video_ids:
        comments = fetch_comments_from_video(video_id)  # Fetch comments for each video
        all_comments.extend(comments)
    
    # Store comments to a file
    comments_file_path = 'PATH TO \\comments.txt'
    store_comments_to_file(all_comments, comments_file_path)
    
    # Process and sort comments
    sorted_comments_file_path = 'PATH TO \\sorted.txt'
    process_file(comments_file_path, query, sorted_comments_file_path)
    
    # Redirect to a new route to display comments
    return redirect(url_for('display_comments'))

def load_comments(file_path):
    comments_with_likes = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # Split line into comment and like count
            parts = line.rsplit(' ', 1)  # Splitting from the right, since the like count is at the end
            if len(parts) == 2:
                comment, likes = parts
                comments_with_likes.append((comment.strip(), likes.strip()))
    return comments_with_likes

@app.route('/display_comments')
def display_comments():
    # Assuming process_file writes to sorted_comments.txt, load and display these comments
    sorted_comments = load_comments('PATH TO \\sorted.txt')
    return render_template('results.html', comments=sorted_comments)

@app.route('/ask_question', methods=['POST'])
def ask_question():
    """Handles form submission, generates answer, and renders the same page."""
    with open('PATH TO \\sorted.txt', 'r', encoding='utf-8') as file:
        comments = [line.strip() for line in file][:10]
    question = request.form['question']
    context = load_comments('PATH TO \\sorted.txt')
    prompt = f"Context: {context}\nQuestion: {question}"

    api_key = "YOUR API KEY"  # Replace with your Jurassic-1 Jumbo API key
    answer = None

    try:
        answer = generate_text_with_jurassic(prompt, api_key)  # Use jurrasic.generate_text for Jurassic-1 Jumbo
    except Exception as e:
        print(f"Error generating answer: {e}")
        answer = "An error occurred while generating the answer. Please try again later."

    return render_template('results.html',comments=comments ,question=question, answer=answer)

if __name__ == '__main__':
    app.run(debug=True)