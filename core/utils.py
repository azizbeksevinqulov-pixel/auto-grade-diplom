from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def grade_answer(student, correct):
    vectorizer = TfidfVectorizer()
    tfidf = vectorizer.fit_transform([student, correct])
    similarity = cosine_similarity(tfidf[0:1], tfidf[1:2])[0][0]
    score = round(similarity * 100, 2)
    return score
