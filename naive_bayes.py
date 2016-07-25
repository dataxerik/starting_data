import re
import glob
import math
import random
from collections import defaultdict, Counter
from machine_learning import split_data


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


def spam_porbability(words_probs, message):
    message_words = tokenize(message)
    log_prob_if_spam = log_prob_if_not_spam = 0

    # iterate through each word in our vocabulary
    for word, prob_if_spam, prob_if_not_spam in words_probs:

        # if *word* appears in the message,
        # add the log probability of seeing it
        if word in message_words:
            log_prob_if_spam = math.log(prob_if_spam)
            log_prob_if_not_spam = math.log(prob_if_not_spam)

        # if *word* doesn't appear in the message
        # add the log probability of _not_ seeing it
        # which is log(1 - probability of seeing)
        else:
            log_prob_if_spam = math.log((1 - prob_if_spam))
            log_prob_if_not_spam = math.log(1 - prob_if_not_spam)

    prob_if_spam = math.exp(log_prob_if_spam)
    prob_if_not_spam = math.exp(log_prob_if_not_spam)

    return prob_if_spam / (prob_if_not_spam + prob_if_spam)


class NaiveBayesClassifer:
    def __init__(self, k=0.5):
        self.k = k
        self.words_probs = []

    def train(self, training_set):
        # count spam and non spam messages
        num_spams = len([is_spam
                         for message, is_spam in training_set
                         if is_spam])

        num_non_spams = len(training_set) - num_spams

        # run training data through out "pipeline"
        words_counts = count_words(training_set)
        self.words_probs = word_probabilities(words_counts,
                                              num_spams,
                                              num_non_spams,
                                              self.k)

    def classify(self, message):
        return spam_porbability(self.words_probs, message)

def p_spam_given_word(word_prob):
    """uses bayes's theorem to compute p(spam | message contains words)"""

    # word_prob is one of the triplets produced by word_probabilities
    word, prob_if_spam, prob_if_not_spam = word_prob
    return prob_if_spam / (prob_if_not_spam + prob_if_spam)


path = r"E:\PycharmProjects\starting_data\spam\*\*"

data = []

subject_regex = re.compile(r"^Subject:\s+")

# glob.glob returns every file name that matches the wildcard path
for fn in glob.glob(path):
    is_spam = "ham" not in fn

    with open(fn, 'r', encoding='ISO-8859-1') as file:
        for line in file:
            if line.startswith("Subject:"):
                # remove the leading "Subject: " and keep what's left
                subject = subject_regex.sub("", line).strip()
                data.append((subject, is_spam))

random.seed(0)


train_data, test_data = split_data(data, 0.75)

classifier = NaiveBayesClassifer()
classifier.train(train_data)

# triplets (subject, actual is_spam, predicted spam probability)
classified = [(subject, is_spam, classifier.classify(subject))
              for subject, is_spam in test_data]

# assume that spam_probability > 0.5 corresponds to spam prediction
# and count the combinations of (actual is_spam, predicted is_spam)
counts = Counter((is_spam, spam_porbability > 0.5)
                 for _, is_spam, spam_porbability in classified)

print(counts)

classified.sort(key=lambda row: row[2])
spammiest_hams = list(filter(lambda row: not row[1], classified))[-5:]
hammiest_spams = list(filter(lambda row: row[1], classified))[:5]

print(spammiest_hams)
print(hammiest_spams)

words = sorted(classifier.words_probs, key=p_spam_given_word)
print(words[-5:])
print(words[:5])