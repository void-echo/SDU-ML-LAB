import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split

# load data
iris = datasets.load_iris()
X = iris.data
y = iris.target
# knn
class KNN:
    def __init__(self, k=2, test_size=0.3):
        self.y = None
        self.X = None
        self.k = k
        self.test_size = test_size
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size)

    def fit(self, X, y):
        self.X = X
        self.y = y

    def predict(self, X):
        y_pred = []
        for x in X:
            y_pred.append(self._predict(x))
        return np.array(y_pred)

    def _predict(self, x):
        # compute distances
        distances = [np.sqrt(np.sum((x - x_train) ** 2)) for x_train in self.X]

        # get k nearest samples, labels
        k_indices = np.argsort(distances)[: self.k]
        k_nearest_labels = [self.y[i] for i in k_indices]

        # majority vote, most common class label
        most_common = np.argmax(np.bincount(k_nearest_labels))
        return most_common

    def score(self, X_test, y_test):
        y_pred = self.predict(X_test)
        accuracy = np.sum(y_pred == y_test) / len(y_test)
        return accuracy

    def show_acc(self):
        # make self.y_test .2f
        self.y_test = np.around(self.y_test, 2)
        self.test_size = np.around(self.test_size, 2)
        # format: <green color> K <reset color>: ...,  <red color> test_size <reset color>: ..., <blue color> accuracy <reset color>: .2f
        print(
            f"\033[32mK\033[0m: {self.k}, \033[31mtest_size\033[0m: {self.test_size}, \033[34maccuracy\033[0m: {self.score(self.X_test, self.y_test)}",
            end=" ")
        print("score: " + str(self.score(self.X_test, self.y_test)))


def test_all_and_plot():
    score_dict = {}
    for k in range(1, 10):
        for test_size in np.arange(0.1, 0.9, 0.1):
            knn = KNN(k=k, test_size=test_size)
            knn.fit(X, y)
            knn.show_acc()
            score_dict[(k, test_size)] = knn.score(knn.X_test, knn.y_test)

    # plot accuracy heatmap
    k = np.arange(1, 10)
    test_size = np.arange(0.1, 0.9, 0.1)
    k, test_size = np.meshgrid(k, test_size)
    score = np.array([score_dict[(k, test_size)] for k, test_size in zip(k.flatten(), test_size.flatten())])
    score = score.reshape(k.shape)

    plt.figure(figsize=(10, 8))
    plt.pcolormesh(k, test_size, score, cmap="RdBu")
    plt.colorbar()
    plt.xlabel("k")
    plt.ylabel("test_size")
    plt.show()


if __name__ == '__main__':
    np.random.seed(42)
    test_all_and_plot()
    # test one: k=3, test_size=0.4
    knn = KNN(k=4, test_size=0.1)
    knn.fit(X, y)
    knn.score(knn.X_test, knn.y_test)
