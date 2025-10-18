# Note: Before running this script, install the required libraries:
# pip install sentence-transformers faiss-cpu

import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss

def load_json(file_path):
    """Load JSON data from a file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_embeddings(texts, model):
    """Get embeddings for a list of texts."""
    return model.encode(texts)

def prepare_resume_texts(resume_data):
    """Combine resume sections into texts for embedding."""
    skills = " ".join(resume_data['skills'])
    education = " ".join(resume_data['education'])
    experience = " ".join(resume_data['experience'])
    return [skills, education, experience]

def prepare_vacancy_texts(vacancy):
    """Combine vacancy requirements into a single text."""
    requirements = " ".join(vacancy['requirements'])
    return requirements

def find_best_vacancies(resume_file, vacancies_file, top_n=5):
    """Find the top N best matching vacancies using vector DB."""
    # Load data
    resume = load_json(resume_file)
    vacancies = load_json(vacancies_file)
    
    # Load multilingual model for Russian/English support
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    
    # Prepare resume embeddings (average of sections)
    resume_texts = prepare_resume_texts(resume)
    resume_embs = get_embeddings(resume_texts, model)
    resume_emb = np.mean(resume_embs, axis=0).reshape(1, -1)
    resume_emb = resume_emb / np.linalg.norm(resume_emb)  # Normalize
    
    # Prepare vacancy texts and embeddings
    vacancy_texts = [prepare_vacancy_texts(v) for v in vacancies]
    vacancy_embs = get_embeddings(vacancy_texts, model)
    vacancy_embs = vacancy_embs / np.linalg.norm(vacancy_embs, axis=1, keepdims=True)  # Normalize
    
    # Create FAISS index
    dimension = vacancy_embs.shape[1]
    index = faiss.IndexFlatIP(dimension)  # Inner Product for cosine similarity
    index.add(vacancy_embs)
    
    # Search for top matches
    distances, indices = index.search(resume_emb, top_n)
    
    # Collect results
    best_vacancies = []
    for dist, idx in zip(distances[0], indices[0]):
        vac = vacancies[idx]
        best_vacancies.append({
            'id': vac['id'],
            'name': vac['name'],
            'score': dist,  # Cosine similarity
            'requirements': vac['requirements']
        })
    
    return best_vacancies

# Example usage
if __name__ == "__main__":
    resume_file = 'resume.json'  # Replace with actual file path
    vacancies_file = 'vacancies.json'  # Replace with actual file path
    best_vacancies = find_best_vacancies(resume_file, vacancies_file, top_n=5)
    
    print("Top matching vacancies:")
    for vac in best_vacancies:
        print(f"ID: {vac['id']}, Name: {vac['name']}, Score: {vac['score']:.4f}")
        print("Requirements:", vac['requirements'])
        print("-" * 40)