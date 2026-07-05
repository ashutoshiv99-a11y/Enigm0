import nltk
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

class NaturalLanguageProcessing:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()
        self.classifier = MultinomialNB()

    def preprocess_text(self, text):
        tokens = nltk.word_tokenize(text)
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return ' '.join(tokens)

    def train_model(self, X, y):
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        X_train = self.vectorizer.fit_transform(X_train)
        X_test = self.vectorizer.transform(X_test)
        self.classifier.fit(X_train, y_train)
        y_pred = self.classifier.predict(X_test)
        print("Model Accuracy:", accuracy_score(y_test, y_pred))

    def predict_intent(self, text):
        text = self.preprocess_text(text)
        text = self.vectorizer.transform([text])
        return self.classifier.predict(text)

# Example usage:
nlp = NaturalLanguageProcessing()
X = ["I want to book a flight", "I need help with my hotel reservation", "I want to cancel my trip"]
y = [0, 1, 2]  # 0: book flight, 1: hotel reservation, 2: cancel trip
nlp.train_model(X, y)
print(nlp.predict_intent("I want to book a flight to New York"))