import math, random, re
from collections import defaultdict, Counter
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import requests


def plot_resumes():
    data = [("big data", 100, 15), ("Hadoop", 95, 25), ("Python", 75, 50),
            ("R", 50, 40), ("machine learning", 80, 20), ("statistics", 20, 60),
            ("data science", 60, 70), ("analytics", 90, 3),
            ("team player", 85, 85), ("dynamic", 2, 90), ("synergies", 70, 0),
            ("actionable insights", 40, 30), ("think out of the box", 45, 10),
            ("self-starter", 30, 50), ("customer focus", 65, 15),
            ("thought leadership", 35, 35)]

    def text_size(total):
        """equals 8 if total is 0, 28 if total is 200"""
        return 8 + total / 200 * 20

    for word, job_popularity, resume_popularity in data:
        plt.text(job_popularity, resume_popularity, word,
                 ha='center', va='center',
                 size=text_size(job_popularity + resume_popularity))

    plt.xlabel("Popularity on Job Postings")
    plt.ylabel("Popularity on Resumes")
    plt.axis([0, 100, 0, 100])
    plt.xticks([])
    plt.yticks([])
    plt.show()


# n-gram model
def fix_unicode(text):
    return text.replace(u"\u2019", "'")


def get_documents():
    url = "http://radar.oreilly.com/2010/06/what-is-data-science.html"
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html5lib')

    content = soup.find("div", "article-body")
    regex = r"[\w']+|[\.]"

    document = []

    for paragraph in content("p"):
        words = re.findall(regex, fix_unicode(paragraph.text))
        document.extend(words)

    return document


def generate_using_bigrams(transitions):
    current = "."  # this means the next word starts a sentence
    result = []
    while True:
        next_world_candidates = transitions[current]
        current = random.choice(next_world_candidates)
        result.append(current)
        if current == ".": return " ".join(result)


def generate_using_trigrams(starts, trigram_transition):
    current = random.choice(starts)  # choose a random starting word
    prev = "."  # and precede it with a '.'
    result = [current]
    while True:
        next_word_candidates = trigram_transition[(prev, current)]
        next = random.choice(next_word_candidates)

        prev, current = current, next
        result.append(current)

        if current == ".":
            return " ".join(result)


def is_terminal(token):
    return token[0] != "_"


def expand(grammar, tokens):
    for i, token in enumerate(tokens):

        # ignore  terminals
        if is_terminal(token):
            continue
        # choose a replacement at random
        replacement = random.choice(grammar[token])

        if is_terminal(replacement):
            tokens[i] = replacement
        else:
            tokens = tokens[:i] + replacement.split() + tokens[(i + 1):]
        return expand(grammar, tokens)
    return tokens


def generate_sentence(grammar):
    return expand(grammar, ["_S"])


def roll_a_die():
    return random.choice([1, 2, 3, 4, 5, 6])


def direct_sample():
    d1 = roll_a_die()
    d2 = roll_a_die()
    return d1, d1 + d2


def random_y_given_x(x):
    # equally likey to be x + 1, x +2, ... , x + 6
    return x + roll_a_die()


def random_x_given_y(y):
    if y <= 7:
        # if the total is 7 or less, the first die is equally likely to be
        # 1, 2, ..., (total - 1_
        return random.randrange(1, y)
    else:
        # if the total is 7 or more, the first die is equally likely to be
        # (total - 6), (total - 5), ..., 6
        return random.randrange(y - 6, 7)


def gibbs_sample(num_iters=100):
    x, y = 1, 2  # doesn't really matter
    for _ in range(num_iters):
        x = random_x_given_y(y)
        y = random_y_given_x(x)
    return x, y


def compare_distribution(num_samples=1000):
    counts = defaultdict(lambda: [0, 0])
    for _ in range(num_samples):
        counts[gibbs_sample()][0] += 1
        counts[direct_sample()][0] += 1
    return counts

if __name__ == '__main__':
    # plot_resumes()
    document = get_documents()
    bigrams = list(zip(document, document[1:]))
    transitions = defaultdict(list)
    for prev, current in bigrams:
        transitions[prev].append(current)

    random.seed(0)
    print("bigram sentences")
    for i in range(10):
        print(i, generate_using_bigrams(transitions))
    print()

    trigrams = list(zip(document, document[1:], document[2:]))
    trigrams_transitions = defaultdict(list)
    starts = []

    for prev, current, next in trigrams:
        if prev == ".":
            starts.append(current)

        trigrams_transitions[(prev, current)].append(next)

    print("Trigram sentences")
    for i in range(10):
        print(i, generate_using_trigrams(starts, trigrams_transitions))
    print()

    grammar = {
            "_S": ["_NP _VP"],
            "_NP": ["_N",
                    "_A _NP _P _A _N"],
            "_VP": ["_V",
                    "_V _NP"],
            "_N": ["data science", "Python", "regression"],
            "_A": ["big", "linear", "logistic"],
            "_P": ["about", "near"],
            "_V": ["learns", "trains", "tests", "is"]
        }

    print("grammar sentences")
    for i in range(10):
        print(i, " ".join(generate_sentence(grammar)))
    print()

    print("gibbs sampling")
    comparsion = compare_distribution()
    for roll, (gibbs, direct) in comparsion.items():
        print(roll, gibbs, direct)
