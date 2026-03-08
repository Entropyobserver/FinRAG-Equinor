"""
Retrieval Metrics for FinRAG-Equinor

Standard IR metrics: MRR, Hit@K, Precision, Recall
"""

from typing import List


def compute_mrr(ranks: List[int]) -> float:
    """
    Compute Mean Reciprocal Rank.
    
    Args:
        ranks: List of ranks of first relevant item (None if no hit)
        
    Returns:
        float: MRR score
    """
    reciprocal_ranks = [
        1.0 / rank if rank is not None else 0.0
        for rank in ranks
    ]
    return sum(reciprocal_ranks) / len(reciprocal_ranks) if reciprocal_ranks else 0.0


def compute_hit_at_k(ranks: List[int], k: int) -> float:
    """
    Compute Hit@K (Recall@K for single-answer QA).
    
    Args:
        ranks: List of ranks of first relevant item
        k: Cutoff position
        
    Returns:
        float: Hit@K score
    """
    hits = [
        1 if rank is not None and rank <= k else 0
        for rank in ranks
    ]
    return sum(hits) / len(hits) if hits else 0.0


def compute_precision_recall(
    num_relevant_retrieved: List[int],
    num_retrieved: List[int],
    num_relevant_total: List[int]
) -> tuple:
    """
    Compute Precision and Recall.
    
    Args:
        num_relevant_retrieved: Number of relevant items retrieved per query
        num_retrieved: Number of items retrieved per query (usually k)
        num_relevant_total: Total number of relevant items per query
        
    Returns:
        tuple: (precision, recall)
    """
    precisions = [
        rel / retr if retr > 0 else 0.0
        for rel, retr in zip(num_relevant_retrieved, num_retrieved)
    ]
    
    recalls = [
        rel / total if total > 0 else 0.0
        for rel, total in zip(num_relevant_retrieved, num_relevant_total)
    ]
    
    avg_precision = sum(precisions) / len(precisions) if precisions else 0.0
    avg_recall = sum(recalls) / len(recalls) if recalls else 0.0
    
    return avg_precision, avg_recall


def compute_dcg(relevance_scores: List[float], k: int) -> float:
    """
    Compute Discounted Cumulative Gain.
    
    Args:
        relevance_scores: List of relevance scores (binary or graded)
        k: Cutoff position
        
    Returns:
        float: DCG@k score
    """
    import math
    
    dcg = 0.0
    for i, rel in enumerate(relevance_scores[:k], start=1):
        dcg += rel / math.log2(i + 1)
    
    return dcg


def compute_ndcg(relevance_scores: List[float], k: int) -> float:
    """
    Compute Normalized Discounted Cumulative Gain.
    
    Args:
        relevance_scores: List of relevance scores
        k: Cutoff position
        
    Returns:
        float: NDCG@k score
    """
    dcg = compute_dcg(relevance_scores, k)
    
    # Ideal DCG (sort relevance scores descending)
    ideal_relevance = sorted(relevance_scores, reverse=True)
    idcg = compute_dcg(ideal_relevance, k)
    
    if idcg == 0.0:
        return 0.0
    
    return dcg / idcg
