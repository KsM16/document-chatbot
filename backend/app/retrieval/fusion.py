# backend/app/retrieval/fusion.py

def reciprocal_rank_fusion(results: list[list[dict]], k: int = 60) -> list[dict]:
    """
    Combines multiple ranked lists into a single list using RRF.
    Formula: score = 1 / (k + rank)
    """
    scores = {}
    
    for result_list in results:
        for rank, item in enumerate(result_list):
            doc_id = item['id']
            if doc_id not in scores:
                scores[doc_id] = {'item': item, 'score': 0}
            # Add the reciprocal rank score
            scores[doc_id]['score'] += 1 / (k + rank + 1)

    # Sort by the combined score in descending order
    fused = sorted(scores.values(), key=lambda x: x['score'], reverse=True)
    
    # Return just the items, stripped of the internal score
    return [x['item'] for x in fused]