import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from sklearn.metrics import accuracy_score

class AdvancedMLNLP:
    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained('distilbert-base-uncased')
        self.tokenizer = AutoTokenizer.from_pretrained('distilbert-base-uncased')
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    def train(self, dataset):
        train_data, test_data = dataset
        train_texts, train_labels = zip(*train_data)
        test_texts, test_labels = zip(*test_data)

        train_encodings = self.tokenizer(list(train_texts), truncation=True, padding=True)
        test_encodings = self.tokenizer(list(test_texts), truncation=True, padding=True)

        train_dataset = torch.utils.data.TensorDataset(torch.tensor(train_encodings['input_ids']), torch.tensor(train_encodings['attention_mask']), torch.tensor(train_labels))
        test_dataset = torch.utils.data.TensorDataset(torch.tensor(test_encodings['input_ids']), torch.tensor(test_encodings['attention_mask']), torch.tensor(test_labels))

        train_dataloader = torch.utils.data.DataLoader(train_dataset, batch_size=16, shuffle=True)
        test_dataloader = torch.utils.data.DataLoader(test_dataset, batch_size=16, shuffle=False)

        optimizer = optim.Adam(self.model.parameters(), lr=1e-5)

        for epoch in range(5):
            self.model.train()
            total_loss = 0
            for batch in train_dataloader:
                input_ids = batch[0].to(self.device)
                attention_mask = batch[1].to(self.device)
                labels = batch[2].to(self.device)

                optimizer.zero_grad()

                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss

                loss.backward()
                optimizer.step()

                total_loss += loss.item()
            print(f'Epoch {epoch+1}, Loss: {total_loss / len(train_dataloader)}')

            self.model.eval()
            predictions = []
            with torch.no_grad():
                for batch in test_dataloader:
                    input_ids = batch[0].to(self.device)
                    attention_mask = batch[1].to(self.device)

                    outputs = self.model(input_ids, attention_mask=attention_mask)
                    logits = outputs.logits
                    pred = torch.argmax(logits, dim=1)
                    predictions.extend(pred.cpu().numpy())

            print(f'Epoch {epoch+1}, Test Accuracy: {accuracy_score(test_labels, predictions)}')

    def predict(self, text):
        inputs = self.tokenizer(text, return_tensors='pt').to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits
            pred = torch.argmax(logits, dim=1)
            return pred.item()

# Example usage
if __name__ == '__main__':
    dataset = [
        ('This is a sample text', 1),
        ('This is another sample text', 0),
        ('Sample text for training', 1),
        ('More sample text', 0),
    ]
    advanced_ml_nlp = AdvancedMLNLP()
    advanced_ml_nlp.train(dataset)
    print(advanced_ml_nlp.predict('This is a test text'))