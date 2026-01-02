

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

def normalize(text: str) -> str:
    """Normalize text: lowercase, remove punctuation, fix smart quotes"""
    text = text.lower()
    text = text.replace("’", "'")               # smart quote
    text = re.sub(r"[^\w\s]", " ", text)       # remove punctuation
    text = re.sub(r"\s+", " ", text)           # remove extra spaces
    return text.strip()

class KnowledgeRetriever:
    def __init__(self, documents):
        """
        documents: list of dicts with 'title' and 'content' keys
        """
        self.docs = documents
        self.texts = [normalize(f"{d['title']} {d['content']}") for d in documents]

        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),  # capture single + 2-word phrases
            min_df=1
        )

        self.vectors = self.vectorizer.fit_transform(self.texts)

    def retrieve(self, query, top_k=2):
        q_vec = self.vectorizer.transform([normalize(query)])
        scores = cosine_similarity(q_vec, self.vectors)[0]

        # Threshold instead of exact 0
        if scores.max() < 0.15:
            return []

        idx = scores.argsort()[-top_k:][::-1]
        return [self.docs[i] for i in idx]
