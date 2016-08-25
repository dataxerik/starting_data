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
    url = "https://www.oreilly.com/ideas/what-is-data-science"
    html = requests.get(url)
    soup = BeautifulSoup(html, 'html5lib')

    content = soup.find("div", "entry-content")
    regex = r"[\w']+|[\.]"

    document = []

    for paragraph in content("p"):
        words = re.findall((regex, fix_unicode(paragraph.text)))
        document.extend(words)

    return document

def generate_using_bigrams(transitions):
    current = "." # this means the next word starts a sentence
    result = []
    while True:
        next_world_candidates = transitions[current]
        current = random.choice(next_world_candidates)
        result.append(current)
        if current == ".": return " ".join(result)

def generate_using_trigrams(starts, trigram_transition):
    current = random.choice(starts) # choose a random starting word
    prev = "."                      # and precede it with a '.'
    result = [current]
    while True:
        next_word_candidates = trigram_transition[(prev, current)]
        next = random.choice(next_word_candidates)

        prev, current = current, next
        result.append(current)

        if current == ".":
            return " ".join(result)



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



