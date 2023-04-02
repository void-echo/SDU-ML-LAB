import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

class NaiveBayes:
    def __init__(self):
        self.classes = None
        self.mean = None
        self.var = None

    def fit(self, X, y):
        self.classes = np.unique(y)
        print("self.classes", self.classes)
        n_classes = len(self.classes)
        n_features = X.shape[1]
        self.mean = np.zeros((n_classes, n_features))
        self.var = np.zeros((n_classes, n_features))
        for i, c in enumerate(self.classes):
            X_c = X[y == c, :]
            self.mean[i, :] = X_c.mean(axis=0)
            self.var[i, :] = X_c.var(axis=0)

    def predict(self, X):
        y_pred = []
        for x in X:
            posterior = []
            for i, c in enumerate(self.classes):
                prior = np.log(np.mean(y_train == c))
                posterior.append(prior + np.sum(np.log(self._pdf(x, i))))

            y_pred.append(self.classes[np.argmax(posterior)])

        return np.array(y_pred)

    def _pdf(self, x, class_idx):
        mean = self.mean[class_idx]
        var = self.var[class_idx]
        return np.exp(-0.5 * ((x - mean) ** 2) / var) / np.sqrt(2 * np.pi * var)


dataset_path = './dataset/Iris.csv'
df = pd.read_csv(dataset_path)

X = df.iloc[:, 1:5].values
y = df.iloc[:, 5].values

np.random.seed(24)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=24)
print("Training record number: ", X_train.shape[0])
print("Testing record number: ", X_test.shape[0])

g = sns.relplot(x='SepalLengthCm', y='SepalWidthCm', data=df, hue='Species', style='Species')
g.fig.set_size_inches(10, 5)
plt.show()


nb = NaiveBayes()
nb.fit(X_train, y_train)
y_pred = nb.predict(X_test)

accuracy_test = accuracy_score(y_test, y_pred)
for i in range(0, len(y_pred)):
    is_right = y_pred[i] == y_test[i]
    if is_right:
        # print with green '√'
        print("\033[1;32m√ \033[0m", end='')
    else:
        # print with red information
        print("\033[1;31m\nPredicted: %20s, Actual: %20s\033[0m" % (y_pred[i], y_test[i]))

print("\nAccuracy on Test Dataset:", accuracy_test)

accuracy_train = accuracy_score(y_train, nb.predict(X_train))
print("Accuracy on Train Dataset:", accuracy_train)

