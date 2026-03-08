"""
Main Evaluation Script for FinRAG-Equinor

Computes retrieval metrics (MRR, Hit@K, Precision, Recall) using
keyword-based answer grounding.

Usage:
    python evaluate_retrieval.py \\
        --predictions results/e5_predictions.jsonl \\
        --gold_data ../data/qa_pairs.jsonl \\
        --threshold 0.60 \\
        --output results/eval_metrics.json
"""

import json
import argparse
from pathlib import Path
from typing import List, Dict
from keyword_grounding import KeywordGrounder
from metrics import compute_mrr, compute_hit_at_k, compute_precision_recall


def load_jsonl(filepath: Path) -> List[Dict]:
    """Load JSONL file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]


def evaluate_predictions(
    predictions: List[Dict],
    gold_data: List[Dict],
    threshold: float = 0.60,
    k_values: List[int] = [1, 3, 5, 10]
) -> Dict:
    """
    Evaluate retrieval predictions.
    
    Args:
        predictions: List of predictions, each with format:
            {
                "question_id": str,
                "retrieved_chunks": [
                    {"chunk_id": str, "text": str, "score": float},
                    ...
                ]
            }
        gold_data: List of gold QA pairs
        threshold: Keyword overlap threshold
        k_values: List of k values for Hit@K
        
    Returns:
        Dict of evaluation metrics
    """
    # Create gold answer lookup
    gold_lookup = {item['id']: item for item in gold_data}
    
    # Initialize grounding
    grounding = KeywordGrounder(threshold=threshold)
    
    # Collect per-query results
    reciprocal_ranks = []
    hits_at_k = {k: [] for k in k_values}
    precision_at_k = {k: [] for k in k_values}
    recall_at_k = {k: [] for k in k_values}
    
    for pred in predictions:
        qid = pred['question_id']
        
        if qid not in gold_lookup:
            print(f"Warning: Question {qid} not found in gold data")
            continue
        
        gold = gold_lookup[qid]
        answer = gold['answer']
        retrieved = pred['retrieved_chunks']
        
        # Extract retrieved chunk texts
        chunk_texts = [chunk['text'] for chunk in retrieved]
        
        # Evaluate retrieval
        result = grounding.evaluate_retrieval(chunk_texts, answer)
        
        # Compute reciprocal rank
        if result['first_relevant_rank'] is not None:
            rr = 1.0 / result['first_relevant_rank']
        else:
            rr = 0.0
        reciprocal_ranks.append(rr)
        
        # Compute Hit@K
        for k in k_values:
            if result['first_relevant_rank'] is not None and result['first_relevant_rank'] <= k:
                hits_at_k[k].append(1)
            else:
                hits_at_k[k].append(0)
        
        # Compute Precision/Recall@K
        # Count relevant chunks in top-k
        for k in k_values:
            top_k_chunks = chunk_texts[:k]
            num_relevant = sum(
                1 for chunk in top_k_chunks
                if grounding.is_relevant(chunk, answer)
            )
            
            precision = num_relevant / k if k > 0 else 0.0
            # For single-answer QA, recall is Hit@K
            recall = 1.0 if num_relevant > 0 else 0.0
            
            precision_at_k[k].append(precision)
            recall_at_k[k].append(recall)
    
    # Aggregate metrics
    n = len(reciprocal_ranks)
    metrics = {
        'num_queries': n,
        'threshold': threshold,
        'MRR': sum(reciprocal_ranks) / n if n > 0 else 0.0
    }
    
    for k in k_values:
        metrics[f'Hit@{k}'] = sum(hits_at_k[k]) / n if n > 0 else 0.0
        metrics[f'Precision@{k}'] = sum(precision_at_k[k]) / n if n > 0 else 0.0
        metrics[f'Recall@{k}'] = sum(recall_at_k[k]) / n if n > 0 else 0.0
    
    return metrics


def main():
    parser = argparse.ArgumentParser(
        description='Evaluate retrieval predictions for FinRAG-Equinor'
    )
    parser.add_argument(
        '--predictions',
        type=Path,
        required=True,
        help='Path to predictions JSONL file'
    )
    parser.add_argument(
        '--gold_data',
        type=Path,
        required=True,
        help='Path to gold QA pairs JSONL file'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=0.60,
        help='Keyword overlap threshold (default: 0.60)'
    )
    parser.add_argument(
        '--output',
        type=Path,
        default=None,
        help='Output path for metrics JSON (optional)'
    )
    
    args = parser.parse_args()
    
    # Load data
    print(f"Loading predictions from {args.predictions}...")
    predictions = load_jsonl(args.predictions)
    
    print(f"Loading gold data from {args.gold_data}...")
    gold_data = load_jsonl(args.gold_data)
    
    # Evaluate
    print(f"\nEvaluating with threshold={args.threshold:.2f}...")
    metrics = evaluate_predictions(predictions, gold_data, args.threshold)
    
    # Print results
    print(f"\n{'='*60}")
    print(f"Evaluation Results (N={metrics['num_queries']} queries)")
    print(f"{'='*60}")
    print(f"Threshold: {metrics['threshold']:.2f}")
    print(f"MRR@10:    {metrics['MRR']:.4f}")
    print(f"\nHit Rates:")
    for k in [1, 3, 5, 10]:
        if f'Hit@{k}' in metrics:
            print(f"  Hit@{k:<2}:  {metrics[f'Hit@{k}']:.2%}")
    print(f"\nPrecision:")
    for k in [1, 3, 5, 10]:
        if f'Precision@{k}' in metrics:
            print(f"  P@{k:<2}:    {metrics[f'Precision@{k}']:.4f}")
    print(f"{'='*60}\n")
    
    # Save results
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(metrics, f, indent=2)
        print(f"Results saved to {args.output}")


if __name__ == '__main__':
    main()
