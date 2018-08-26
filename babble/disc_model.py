import random

from sklearn.linear_model import LogisticRegression

from metal.utils import convert_labels
from metal.metrics import metric_score

class LogisticRegressionWrapper(object):
    """A wrapper around scikit-learn's LogisticRegression class

    The wrapper is necessary both to convert labels from categorical to one-zero
    and to match the interface expected by snorkel-metal's ModelTuners.
    """
    def __init__(self, C=1.0, penalty='l2', seed=None):
        if seed:
            random.seed(seed)
        self.model = LogisticRegression(C=C, penalty='l2')

    def train(self, X, Y, X_dev=None, Y_dev=None, **kwargs):
        Y_bin = convert_labels(Y, 'categorical', 'onezero')
        self.model.fit(X, Y_bin)

    def predict(self, X):
        return self.model.predict(X)

    def score(self, X, Y, metric='f1', verbose=True):
        Y = convert_labels(Y, 'categorical', 'onezero')
        Y_p = self.predict(X)

        metric_list = metric if isinstance(metric, list) else [metric]
        scores = []
        for metric in metric_list:
            score = metric_score(Y, Y_p, metric)
            scores.append(score)
            if verbose:
                print(f"{metric.capitalize()}: {score:.3f}")

        if isinstance(scores, list) and len(scores) == 1:
            return scores[0]
        else:
            return scores

