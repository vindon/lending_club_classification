import logging
import util as dfmt
from sklearn.feature_selection import VarianceThreshold
import numpy as np


class FeatureSelection:
    """
    Class that encapsulates all relevant feature selection methods.
    """
    @dfmt.timed
    def variance_threshold(self, dframe=None, columns=None, skip_columns=None, thresh=0.0, autoremove=False):
        """
         Wrapper for sklearn variance threshold to for pandas dataframe
        :param dframe:
        :param columns:
        :param skip_columns:
        :param thresh:
        :param autoremove:
        :return:
        """
        logging.debug("Finding low-variance features")
        removed_features=[]
        try:
            all_columns = dframe.columns

            # remove the skip columns
            remaining_cols = all_columns.drop(skip_columns)

            # get length of new index.
            max_index = len(remaining_cols) - 1

            skipped_idx = [all_columns.get_loc(column) for column in skip_columns]

            for idx, item in enumerate(skipped_idx):
                if item > max_index:
                    diff = item - max_index
                    skipped_idx[idx] -= diff
                if item == max_index:
                    diff = item - len(skip_columns)
                    skipped_idx[idx] -= diff
                if idx == 0:
                    skipped_idx[idx] = item

            skipped_values = dframe.iloc[:skipped_idx].values

            X = dframe.loc[:, remaining_cols].values

            vt = VarianceThreshold(threshold=thresh)

            vt.fit(X)

            feature_indices = vt.get_support(indices=True)

            feature_names = [remaining_cols[idx] for idx, _ in enumerate(remaining_cols) if idx in feature_indices]

            removed_features = list(np.setdiff1d(remaining_cols, feature_names))

            logging.debug("Found %d low - variance columns " % len(removed_features))

        except Exception as e:
            logging.error(e)
            logging.error("Could not remove low variance features, some thing went wrong")
            print(e)
            pass

        return dframe, removed_features
