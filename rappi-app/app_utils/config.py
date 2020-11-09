#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 17:01:31 2020

@author: Raul Sanchez-Vazquez
"""
import os

version = '1.1.0'

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
