scores = [0.91, 0.72, 0.95, 0.88]
def get_high_scores(scores, threshold=0.9):
    data = []
    for x in scores:
        if x >= threshold:
            data.append(x)
    return data
result1 = get_high_scores(scores)
result2 = get_high_scores(scores, threshold=0.8)
print(result1)
print(result2)