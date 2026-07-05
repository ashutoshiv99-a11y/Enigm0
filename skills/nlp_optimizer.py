import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import string
from collections import defaultdict
import numpy as np

class NLP_Optimizer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.lemmatizer = WordNetLemmatizer()

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(r'http\S+', '', text)
        text = text.translate(str.maketrans('', '', string.punctuation))
        tokens = word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens]
        return tokens

    def optimize_performance(self, text):
        tokens = self.preprocess_text(text)
        token_freq = defaultdict(int)
        for token in tokens:
            token_freq[token] += 1
        return token_freq

    def fix_bugs(self, text):
        tokens = self.preprocess_text(text)
        bug_fixes = []
        for token in tokens:
            if token in self.stop_words:
                bug_fixes.append(token)
        return bug_fixes

    def enhance_nlp(self, text):
        tokens = self.preprocess_text(text)
        nlp_output = []
        for token in tokens:
            nlp_output.append((token, self.lemmatizer.lemmatize(token)))
        return nlp_output

def main():
    nlp_optimizer = NLP_Optimizer()
    text = "This is a sample text to optimize performance, fix bugs, and enhance natural language processing capabilities."
    print(nlp_optimizer.optimize_performance(text))
    print(nlp_optimizer.fix_bugs(text))
    print(nlp_optimizer.enhance_nlp(text))

if __name__ == "__main__":
    main()