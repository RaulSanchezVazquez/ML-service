#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import json


def x_raw(x_raw):
    """Convert feature vector to a serializable json for the http request.

    Parameters
    ----------
    x_raw: pandas.DataFrame

    Returns
    -------
    x_raw_str: str
    """
    if 'created_at' in x_raw:
        x_raw['created_at'] = x_raw['created_at'].astype(str)

    x_raw_str = json.dumps(x_raw.iloc[0].to_dict())

    return x_raw_str


def x(x):
    """Convert feature vector to a serializable json for the http request.

    Parameters
    ----------
    x: pandas.DataFrame

    Returns
    -------
    x_str: str
    """

    x_str = json.dumps(x.iloc[0].to_dict())

    return x_str
