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


# Features that need encoding.
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
    """

    X = data.copy()

    features_to_drop = list(set(
        _forbidden_features
    ).intersection(
        X.columns))

    X = X.drop(features_to_drop, axis=1)

    for f, f_enc in categ_enc.items():
        X[f] = X[f].apply(
            lambda x: f_enc[x] if x in f_enc else np.nan)

    return X


def make_features(data):
    """
    """
    data = data.copy()
    logger._LOGGER.info('Set data types')
    for f, dtype in _features.items():
        logger._LOGGER.info('%s: %s' % (f, dtype))
        if dtype == 'str':
            data[f] = data[f].astype(str)
        elif dtype == 'float':
            data[f] = data[f].astype(float)
        elif dtype == 'date':
            data[f] = pd.to_datetime(data[f])

    logger._LOGGER.info('Creating features')
    data['weekday'] = data['created_at'].dt.day_name()

    return data


def json_to_df(x):
    """
    """
    missing_features = set(_features) - set(x.keys())

    if len(missing_features) > 0:
        return None

    x = pd.DataFrame([x])

    return x
