"""
Keyword-Based Answer Grounding for Chunking-Agnostic Evaluation

This module implements the keyword overlap method for determining whether
a retrieved chunk contains sufficient answer information.

Usage:
    from keyword_grounding import KeywordGrounder
    
    grounding = KeywordGrounder(threshold=0.60)
    is_relevant = grounding.is_relevant(chunk_text, answer_text)
"""

import re
from typing import List, Set
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')


class KeywordGrounder:
    """
    Implements keyword-based answer grounding for retrieval evaluation.
    
    A retrieved chunk is deemed relevant if it contains sufficient keywords
    from the gold answer, where sufficiency is determined by an overlap threshold.
    """
    
    def __init__(self, threshold: float = 0.60, language: str = 'english'):
        """
        Initialize the keyword grounder.
        
        Args:
            threshold (float): Minimum keyword overlap ratio (0.0-1.0)
            language (str): Language for stopword filtering
        """
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("Threshold must be between 0.0 and 1.0")
        
        self.threshold = threshold
        self.stopwords = set(stopwords.words(language))
        
       # Add financial domain-specific stopwords
        self.stopwords.update([
            'according', 'stated', 'mentioned', 'discussed', 
            'reported', 'document', 'report', 'annual', 'form'
        ])
    
    def extract_keywords(self, text: str) -> Set[str]:
        """
        Extract content keywords from text.
        
        Args:
            text (str): Input text
            
        Returns:
            Set[str]: Set of lowercase keywords (excluding stopwords)
        """
        # Normalize text
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Filter: alphanumeric, not stopword, length > 2
        keywords = {
            token for token in tokens
            if token.isalnum() and token not in self.stopwords and len(token) > 2
        }
        
        return keywords
    
    def compute_overlap(self, chunk_text: str, answer_text: str) -> float:
        """
        Compute keyword overlap ratio between chunk and answer.
        
        Args:
            chunk_text (str): Retrieved chunk text
            answer_text (str): Gold answer text
            
        Returns:
            float: Overlap ratio (intersection / answer_keywords)
        """
        chunk_keywords = self.extract_keywords(chunk_text)
        answer_keywords = self.extract_keywords(answer_text)
        
        if len(answer_keywords) == 0:
            return 0.0
        
        intersection = chunk_keywords & answer_keywords
        overlap_ratio = len(intersection) / len(answer_keywords)
        
        return overlap_ratio
    
    def is_relevant(self, chunk_text: str, answer_text: str) -> bool:
        """
        Determine if chunk is relevant based on keyword overlap.
        
        Args:
            chunk_text (str): Retrieved chunk text
            answer_text (str): Gold answer text
            
        Returns:
            bool: True if overlap >= threshold, False otherwise
        """
        overlap = self.compute_overlap(chunk_text, answer_text)
        return overlap >= self.threshold
    
    def evaluate_retrieval(
        self, 
        retrieved_chunks: List[str], 
        answer: str
    ) -> dict:
        """
        Evaluate a ranked list of retrieved chunks.
        
        Args:
            retrieved_chunks (List[str]): Ranked list of chunk texts
            answer (str): Gold answer text
            
        Returns:
            dict: Evaluation metrics (first_relevant_rank, is_hit, overlap_scores)
        """
        overlap_scores = [
            self.compute_overlap(chunk, answer) 
            for chunk in retrieved_chunks
        ]
        
        # Find first relevant chunk
        first_relevant_rank = None
        for rank, overlap in enumerate(overlap_scores, start=1):
            if overlap >= self.threshold:
                first_relevant_rank = rank
                break
        
        return {
            'first_relevant_rank': first_relevant_rank,
            'is_hit': first_relevant_rank is not None,
            'overlap_scores': overlap_scores,
            'max_overlap': max(overlap_scores) if overlap_scores else 0.0
        }


def example_usage():
    """Example usage of KeywordGrounder"""
    
    # Initialize grounding with 60% threshold
    grounding = KeywordGrounder(threshold=0.60)
    
    # Example 1: Relevant chunk (overlap >= 60%)
    answer = "Equinor reported operating income of $5.2 billion in Q4 2018"
    chunk = "In Q4 2018, Equinor achieved operating income of $5.2B"
    
    overlap = grounding.compute_overlap(chunk, answer)
    is_relevant = grounding.is_relevant(chunk, answer)
    
    print(f"Example 1:")
    print(f"  Overlap: {overlap:.2%}")
    print(f"  Relevant: {is_relevant}")
    print()
    
    # Example 2: Irrelevant chunk (overlap < 60%)
    answer = "Equinor reported operating income of $5.2 billion in Q4 2018"
    chunk = "The company's revenue in 2018 was strong"
    
    overlap = grounding.compute_overlap(chunk, answer)
    is_relevant = grounding.is_relevant(chunk, answer)
    
    print(f"Example 2:")
    print(f"  Overlap: {overlap:.2%}")
    print(f"  Relevant: {is_relevant}")
    print()
    
    # Example 3: Evaluate ranked retrieval
    retrieved = [
        "The company reported revenue of $10B in 2019",  # Irrelevant
        "Equinor's operating income was $5.2B in Q4 2018",  # Relevant (rank 2)
        "Production volumes increased in 2018"  # Irrelevant
    ]
    
    result = grounding.evaluate_retrieval(retrieved, answer)
    
    print(f"Example 3 (Ranked Retrieval):")
    print(f"  First relevant rank: {result['first_relevant_rank']}")
    print(f"  Is hit: {result['is_hit']}")
    print(f"  Max overlap: {result['max_overlap']:.2%}")


if __name__ == '__main__':
    example_usage()
