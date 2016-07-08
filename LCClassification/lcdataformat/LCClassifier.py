import pandas as pd
import numpy as np
import sys
import logging
from logging.config import fileConfig
import time
import datetime as dt
import sklearn.metrics
import sklearn.svm
import sklearn.svm.libsvm

from lcdataextractor import LcDataExtractor


class TrueValuedClassifier:
    def fit(self,A,A_csv,b):
        return self

    def predict(self,A,A_csv):
        return np.ones(A.shape[0])



def run(file_name):
    ###Initialize Logging for the application
    fileConfig('logging_config.ini')
    logger = logging.getLogger()
    logger.debug("Testing Logging")
    dataExtractor = LcDataExtractor()
    df = dataExtractor.create(file_name)
    print(df.head())


if __name__ == '__main__':
    run(sys.argv[1])