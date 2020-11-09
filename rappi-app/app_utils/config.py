#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import os

# Model version
version = '1.0.0'

# Project path
PRJ_DIR = '/'.join(os.path.abspath(__file__).split('/')[:-2])

# Path were artifacts are stored.
ARTIFACTS_PATH = os.path.join(
    PRJ_DIR,
    'app_utils/artifacts')

# Create folder if it does not exist
os.makedirs(
    ARTIFACTS_PATH,
    exist_ok=True)
