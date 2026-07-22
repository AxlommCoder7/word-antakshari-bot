"""
Download comprehensive English word list (370k+ words)
Run this once before starting the bot
"""
import os
import requests


def download_word_list():
    """GitHub se comprehensive word list download karta hai"""
    
    # Create data directory
    os.makedirs("data", exist_ok=True)
    
    # Multiple sources for comprehensive coverage
    urls = [
        # Source 1: dwyl/english-words (370k+ words)
        "https://raw.githubusercontent.com/dwyl/english-words/master/words.txt",
        
        # Source 2: first20hours/google-10000-english (10k most common)
        "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english.txt",
        
        # Source 3: powerlanguage/word-lists (various lists)
        "https://raw.githubusercontent.com/powerlanguage/word-lists/master/1000-most-common-words.txt",
    ]
    
    output_file = "data/english_words.txt"
    all_words = set()
    
    print("📥 Downloading comprehensive English word list...")
    print("=" * 60)
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Downloading from: {url}")
        
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            words = set(line.strip().lower() for line in response.text.split('\n') if line.strip())
            all_words.update(words)
            
            print(f"✅ Downloaded {len(words)} words")
            
        except Exception as e:
            print(f"❌ Error: {e}")
    
    # Filter only alphabetic words
    all_words = set(w for w in all_words if w.isalpha() and len(w) >= 2)
    
    # Save to file
    with open(output_file, 'w', encoding='utf-8') as f:
        for word in sorted(all_words):
            f.write(word + '\n')
    
    print("\n" + "=" * 60)
    print(f"🎉 SUCCESS! Total unique words: {len(all_words)}")
    print(f"💾 Saved to: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    download_word_list()
