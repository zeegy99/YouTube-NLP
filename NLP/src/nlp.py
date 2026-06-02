import pandas as pd
from collections import Counter
import re
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from gensim.models import Word2Vec
from transformers import (
    AutoTokenizer, 
    AutoModelForMaskedLM,
    DataCollatorForLanguageModeling,
    TrainingArguments,
    Trainer
)

class UnsupervisedTFTAnalyzer:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path, encoding='latin-1')
        self.df['text'] = self.df['text'].fillna('')
        self.entities = None
        self.w2v_model = None
        self.topics = None
    
    def discover_entities(self):
        """Find all important terms automatically"""
        # N-grams
        vectorizer = CountVectorizer(
            ngram_range=(1, 3),
            max_features=500,
            stop_words='english',
            min_df=5
        )
        
        ngram_matrix = vectorizer.fit_transform(self.df['text'])
        phrases = vectorizer.get_feature_names_out()
        frequencies = ngram_matrix.sum(axis=0).A1
        
        self.entities = dict(zip(phrases, frequencies))
        return sorted(self.entities.items(), key=lambda x: x[1], reverse=True)
    
    def train_embeddings(self):
        """Learn word relationships"""
        sentences = [text.lower().split() for text in self.df['text']]
        self.w2v_model = Word2Vec(sentences, vector_size=100, window=5, min_count=10)
        return self.w2v_model
    
    def discover_topics(self, n_topics=10):
        """Find topic clusters"""
        tfidf = TfidfVectorizer(max_features=500, stop_words='english', min_df=5)
        tfidf_matrix = tfidf.fit_transform(self.df['text'])
        
        lda = LatentDirichletAllocation(n_components=n_topics, random_state=42)
        lda.fit(tfidf_matrix)
        
        feature_names = tfidf.get_feature_names_out()
        topics = []
        for topic in lda.components_:
            top_idx = topic.argsort()[-15:][::-1]
            topics.append([feature_names[i] for i in top_idx])
        
        self.topics = topics
        return topics
    
    def find_similar_terms(self, term, top_n=10):
        """Find similar terms using embeddings"""
        if self.w2v_model and term in self.w2v_model.wv:
            return self.w2v_model.wv.most_similar(term, topn=top_n)
        return []
    
    
def content_analysis():
    
    model_name = "bert-base-uncased" 
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForMaskedLM.from_pretrained(model_name)

    tft_terms = [
        "reroll", "hyperroll", "slowroll", "econ", "carousel", 
        "augment", "BiS", "3-star", "4-cost", "5-cost",
        "frontline", "backline", "itemize", "positioning",
        "comp", "synergy", "trait", "emblem", "spatula"
    ]

    num_added = tokenizer.add_tokens(tft_terms)
    model.resize_token_embeddings(len(tokenizer))
    print(f"Added {num_added} new tokens")

