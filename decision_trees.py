import math
from collections import Counter, defaultdict
from functools import partial


def entropy(class_probabilities):
    """given a list of class probabilities, compute the entropy"""
    return sum(-p * math.log(p, 2)
               for p in class_probabilities
               if p)  # ignore zero


def class_probabilities(labels):
    total_count = len(labels)
    return [count / total_count
            for count in Counter(labels).values()]


def data_entropy(labeled_data):
    labels = [label for _, label in labeled_data]
    probabilities = class_probabilities(labels)
    return entropy(probabilities)


def partition_entropy(subsets):
    """find the entropy from this partition of data into subets
    subsets is a list of lists of labeled data"""

    total_count = sum(len(subset) for subset in subsets)

    return sum(data_entropy(subset) * len(subset) / total_count
               for subset in subsets)


def group_by(items, key_fn):
    """returns a defaultdict(list), where each input item
    is in the list whose key is key_fn(item)"""
    groups = defaultdict(list)
    for item in items:
        key = key_fn(item)
        groups[key].append(item)
    return groups


def partition_by(inputs, attribute):
    """Each input is a pair (attribute, label).
    returns a dict : attribute_value -> inputs"""
    return group_by(inputs, lambda x: x[0][attribute])


def partition_entropy_by(inputs, attribute):
    """computes the entropy corresponding to the given partition"""
    partitions = partition_by(inputs, attribute)
    return partition_entropy(partitions.values())


def classify(tree, input):
    """Classify the input using the given decision tree"""

    # if this is a leaf node, return its value
    if tree in [True, False]:
        return tree

    # Otherwise this tree consists of an attribute to split on
    # and a dictionary whose keys are values of that attribute
    # and show values of are subtrees to consider next
    attribute, subtree_dict = tree

    subtree_key = input.get(attribute)  # None if input is missing attribute

    if subtree_key not in subtree_dict:
        subtree_key = None  # if no subtree for key, we'll use the None subtree

    subtree = subtree_dict[subtree_key]
    return classify(subtree, input)


def build_tree_id3(inputs, split_candidates=None):
    # if this is our first place
    # all keys of the first ipnut are split candidates
    if split_candidates is None:
        split_candidates = inputs[0][0].keys()

    # count Trues and Falses in the inputs
    num_inputs = len(inputs)
    num_trues = len([label for item, label in inputs if label])
    num_falses = num_inputs - num_trues

    if num_trues == 0: return False  # No Trues? return a "False" Leaf
    if num_falses == 0: return True  # No Falses? return a "True" Leaf

    if not split_candidates:  # if no split candidates are left
        return num_trues >= num_falses  # return the majority leaf

    # otherwise, split on the best attribute
    best_attribute = min(split_candidates,
                         key=partial(partition_entropy_by, inputs))

    partitions = partition_by(inputs, best_attribute)
    new_candidates = [a for a in split_candidates
                      if a != best_attribute]

    subtrees = {attribute_value: build_tree_id3(subset, new_candidates)
                for attribute_value, subset in partitions.items()}

    subtrees[None] = num_trues > num_falses  # default case

    return (best_attribute, subtrees)


def forest_classify(trees, input):
    votes = [classify(tree, input) for tree in trees]
    vote_counts = Counter(votes)
    return vote_counts.most_common(1)[0][0]


if __name__ == "__main__":
    inputs = [
        ({'level': 'Senior', 'lang': 'Java', 'tweets': 'no', 'phd': 'no'}, False),
        ({'level': 'Senior', 'lang': 'Java', 'tweets': 'no', 'phd': 'yes'}, False),
        ({'level': 'Mid', 'lang': 'Python', 'tweets': 'no', 'phd': 'no'}, True),
        ({'level': 'Junior', 'lang': 'Python', 'tweets': 'no', 'phd': 'no'}, True),
        ({'level': 'Junior', 'lang': 'R', 'tweets': 'yes', 'phd': 'no'}, True),
        ({'level': 'Junior', 'lang': 'R', 'tweets': 'yes', 'phd': 'yes'}, False),
        ({'level': 'Mid', 'lang': 'R', 'tweets': 'yes', 'phd': 'yes'}, True),
        ({'level': 'Senior', 'lang': 'Python', 'tweets': 'no', 'phd': 'no'}, False),
        ({'level': 'Senior', 'lang': 'R', 'tweets': 'yes', 'phd': 'no'}, True),
        ({'level': 'Junior', 'lang': 'Python', 'tweets': 'yes', 'phd': 'no'}, True),
        ({'level': 'Senior', 'lang': 'Python', 'tweets': 'yes', 'phd': 'yes'}, True),
        ({'level': 'Mid', 'lang': 'Python', 'tweets': 'no', 'phd': 'yes'}, True),
        ({'level': 'Mid', 'lang': 'Java', 'tweets': 'yes', 'phd': 'no'}, True),
        ({'level': 'Junior', 'lang': 'Python', 'tweets': 'no', 'phd': 'yes'}, False)
    ]

    for key in ['level', 'lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(inputs, key))

    senior_inputs = [(input, label)
                     for input, label in inputs if input['level'] == "Senior"]

    for key in ['lang', 'tweets', 'phd']:
        print(key, partition_entropy_by(senior_inputs, key))

    tree = build_tree_id3(inputs)

    print("Junior / Java / tweets / no phd", classify(tree,
                                                      {"level": "Junior",
                                                       "lang": "Java",
                                                       "tweets": "yes",
                                                       "phd": "no"}))

    print("Junior / Java / tweets / phd", classify(tree,
                                                   {"level": "Junior",
                                                    "lang": "Java",
                                                    "tweets": "yes",
                                                    "phd": "yes"}))

    print("Intern", classify(tree, {"level": "Intern"}))
    print("Senior", classify(tree, {"level": "Senior"}))
