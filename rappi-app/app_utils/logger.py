#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import logging

_LOGGER = None


def init(name='root'):
    """Configures a global logger.

    If this method is invoqued multiple times the logger is just initialized
    once.

    Returns
    --------

    logger: logging.Logger
        Logger.

    Example
    --------
    ::

        >>> from app_utils import logger
        >>> logger.init()
        >>> logger._LOGGER.info('Log some message')
        2020-11-08 21:45:26,355 :: INFO :: <module> :: 6 :: Log some message
    """
    global _LOGGER

    if _LOGGER is not None:
        return

    # Log format.
    formatter = logging.Formatter(
        '%(asctime)s :: '
        '%(levelname)s :: '
        '%(funcName)s :: '
        '%(lineno)d :: '
        '%(message)s')

    # Create handler and set format.
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    # Create logger.
    logger = logging.getLogger(name)
    logger.propagate = False

    # Set level
    logger.setLevel(logging.INFO)

    # Attatch handler
    logger.addHandler(handler)

    _LOGGER = logger

    return
