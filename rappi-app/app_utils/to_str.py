#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import json


def x_raw(x_raw):
    """
    """
    if 'created_at' in x_raw:
        x_raw['created_at'] = x_raw['created_at'].astype(str)

    x_raw_str = json.dumps(x_raw.iloc[0].to_dict())

    return x_raw_str


def x(x):
    """
    """

    x_raw_str = json.dumps(x.iloc[0].to_dict())

    return x_raw_str
