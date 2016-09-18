import random
import matplotlib.pyplot as plt
from linear_algebra import squared_distance, vector_mean


class KMeans:
    """performs k-means clustering"""

    def __init__(self, k):
        self.k = k  # number of clusters
        self.means = None  # means of clusters

    def classify(self, input):
        """return the index of the cluster closest to the input"""
        return min(range(self.k),
                   key=lambda i: squared_distance(input, self.means[i]))

    def train(self, inputs):
        # choose k random points as the initial means
        self.means = random.sample(inputs, self.k)
        assignments = None

        while True:
            # print(assignments)
            # Find new assignments
            new_assignments = list(map(self.classify, inputs))

            # If no assignments have changed, we're done
            if assignments == new_assignments:
                return

            # Otherwise keep the new assignments
            assignments = new_assignments

            # And compute new means based on the new assignments
            for i in range(self.k):
                # find all the points assigned to cluster i
                i_points = [p for p, a in zip(inputs, assignments) if a == i]

                # make sure i_points is not empty so don't divide by 0
                if i_points:
                    self.means[i] = vector_mean(i_points)


if __name__ == "__main__":
    inputs = [[-14, -5], [13, 13], [20, 23], [-19, -11], [-9, -16], [21, 27], [-49, 15], [26, 13], [-46, 5], [-34, -1],
              [11, 15], [-49, 0], [-22, -16], [19, 28], [-12, -8], [-13, -19], [-41, 8], [-11, -6], [-25, -9],
              [-18, -3]]

    random.seed(0)  # so you get the same results as me
    clusterer = KMeans(3)
    clusterer.train(inputs)
    print("3-means:")
    print(clusterer.means)
    print()

    x = [input[0] for input in inputs]
    y = [input[1] for input in inputs]
    plt.scatter(x, y)
    plt.show()
