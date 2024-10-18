import os
import logging
from typing import List, Dict, Tuple
from backend.app.utils.logging_config import logger

def preprocess_text(text: str) -> List[str]:
    """
    Preprocesses the text by converting to lowercase and splitting into words.

    :param text: The text to preprocess.
    :return: List of words.
    """
    logger.debug("Preprocessing text for n-gram generation.")
    # Replace newlines and multiple spaces with a single space
    text = text.replace('\n', ' ').replace('\r', ' ').strip()
    processed = ' '.join(text.split()).lower().split()
    logger.debug(f"Preprocessed text: {processed[:10]}...")  # Show first 10 words for brevity
    return processed

def generate_ngrams(words: List[str], n: int) -> List[Tuple[str, int]]:
    """
    Generates n-grams from a list of words.

    :param words: List of words.
    :param n: Size of the n-gram.
    :return: List of tuples containing n-gram and its position.
    """
    logger.debug(f"Generating {n}-grams from words.")
    ngrams = [(" ".join(words[i:i+n]), i) for i in range(len(words) - n + 1)]
    logger.debug(f"Generated {len(ngrams)} n-grams.")
    return ngrams

def compute_hash(ngram: str, base: int = 256, mod: int = 10**9 + 7) -> int:
    """
    Computes a simple rolling hash for an n-gram.

    :param ngram: The n-gram string.
    :param base: Base number for hashing.
    :param mod: Modulus value for hashing.
    :return: Hash value.
    """
    logger.debug(f"Computing hash for n-gram: '{ngram}'.")
    h = 0
    for char in ngram:
        h = (h * base + ord(char)) % mod
    logger.debug(f"Hash for n-gram '{ngram}': {h}")
    return h

def load_source_ngrams(n: int) -> Dict[int, List[Tuple[str, str]]]:
    """
    Loads n-gram hashes from all source documents.

    :param n: Size of the n-grams.
    :return: Dictionary mapping hash values to list of (source_file, ngram) tuples.
    """
    logger.info(f"Loading source n-grams with n={n}.")
    source_ngrams = {}
    source_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'source_documents')
    
    for filename in os.listdir(source_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(source_dir, filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            words = preprocess_text(content)
            ngrams = generate_ngrams(words, n)
            
            for ngram, _ in ngrams:
                h = compute_hash(ngram)
                if h not in source_ngrams:
                    source_ngrams[h] = []
                source_ngrams[h].append((filename, ngram))
    
    logger.info(f"Loaded n-grams from {len(source_ngrams)} unique hashes.")
    return source_ngrams

def rabin_karp_plagiarism(target_text: str, n: int = 5, threshold: int = 3) -> List[Dict]:
    """
    Identifies plagiarism by comparing target text against source documents using Rabin-Karp.

    :param target_text: The text of the target document to analyze.
    :param n: Size of the n-grams.
    :param threshold: Minimum number of matches required for plagiarism detection.
    :return: List of plagiarism instances.
    """
    logger.info(f"Starting Rabin-Karp plagiarism detection with n={n}, threshold={threshold}")
    source_ngrams = load_source_ngrams(n)
    logger.info(f"Loaded {len(source_ngrams)} source n-gram hashes")

    words = preprocess_text(target_text)
    ngrams = generate_ngrams(words, n)
    logger.info(f"Generated {len(ngrams)} n-grams from target text")

    plagiarism_instances = []
    potential_matches = {}

    for ngram, position in ngrams:
        h = compute_hash(ngram)
        if h in source_ngrams:
            for source_file, source_ngram in source_ngrams[h]:
                if ngram == source_ngram:
                    logger.debug(f"Match found: '{ngram}' in {source_file} at position {position}")
                    if source_file not in potential_matches:
                        potential_matches[source_file] = []
                    potential_matches[source_file].append((ngram, position))

    for source_file, matches in potential_matches.items():
        if len(matches) >= threshold:
            for ngram, position in matches:
                plagiarism_instances.append({
                    'source_document': source_file,
                    'ngram': ngram,
                    'position_in_target': position
                })
            logger.info(f"Plagiarism detected: {len(matches)} matches found in {source_file}")

    logger.info(f"Plagiarism detection completed. Total instances found: {len(plagiarism_instances)}")
    return plagiarism_instances
