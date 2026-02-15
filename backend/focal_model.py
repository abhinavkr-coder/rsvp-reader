"""
Improved Focal Letter Predictor for RSVP Reading

Based on research:
- Optimal Viewing Position (OVP) is typically 30-40% from word start
- Consonants are more important than vowels for word recognition
- The "anchor point" should be slightly left of center
- Multiple focal points can improve readability for longer words
"""

import numpy as np

class FocalLetterPredictor:
    def __init__(self):
        # Vowels are less critical for word recognition
        self.vowels = set('aeiouAEIOU')
        
        # High-value consonants that aid recognition
        self.important_consonants = set('bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ')
    
    def calculate_ovp(self, word_length):
        """
        Calculate Optimal Viewing Position based on word length
        Research shows OVP is typically 30-40% from the start
        """
        if word_length <= 3:
            return word_length // 2
        elif word_length <= 5:
            return int(word_length * 0.35)
        elif word_length <= 8:
            return int(word_length * 0.37)
        else:
            return int(word_length * 0.40)
    
    def get_character_importance(self, char, position, word_length):
        """
        Calculate importance score for a character at a position
        Higher scores = more important for word recognition
        """
        score = 0.0
        
        # Base score for consonants vs vowels
        if char in self.important_consonants:
            score += 1.0
        elif char in self.vowels:
            score += 0.3
        else:
            score += 0.1  # Numbers, special chars
        
        # Position-based scoring (prefer positions near OVP)
        ovp = self.calculate_ovp(word_length)
        distance_from_ovp = abs(position - ovp)
        position_score = 1.0 / (1 + distance_from_ovp * 0.5)
        score *= position_score
        
        # Penalize first and last positions slightly
        if position == 0:
            score *= 0.7
        elif position == word_length - 1:
            score *= 0.6
        
        # Boost middle consonants
        if position > 0 and position < word_length - 1:
            if char in self.important_consonants:
                score *= 1.2
        
        return score
    
    def identify_focal_letters(self, word):
        """
        Identify the most important letter(s) for RSVP reading
        Returns indices of focal letters with their weights
        """
        if len(word) == 0:
            return [], []
        
        if len(word) == 1:
            return [0], [1.0]
        
        # Calculate importance for each character
        scores = []
        for i, char in enumerate(word):
            score = self.get_character_importance(char, i, len(word))
            scores.append(score)
        
        scores = np.array(scores)
        
        # Normalize scores
        if scores.max() > 0:
            scores = scores / scores.max()
        
        # For short words (1-4 chars): 1 focal letter
        # For medium words (5-8 chars): 1-2 focal letters
        # For long words (9+ chars): 2-3 focal letters
        if len(word) <= 4:
            num_focal = 1
        elif len(word) <= 8:
            num_focal = 2 if len(word) >= 6 else 1
        else:
            num_focal = min(3, len(word) // 4)
        
        # Get top N indices
        focal_indices = np.argsort(scores)[-num_focal:][::-1]
        focal_indices = sorted(focal_indices.tolist())  # Sort by position
        
        focal_weights = [scores[i] for i in focal_indices]
        
        return focal_indices, focal_weights
    
    def get_primary_focal(self, word):
        """
        Get the single most important focal letter (for main highlighting)
        """
        indices, weights = self.identify_focal_letters(word)
        if len(indices) > 0:
            return indices[0]
        return 0


class FocalLetterExtractor:
    def __init__(self):
        self.predictor = FocalLetterPredictor()
    
    def get_focal_letters(self, word):
        """
        Returns list of focal letter dictionaries with index, char, and weight
        """
        if len(word) == 0:
            return []
        
        indices, weights = self.predictor.identify_focal_letters(word)
        
        return [
            {
                'index': int(idx),
                'char': word[int(idx)],
                'weight': float(weight)
            }
            for idx, weight in zip(indices, weights)
        ]
    
    def get_primary_focal_letter(self, word):
        """
        Returns the main focal letter for display
        """
        if len(word) == 0:
            return {'index': 0, 'char': '', 'weight': 0.0}
        
        idx = self.predictor.get_primary_focal(word)
        focal_letters = self.get_focal_letters(word)
        
        if focal_letters:
            return focal_letters[0]
        
        return {'index': idx, 'char': word[idx], 'weight': 1.0}


# Global instance
focal_extractor = FocalLetterExtractor()


# Test the predictor
if __name__ == "__main__":
    test_words = [
        "I", "am", "the", "quick", "brown", "fox", "jumps", 
        "over", "lazy", "dog", "reading", "comprehension",
        "extraordinary", "example", "beautiful", "information"
    ]
    
    print("Testing Focal Letter Predictor:")
    print("=" * 60)
    
    for word in test_words:
        focal_letters = focal_extractor.get_focal_letters(word)
        primary = focal_extractor.get_primary_focal_letter(word)
        
        # Create visual representation
        visual = list(word)
        for fl in focal_letters:
            visual[fl['index']] = f"[{visual[fl['index']]}]"
        
        print(f"{word:20} -> {''.join(visual):30} (primary: {primary['char']} at {primary['index']})")
    
    print("=" * 60)