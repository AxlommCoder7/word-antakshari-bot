"""
Dictionary - Words validate karta hai
"""
import json
import os
from typing import Set
import nltk
from nltk.corpus import words


class Dictionary:
    """Word validation ke liye"""
    
    def __init__(self):
        self.valid_words: Set[str] = set()
        self._load_dictionary()
    
    def _load_dictionary(self):
        """Dictionary load karta hai"""
        try:
            # NLTK se words load karo
            nltk.download('words', quiet=True)
            self.valid_words = set(w.lower() for w in words.words())
            
            # Custom words bhi add karo
            custom_words_file = "data/words.json"
            if os.path.exists(custom_words_file):
                with open(custom_words_file, 'r') as f:
                    custom_words = json.load(f)
                    self.valid_words.update(w.lower() for w in custom_words)
            
            print(f"✅ Dictionary loaded: {len(self.valid_words)} words")
            
        except Exception as e:
            print(f"❌ Error loading dictionary: {e}")
            # Fallback - basic words
            self.valid_words = set([
                "apple", "banana", "cat", "dog", "elephant", "fish",
                "game", "house", "ice", "jungle", "kite", "lion",
                "monkey", "nest", "orange", "pen", "queen", "rabbit",
                "sun", "tree", "umbrella", "van", "water", "xylophone",
                "yellow", "zebra"
            ])
    
    def is_valid_word(self, word: str) -> bool:
        """Check karta hai ki word valid hai ya nahi"""
        return word.lower() in self.valid_words
    
    def add_word(self, word: str):
        """Naya word add karta hai"""
        self.valid_words.add(word.lower())
    
    def get_word_count(self) -> int:
        """Total words return karta hai"""
        return len(self.valid_words)
