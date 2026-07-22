"""
Comprehensive Dictionary - Duniya ke saare English words
"""
import os
import json
import nltk
from typing import Set
from nltk.corpus import words, wordnet
import requests


class Dictionary:
    """Comprehensive word validation - 370k+ words"""
    
    def __init__(self):
        self.valid_words: Set[str] = set()
        self.word_meanings: dict = {}  # word -> meaning (optional)
        self._load_dictionary()
    
    def _load_dictionary(self):
        """Saare words load karta hai from multiple sources"""
        print("📚 Loading comprehensive dictionary...")
        
        # ═══════════════════════════════════════════
        # SOURCE 1: NLTK Words Corpus (236k+ words)
        # ═══════════════════════════════════════════
        try:
            nltk.download('words', quiet=True)
            nltk_words = set(w.lower() for w in words.words())
            self.valid_words.update(nltk_words)
            print(f"✅ NLTK Words loaded: {len(nltk_words)} words")
        except Exception as e:
            print(f"❌ Error loading NLTK words: {e}")
        
        # ═══════════════════════════════════════════
        # SOURCE 2: NLTK WordNet (147k+ words with meanings)
        # ═══════════════════════════════════════════
        try:
            nltk.download('wordnet', quiet=True)
            wordnet_words = set()
            for synset in wordnet.all_synsets():
                for lemma in synset.lemmas():
                    word = lemma.name().lower().replace('_', ' ')
                    if word.isalpha():
                        wordnet_words.add(word)
            
            self.valid_words.update(wordnet_words)
            print(f"✅ WordNet loaded: {len(wordnet_words)} words")
        except Exception as e:
            print(f"❌ Error loading WordNet: {e}")
        
        # ═══════════════════════════════════════════
        # SOURCE 3: External Word List (370k+ words)
        # ═══════════════════════════════════════════
        external_words_file = "data/english_words.txt"
        if os.path.exists(external_words_file):
            try:
                with open(external_words_file, 'r', encoding='utf-8') as f:
                    external_words = set(line.strip().lower() for line in f if line.strip())
                    self.valid_words.update(external_words)
                    print(f"✅ External word list loaded: {len(external_words)} words")
            except Exception as e:
                print(f"❌ Error loading external words: {e}")
        else:
            print(f"⚠️ External word list not found: {external_words_file}")
            print("💡 Download karne ke liye: python download_words.py")
        
        # ═══════════════════════════════════════════
        # SOURCE 4: Custom Words (JSON file)
        # ═══════════════════════════════════════════
        custom_words_file = "data/words.json"
        if os.path.exists(custom_words_file):
            try:
                with open(custom_words_file, 'r', encoding='utf-8') as f:
                    custom_words = json.load(f)
                    self.valid_words.update(w.lower() for w in custom_words)
                    print(f"✅ Custom words loaded: {len(custom_words)} words")
            except Exception as e:
                print(f"❌ Error loading custom words: {e}")
        
        # ═══════════════════════════════════════════
        # SOURCE 5: Common Words (Fallback)
        # ═══════════════════════════════════════════
        common_words = [
            "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
            "of", "with", "by", "from", "up", "about", "into", "through", "during",
            "is", "are", "was", "were", "be", "been", "being", "have", "has", "had",
            "do", "does", "did", "will", "would", "could", "should", "may", "might",
            "can", "able", "must", "need", "dare", "ought", "used", "apple", "banana",
            "cat", "dog", "elephant", "fish", "game", "house", "ice", "jungle", "kite",
            "lion", "monkey", "nest", "orange", "pen", "queen", "rabbit", "sun", "tree",
            "umbrella", "van", "water", "xylophone", "yellow", "zebra", "python",
            "telegram", "bot", "word", "chain", "antakshari", "multiplayer", "dictionary"
        ]
        self.valid_words.update(w.lower() for w in common_words)
        
        # Remove duplicates and filter
        self.valid_words = set(w for w in self.valid_words if w.isalpha() and len(w) >= 2)
        
        print(f"\n🎉 TOTAL WORDS LOADED: {len(self.valid_words)}")
        print("=" * 50)
    
    def is_valid_word(self, word: str) -> bool:
        """Check karta hai ki word valid hai ya nahi"""
        word = word.lower().strip()
        
        # Basic checks
        if not word or not word.isalpha() or len(word) < 2:
            return False
        
        # Check in loaded dictionary
        if word in self.valid_words:
            return True
        
        # Optional: Check with external API (slow but comprehensive)
        # return self._check_with_api(word)
        
        return False
    
    def _check_with_api(self, word: str) -> bool:
        """External dictionary API se check karta hai (optional)"""
        try:
            # Free Dictionary API
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            response = requests.get(url, timeout=2)
            
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 0:
                    # Cache the word for future use
                    self.valid_words.add(word.lower())
                    return True
        except Exception as e:
            print(f"API error: {e}")
        
        return False
    
    def get_meaning(self, word: str) -> str:
        """Word ka meaning return karta hai (optional feature)"""
        word = word.lower().strip()
        
        # Check cache
        if word in self.word_meanings:
            return self.word_meanings[word]
        
        # Try WordNet
        try:
            synsets = wordnet.synsets(word)
            if synsets:
                meaning = synsets[0].definition()
                self.word_meanings[word] = meaning
                return meaning
        except:
            pass
        
        return "Meaning not available"
    
    def add_word(self, word: str):
        """Naya word add karta hai"""
        self.valid_words.add(word.lower())
    
    def get_word_count(self) -> int:
        """Total words return karta hai"""
        return len(self.valid_words)
    
    def get_words_starting_with(self, letter: str) -> list:
        """Specific letter se start hone wale words return karta hai"""
        letter = letter.lower()
        return [w for w in self.valid_words if w.startswith(letter)]
