import sys
from collections import Counter


# pass in  the number of words as the first argument
try:
    num_words = int(sys.argv[1])
except:
    print("usage: frequency.py num_words")
    sys.exit(1) # non-zero exit code indicates error

counter = Counter(word.lower()
                  for line in sys.stdin
                  for word in line.strip().split()
                  if word)

for word, count in counter.most_common(num_words):
    sys.stdout.write(str(count))
    sys.stdout.write("\t")
    sys.stdout.write(word)
    sys.stdout.write("\n")