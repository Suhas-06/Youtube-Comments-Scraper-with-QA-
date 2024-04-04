import requests
import sys
def load_comments(filepath):
    """Load comments from a file and return as a single string."""
    comments = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            comment, _ = line.strip().split('\t')  # Assumes 'comment\tlike_count' format
            comments.append(comment)
    return " ".join(comments)

def generate_text_with_jurassic(prompt, api_key):
    url = "YOUR API KEY"# Ensure this is correct
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    
    data = {
        "prompt": prompt,
        "maxTokens": 100,
        "temperature": 0.7,
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        print(f"API Error: {response.status_code}")
        print(f"API Response: {response.json()}")
        return "An error occurred while processing the API response."

    result = response.json()

    try:
        return result['completions'][0]['data']['text']
    except KeyError:
        print("KeyError: The expected keys were not found in the response.")
        print("API Response:", result)
        return "An error occurred while processing the API response."

def main():
    # Specify the path to your comments file
    file_path = "ADD FILE PATH"

    # Load comments from the file
    comments = load_comments(file_path)

    # Combine the comments with your question to form the prompt
    question = " "
    prompt = f"Context: {comments}\nQuestion: {question}"
    #print(prompt)
    # Your AI21 API key
    api_key = "YOUR API KEY"

    # Generate a response based on the combined prompt
    response_text = generate_text_with_jurassic(prompt, api_key)
    return response_text

if __name__ == "__main__":
    print(main())