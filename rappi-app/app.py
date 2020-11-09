#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Raul Sanchez-Vazquez
"""
import json
import time

from flask import Flask
from flask import request
from flask import jsonify

from app_utils import config
from app_utils import logger
from app_utils import encoder
from app_utils import transformer
from app_utils import scorer
from app_utils import to_str
from app_utils import rappy_mysql


# App.
app = Flask(__name__)

# Init objects
logger.init()
encoder.load()
scorer.load()


@app.route('/')
def index():
    """
    """
    return {"version": config.version}


@app.route('/score', methods = ['POST'])
def score():
    """

    Example
    --------
    ::

        body = {
            'order_id': '14364873',
            'store_id': '30000009',
            'to_user_distance': '2.4781006757058885',
            'to_user_elevation': '-72.71936035156295',
            'total_earning': '4200',
            'created_at': '2017-09-07T20:02:17Z',
            'taken': '0'}
    """
    start = time.time()

    body = request.json

    logger._LOGGER.info('Data: %s' % body)
    data = transformer.json_to_df(body)

    logger._LOGGER.info('Compute features')
    x_raw = transformer.make_features(data)

    logger._LOGGER.info('Compute X matrix')
    x = transformer.encode(x_raw, encoder._categ_enc)

    logger._LOGGER.info('Compute score')
    y_score = scorer.predict_proba(x)[0][1]
    logger._LOGGER.info('score: %s' % y_score)

    end = time.time()
    execution_time = end - start

    response = {
        'order_id': body['order_id'],
        'store_id': body['store_id'],
        'version': config.version,
        'execution_time': execution_time,
        'y_score': float(y_score),
        'x_raw': to_str.x_raw(x_raw),
        'x': to_str.x(x)}

    logger._LOGGER.info('Store response in bd')
    id_model_result = rappy_mysql.store_response(response)
    logger._LOGGER.info('Stored response id: %s' % id_model_result)

    logger._LOGGER.info('Response: %s' % response)
    response = jsonify(response)

    return response



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
