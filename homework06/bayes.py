from math import log

import numpy as np


class NaiveBayesClassifier:
    def __init__(self, alpha):
        self.alpha = alpha
        self.dictionary = {}
        self.classes = {}

    def fit(self, X, y):
        """Fit Naive Bayes classifier according to X, y."""
        values, counts = np.unique(np.array(y), return_counts=True)
        words_per_class = {value: 0 for value in values}
        self.classes = {values[i]: counts[i] / len(y) for i in range(len(values))}
        for i, text in enumerate(x):
            for word in text:
                if word not in self.dictionary:
                    self.dictionary[word] = {value: 0 for value in values}
                self.dictionary[word][y[i]] += 1
                words_per_class[y[i]] += 1

        for word, counter in self.dictionary.items():
            probabilities = {
                key: (counter[key] + self.alpha)
                / (words_per_class[key] + self.alpha * len(self.dictionary))
                for key in counter.keys()
            }
            self.dictionary[word] = probabilities
    def predict(self, X):
        """Perform classification on an array of test vectors X."""
        predictions = []
        for text in x:
            predict = {key: log(value) for key, value in self.classes.items()}
            for word in text:
                if word in self.dictionary:
                    for key in predict.keys():
                        predict[key] += log(self.dictionary[word][key])

            predicted_classes = dict(sorted(predict.items(), key=lambda x: x[1]))
            predictions.append(list(predicted_classes)[-1])
        return predictions
    def score(self, X_test, y_test):
        """Returns the mean accuracy on the given test data and labels."""
        predicted = self.predict(x_test)
        guessed = 0
        for i, label in enumerate(y_test):
            if predicted[i] == label:
                guessed += 1
        return guessed / len(y_test)
