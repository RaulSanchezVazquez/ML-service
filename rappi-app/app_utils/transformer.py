#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import pandas as pd
import numpy as np

from app_utils import logger

# Init logs
logger.init()


# Feature list and data types
_features = {
    'order_id': 'str',
    'store_id': 'str',
    'to_user_distance': 'float',
    'to_user_elevation': 'float',
    'total_earning': 'float',
    'created_at': 'date'}

# Features that need encoding
_enc_features = [
    'store_id',
    'weekday']

# Do not use the following features (defensive case)
_forbidden_features = [
    'order_id',
    'created_at',
    'taken']


def get_encoder(categ_data, min_freq=5):
    """Get categorical encoder.

    Parameters
    -----------
    categ_data: pandas.DataFrame
        The data used to compute the encodings.
    min_freq: int
        Min frequency of a categorical item in order to compute target
        statistics.

    Returns
    -------
    categ_enc: dict
        A dictionary containing feature names, then a mapping of categorical
        value and a numeric score.

    Example
    --------
    ::

        >>> import pandas as pd
        >>> from app_utils import transformer
        >>> categ_data = pd.DataFrame({
            'store_id': ['1', '2', '2', '3', '3', '3'],
            'weekday': ['M', 'T', 'W', 'TH', 'F', 'S'],
            'taken': [1, 0, 1, 0, 0, 1]})

        >>> transformer.get_encoder(categ_data, min_freq=1)
        {'store_id': {'1': 1.0, '2': 0.5, '3': 0.333},
         'weekday': {'F': 0, 'M': 1, 'S': 1, 'T': 0, 'TH': 0, 'W': 1}}

        >>> transformer.get_encoder(categ_data, min_freq=3)
        {'store_id': {'3': 0.3333333333333333}, 'weekday': {}}

    """
    categ_enc = {}
    for f in _enc_features:
        freq_cnt = categ_data[f].value_counts()
        valid_entity = freq_cnt[freq_cnt >= min_freq].index

        entity_target_mean = categ_data.groupby(f)['taken'].mean()

        categ_enc[f] = entity_target_mean[
            entity_target_mean.index.isin(valid_entity)].to_dict()

    return categ_enc


def encode(data, categ_enc):
    """Apply categorical encoder.

    Parameters
    -----------
    data: pandas.DataFrame
        Dataframe containing the features to encode.
    categ_enc: dict
        The encoder object.

    Example
    --------
    ::

        >>> import pandas as pd
        >>> from app_utils import transformer
        >>> categ_enc = {'store_id': {'1': 1.0, '2': 0.5, '3': 0.333}}
        >>> data = pd.DataFrame({
            'store_id': ['1', '2', '2', '3', '3', '3']})
        >>> transformer.encode(data, categ_enc)
               store_id
            0     1.000
            1     0.500
            2     0.500
            3     0.333
            4     0.333
            5     0.333
    """

    X = data.copy()

    # Drop forbidden features (apply defensive case)
    features_to_drop = list(set(
        _forbidden_features
    ).intersection(
        X.columns))

    X = X.drop(features_to_drop, axis=1)

    # Encode categorical features
    for f, f_enc in categ_enc.items():
        X[f] = X[f].apply(
            lambda x: f_enc[x] if x in f_enc else np.nan)

    return X


def make_features(data):
    """Compute features.

    Parse data types and compute the following features:
        - weekday

    Parameters
    -----------
    data: pandas.DataFrame
        Dataframe containing information.

    Returns
    --------
    data: pandas.DataFrame
        Dataframe that contains more features than the original data.
    """
    data = data.copy()

    # Set correct data types
    logger._LOGGER.info('Set data types')
    for f, dtype in _features.items():
        logger._LOGGER.info('%s: %s' % (f, dtype))
        if dtype == 'str':
            data[f] = data[f].astype(str)
        elif dtype == 'float':
            data[f] = data[f].astype(float)
        elif dtype == 'date':
            data[f] = pd.to_datetime(data[f])

    # Compute features
    logger._LOGGER.info('Creating features')
    data['weekday'] = data['created_at'].dt.day_name()

    return data


def json_to_df(x):
    """Converts dict containing features to a dataframe.

    Parameters
    ----------
    x: dict
        Dictionary of a map of feature-names and feature-values.

    Returns
    --------
    x: pandas.DataFrame
        Dataframe containing a single row.
    """
    missing_features = set(_features) - set(x.keys())

    if len(missing_features) > 0:
        return None

    x = pd.DataFrame([x])

    return x
