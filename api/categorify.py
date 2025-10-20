from sklearn.base import BaseEstimator, TransformerMixin
import pandas as pd


class Categorify(BaseEstimator, TransformerMixin):
    def __init__(self, cat_columns=None):
        self.cat_columns = cat_columns
        self.categories_ = {}

    def fit(self, X, y=None):
        for col in self.cat_columns:
            self.categories_[col] = X[col].astype("category").cat.categories
        return self

    def transform(self, X):
        X = X.copy()
        for col in self.cat_columns:
            X[col] = pd.Categorical(X[col], categories=self.categories_[col])
        return X
