from transformers import BertTokenizer, BertModel
import torch
from scipy.spatial.distance import cosine
import spacy




# Load models and tokenizers outside the function to avoid reloading them on each call
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')
nlp = spacy.load("en_core_web_sm")


def just_keyword(query):
    doc = nlp(query)
    noun_chunks = list(doc.noun_chunks)
    return noun_chunks[0].root.text
   


def generate_bert_embedding(text):
    input_ids = tokenizer.encode(text, add_special_tokens=True)
    input_tensor = torch.tensor(input_ids).unsqueeze(0)
    with torch.no_grad():
        outputs = model(input_tensor)
        embeddings = outputs[0].squeeze(0).mean(dim=0).numpy()
    return embeddings

def calculate_cosine_similarity(vec1, vec2):
    return 1 - cosine(vec1, vec2)

def process_file(file_path, query, output_file, threshold=0.6):
    # Extract keywords from query
    doc = nlp(query)
    keywords = [token.text for token in doc if token.pos_ in ['NOUN', 'PROPN']]
    print(f"Processing new file for query: {query}") 

    with open(file_path, 'r', encoding='utf-8') as file, open(output_file, 'w', encoding='utf-8') as output:
        for line in file:
           
            parts = line.strip().split('\t')
            if len(parts) >= 2:
                comment, like_count = parts[0], parts[1]
            else:
                
                continue
            keyword_present = any(keyword.lower() in comment.lower() for keyword in keywords)
            comment_embedding = generate_bert_embedding(comment)
            query_embedding = generate_bert_embedding(query)
            similarity = calculate_cosine_similarity(query_embedding, comment_embedding)

            if keyword_present or similarity >= threshold:
                output.write(f"{comment}\t{like_count}\n")


def calculate_similarity_score(query, comment):
    query_embedding = generate_bert_embedding(query)
    comment_embedding = generate_bert_embedding(comment)
    similarity = calculate_cosine_similarity(query_embedding, comment_embedding)
    return similarity

