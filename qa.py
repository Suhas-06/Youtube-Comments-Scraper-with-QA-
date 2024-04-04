
import requests

def load_comments(filepath):
    """Load comments from a file and return as a single string."""
    comments = []
    with open(filepath, 'r', encoding='utf-8') as file:
        for line in file:
            comment, _ = line.strip().split('\t') 
            comments.append(comment)
    return " ".join(comments)


def generate_text_with_jurassic(prompt, api_key):
    url = "https://api.ai21.com/studio/v1/j2-mid/complete"# Ensure this is correct
    
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


