import os
import string
from typing import List, Tuple

# Define the path to the source_documents folder
#SOURCE_DOCS_PATH = os.path.join(os.path.dirname(__file__), '..')
# source_documents folder is at the same level as the backend folder

SOURCE_DOCS_PATH = os.path.join(os.path.dirname(__file__), '..', '..','..', 'source_documents')
print(SOURCE_DOCS_PATH) 

def preprocess_text(text: str) -> List[str]:
    translator = str.maketrans('', '', string.punctuation)
    return text.lower().translate(translator).split()

def generate_ngrams(words: List[str], n: int) -> List[str]:
    return [" ".join(words[i:i+n]) for i in range(len(words) - n + 1)]

def compute_hash(ngram: str, base: int = 256, mod: int = 10**9 + 7) -> int:
    """Simple rolling hash function for n-grams."""
    h = 0
    for char in ngram:
        h = (h * base + ord(char)) % mod
    return h

    # Explain compute_hash
    # The compute_hash function takes an n-gram and returns a hash value.
    # It does this by iterating over each character in the n-gram, converting it to its ASCII value, and adding it to the hash value.
    # How hard it is to break this hash function?
    # can hash collisions occur in this function?
    # Answer: It is not a good hash function for large strings. It is easy to break using a dictionary attack.
    # Answer: Yes, hash collisions can occur in this function.

def ingest_source_document(file_name: str, content: str, n: int = 3):
    """
    Saves a source document to the source_documents folder and precomputes its n-gram hashes.

    :param file_name: Name of the file to create.
    :param content: Content of the source document.
    :param n: Size of n-grams for hashing.
    """
    # Save the content to a file
    file_path = os.path.join(SOURCE_DOCS_PATH, file_name)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

    # Precompute and save n-gram hashes
    words = preprocess_text(content)
    ngrams = generate_ngrams(words, n)
    with open(file_path + f".ngrams", 'w', encoding='utf-8') as f:
        for ngram in ngrams:
            h = compute_hash(ngram)
            f.write(f"{h}\t{ngram}\n")

