import pandas as pd
import numpy as np
import time
import datetime as dt
import sklearn.metrics
import sklearn.svm
import sklearn.svm.libsvm


class TrueValuedClassifier:
    def fit(self,A,A_csv,b):
        return self

    def predict(self,A,A_csv):
        return np.ones(A.shape[0])


