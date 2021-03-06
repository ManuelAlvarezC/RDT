import numpy as np
import pandas as pd

from rdt.transformers.BaseTransformer import BaseTransformer


class NullTransformer(BaseTransformer):
    """Transformer for missing/null data."""

    def __init__(self, *args, **kwargs):
        """ initialize transformer """
        super().__init__(type=['datetime', 'number'], *args, **kwargs)

    def fit(self, col, col_meta, *args):
        self.col_name = col_meta['name']
        self.new_name = '?' + self.col_name

        if isinstance(col, pd.DataFrame):
            col = col[self.col_name]

        mean = col.mean()

        if not pd.isnull(mean) and col_meta['type'] == 'number':
            self.default_value = mean
        else:
            self.default_value = 0

    def transform(self, col, col_meta, *args):
        """Prepare the transformer to convert data and return the processed table.

        Args:
            col(pandas.DataFrame): Data to transform.
            col_meta(dict): Meta information of the column.
            missing(bool): Wheter or not handle missing values using NullTransformer.

        Returns:
            pandas.DataFrame
        """
        out = pd.DataFrame()
        out[self.new_name] = (pd.notnull(col) * 1).astype(int)
        out[self.col_name] = col.fillna(self.default_value)
        return out

    def reverse_transform(self, col, col_meta):
        """Converts data back into original format.

        Args:
            col(pandas.DataFrame): Data to transform.
            col_meta(dict): Meta information of the column.
            missing(bool): Wheter or not handle missing values using NullTransformer.

        Returns:
            pandas.DataFrame
        """
        output = pd.DataFrame()
        col_name = col_meta['name']
        new_name = '?' + col_name

        col.loc[col[new_name] == 0, col_name] = np.nan
        output[col_name] = col[col_name]
        return output
