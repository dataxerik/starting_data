import sys, re

# sys.argv is a lis tof command-line argument
# sys.argv[0] is the name of the program itself
# sys.argv[1]
regex = sys.argv[1]

# for every line passed into the script
for line in sys.stdin:
    # if it matches the regex, write it to the stdout
    if re.search(regex, line):
        sys.stdout.write(line)