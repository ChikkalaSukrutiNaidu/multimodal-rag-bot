def is_relevant(scores):

    if not scores:
        return False

    best_score = min(scores)

    print("FAISS Scores:", scores)

    return best_score < 1.0