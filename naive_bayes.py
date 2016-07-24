import re
from collections import defaultdict


def tokenize(message):
    message = message.lower()
    all_words = re.findall("[a-z0-9']+", message)
    return set(all_words)


def count_words(training_set):
    """training set consists of pairs (message, is_spam)"""
    counts = defaultdict(lambda: [0, 0])
    for message, is_spam in training_set:
        for word in tokenize(message):
            counts[word][0 if is_spam else 1] += 1
    return counts


def word_probabilities(counts, total_spams, total_non_spams, k=0.5):
    """turn the words_counts int oa list of triplets
    w, p(w | spam) and p(w | -spam)"""
    return [(w,
             (spam + k) / (total_spams + 2 * k),
             (non_spam + k) / (total_non_spams + 2 * k))
            for w, (spam, non_spam) in counts.items()]