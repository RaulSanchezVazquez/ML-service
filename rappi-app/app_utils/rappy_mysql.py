#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import os

from sqlalchemy import \
    Table, Column, Integer, String, MetaData, Float, DateTime, create_engine

from app_utils import logger

# Init
logger.init()


def connect():
    """Creates sqlalchemy engine used connect to database.

    Returns
    -------
    engine : sqlalchemy.engine.base.Engine
        sqlalchemy engined used to fetch data.
    """

    port = os.getenv('RAPPI_DB_PORT')
    host = os.getenv('RAPPI_DB_HOST')
    user = os.getenv('RAPPI_DB_USER')
    passw = os.getenv('RAPPI_DB_PASSW')
    db_name = os.getenv('RAPPI_DB_NAME')

    connect_str = "mysql://%s:%s@%s:%s/%s?charset=utf8" % (
        user, passw, host, port, db_name)

    engine = create_engine(connect_str)

    return engine


def get_model_response():
    """Get Table use to store models.

    Returns
    -------
    model_response : sqlalchemy.sql.schema.Table
        Table object.
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
    """Persis the response object in DB.

    Parameters
    ----------
    response: dict

    Returns
    --------
    id_model_result: int
        The ID of the response stored in DB.

    Example
    -------
    ::

        >>> from app_utils import rappy_mysql
        >>> response = {
                'order_id': 1,
                'store_id': 2,
                'version': '1.0.0',
                'execution_time': 1,
                'y_score': 0.1,
                'x': 'x_test',
                'x_raw': 'x_test'}

        >>> id_insert = rappy_mysql.store_response(response)
        >>> id_insert[0]
        1

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

    return id_model_result[0]
