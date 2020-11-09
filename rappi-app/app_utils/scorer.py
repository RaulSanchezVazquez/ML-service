#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import os
import pickle

from app_utils import config


MODEL_PATH = os.path.join(
    config.ARTIFACTS_PATH,
    'xgb_model.pkl')


_xgb_model = None


def save(xgb_model):
    """Save an xgb classfier.

    Parameters
    -----------
    xgb_model: xgboost.XGBClassifier
    """

    # save
    pickle.dump(xgb_model, open(MODEL_PATH, "wb"))


def load():
    """Load the model.

    If this method is invoqued multiple times the model is just loaded once.
    """
    global _xgb_model

    # load
    if _xgb_model is None:
        _xgb_model = pickle.load(open(MODEL_PATH, "rb"))

    return


def predict_proba(x):
    """Get model predictions.

    Returns
    --------
    y_score: np.array
        The model scores.
    """

    global _xgb_model

    y_score = _xgb_model.predict_proba(x)

    return y_score
