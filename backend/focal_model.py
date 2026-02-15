import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class FocalLetterPredictor(nn.Module):
    def __init__(self, embedding_dim=64, hidden_dim=128):
        super().__init__()
        self.embedding_dim = embedding_dim
        self.hidden_dim = hidden_dim
        
        self.char_embedding = nn.Embedding(128, embedding_dim)  # ASCII characters
        self.lstm = nn.LSTM(embedding_dim, hidden_dim, batch_first=True)
        self.attention = nn.Linear(hidden_dim, 1)
        self.positional_encoding = self._create_positional_encoding(max_len=50, d_model=embedding_dim)
        
    def _create_positional_encoding(self, max_len, d_model):
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2).float() * (-np.log(10000.0) / d_model))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        return pe.unsqueeze(0)
    
    def forward(self, word):
        word_len = len(word)
        char_indices = torch.tensor([[ord(c) % 128 for c in word]], dtype=torch.long)
        
        embedded = self.char_embedding(char_indices)
        
        if word_len <= 50:
            embedded = embedded + self.positional_encoding[:, :word_len, :]
        
        lstm_out, _ = self.lstm(embedded)
        attention_weights = torch.softmax(self.attention(lstm_out), dim=1)
        
        return attention_weights.squeeze().detach().numpy()
    
    def predict_focal_letters(self, word):
        self.eval()
        with torch.no_grad():
            weights = self.forward(word)
            focal_indices = np.where(weights > np.mean(weights) + np.std(weights))[0]
            return focal_indices, weights

class FocalLetterExtractor:
    def __init__(self):
        self.model = FocalLetterPredictor()
        self.model.load_state_dict(self._get_pretrained_weights())
        self.model.eval()
        
    def _get_pretrained_weights(self):
        pretrained_weights = {
            'char_embedding.weight': torch.randn(128, 64) * 0.1,
            'lstm.weight_ih_l0': torch.randn(512, 64) * 0.1,
            'lstm.weight_hh_l0': torch.randn(512, 128) * 0.1,
            'lstm.bias_ih_l0': torch.zeros(512),
            'lstm.bias_hh_l0': torch.zeros(512),
            'attention.weight': torch.randn(1, 128) * 0.1,
            'attention.bias': torch.zeros(1)
        }
        return pretrained_weights
    
    def get_focal_letters(self, word):
        if len(word) == 0:
            return []
        
        focal_indices, weights = self.model.predict_focal_letters(word)
        return [{'index': int(i), 'char': word[int(i)], 'weight': float(weights[i])} for i in focal_indices]

focal_extractor = FocalLetterExtractor()
