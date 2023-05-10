import numpy as np
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from echo_logger import *

# noinspection PyAttributeOutsideInit
class MySVM:
    """
    Params
        eta : float
        epoch : int
        random_state : int
        num_samples : int
        num_features : int
        w : NDArray[float]
        b : float
        alpha : NDArray[float]

    Methods:
        fit -> None
            Fitting parameter vectors for training data
        predict -> NDArray[int]
            Return predicted value
    """

    def __init__(self, eta=0.001, epoch=1000, random_state=42):
        self.eta = eta
        self.epoch = epoch
        self.random_state = random_state
        self.is_trained = False

    def fit(self, X, y):
        """
        Fitting parameter vectors for training data

        Parameters
        ----------
        X : NDArray[NDArray[float]]
        y : NDArray[float]
        """
        self.num_samples = X.shape[0]
        self.num_features = X.shape[1]
        self.w = np.zeros(self.num_features)
        self.b = 0
        rgen = np.random.RandomState(self.random_state)
        self.alpha = rgen.normal(loc=0.0, scale=0.01, size=self.num_samples)

        for _ in range(self.epoch):
            self._cycle(X, y)

        indexes_sv = [i for i in range(self.num_samples) if self.alpha[i] != 0]
        for i in indexes_sv:
            self.w += self.alpha[i] * y[i] * X[i]
        for i in indexes_sv:
            self.b += y[i] - (self.w @ X[i])
        self.b /= len(indexes_sv)
        self.is_trained = True

    def predict(self, X):
        """
        X : NDArray[NDArray[float]]
        Returns NDArray[int]
        """
        assert self.is_trained, "Model is not trained yet"
        hyperplane = X @ self.w + self.b
        result = np.where(hyperplane > 0, 1, -1)
        return result

    def _cycle(self, X, y):
        """
        One cycle of gradient descent method
        X : NDArray[NDArray[float]]
        y : NDArray[float]
        """
        y = y.reshape([-1, 1])
        H = (y @ y.T) * (X @ X.T)  # @ means matrix multiplication in numpy
        grad = np.ones(self.num_samples) - H @ self.alpha
        self.alpha += self.eta * grad
        self.alpha = np.where(self.alpha < 0, 0, self.alpha)




iris = load_iris()
df_iris = pd.DataFrame(iris.data, columns=iris.feature_names)
df_iris['class'] = iris.target
df_iris = df_iris[df_iris['class'] != 2]
df_iris = df_iris[['petal length (cm)', 'petal width (cm)', 'class']]
X = df_iris.iloc[:, :-1].values
y = df_iris.iloc[:, -1].values
y = np.where(y==0, -1, 1)


sc = StandardScaler()
X_std = sc.fit_transform(X)


X_train, X_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, stratify=y)
print_info("X_test\n", X_test)
print_info("y_test\n", y_test)
hard_margin_svm = MySVM()
hard_margin_svm.fit(X_train, y_train)
y_pred = hard_margin_svm.predict(X_test)
accuracy = np.sum(y_pred == y_test) / len(y_test)
print_info("Accuracy: ", accuracy)

