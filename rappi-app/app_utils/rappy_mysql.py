#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

from app_utils import logger

logger.init()

from sqlalchemy import create_engine
from sqlalchemy import (
    Table, Column, Integer, String, MetaData, Float, DateTime)


def connect():
    """Creates sqlalchemy engine used connect to database.

    Return
    ------
    engine : sqlalchemy.engine.base.Engine
        sqlalchemy engined used to fetch data.

        'mysql://root:rappi-secret@0.0.0.0:5001/rappi?charset=utf8'
    """

    port = os.getenv('RAPPI_DB_PORT')
    host = os.getenv('RAPPI_DB_HOST')
    user = os.getenv('RAPPI_DB_USER')
    passw = os.getenv('RAPPI_DB_PASSW')
    db_name = os.getenv('RAPPI_DB_NAME')

    connect_str = "mysql://%s:%s@%s:%s/%s?charset=utf8" % (
        user, passw, host, port, db_name)

    logger._LOGGER.info(connect_str)

    engine = create_engine(connect_str)

    return engine


def get_model_response():
    """
    """
    meta = MetaData()

    model_response = Table(
       'model_response',
       meta,
       Column('id', Integer, primary_key=True),
       Column('created_at', DateTime),
       Column('order_id', Integer),
       Column('store_id', Integer),
       Column('y_score', Float),
       Column('x_raw', String),
       Column('x', String),
       Column('execution_time', Float),
       Column('version', String))

    return model_response


def store_response(response):
    """

    Parameters
    ----------
    response: dict

    Example
    -------
    ::

        response = {
            'order_id': 1,
            'store_id': 2,
            'version': '1.0.0',
            'execution_time': 1,
            'y_score': 0.1,
            'x': 'x_test',
            'x_raw': 'x_test'
        }

        store_response(response)

    """
    # Get connection eng.
    engine = connect()

    # Fetch table object
    model_response = get_model_response()

    # Insert operation
    insert = model_response.insert().values(response)

    # Execute the insert
    result = engine.execute(insert)

    # Get model_response ID
    id_model_result = result.inserted_primary_key

    # Close connection to database
    engine.dispose()

    return id_model_result
