# Reproduce the experiment and train the model.

In order to reproduce the model and its artifacs.
Create a conda environment following these steps:

```bash
$ cd notebooks
notebooks $ conda env create -f environment.yml
notebooks $ conda activate rappi-train
(rappi-train) notebooks$ which python
/some-path/anaconda3/envs/rappi-train/bin/python
```
Then, launch the jupyter notebook:

```bash
$ jupyter notebook
```

And create the model and its artifacs by running the notebook:
`notebooks/Training and Experiment.ipynb`

# Use Docker and run the serving of the model.

```bash
$ cd ML-service
ML-service $ docker-compose up
```

## Test the API

```python
import os
import json
import urllib3

http = urllib3.PoolManager()
```


```python
response = http.request(
     'GET',
     'http://0.0.0.0:5000',
     headers={'Content-Type': 'application/json'})

response = json.loads(
    response.data.decode('utf-8'))

response
```




    {'version': '1.0.0'}




```python
body = {
    'created_at': '2017-10-02 00:02:52+0000',
    'order_id': '15759823',
    'store_id': '900015235',
    'to_user_distance': 3.7915624271915673,
    'to_user_elevation': -1.2239990234370453,
    'total_earning': 9750.0}

response = http.request(
    'POST',
    'http://0.0.0.0:5000/score',
    body=json.dumps(body).encode('utf-8'),
    headers={'Content-Type': 'application/json'})

response = json.loads(
    response.data.decode('utf-8'))

response
```




    {'execution_time': 0.03294110298156738,
     'order_id': '15759823',
     'store_id': '900015235',
     'version': '1.0.0',
     'x': '{"store_id": 0.8791208791208791, "to_user_distance": 3.7915624271915673, "to_user_elevation": -1.2239990234370453, "total_earning": 9750.0, "weekday": 0.9083583369052722}',
     'x_raw': '{"created_at": "2017-10-02 00:02:52+00:00", "order_id": "15759823", "store_id": "900015235", "to_user_distance": 3.7915624271915673, "to_user_elevation": -1.2239990234370453, "total_earning": 9750.0, "weekday": "Monday"}',
     'y_score': 0.13863785564899445}



# Ensure that the response was saved on the DB


```python
import pandas as pd

from sqlalchemy import create_engine

engine = create_engine('mysql://root:rappi-secret@0.0.0.0:5001/rappi?charset=utf8')

data = pd.read_sql('SELECT * FROM model_response', engine)
data
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>created_at</th>
      <th>order_id</th>
      <th>store_id</th>
      <th>y_score</th>
      <th>x_raw</th>
      <th>x</th>
      <th>execution_time</th>
      <th>version</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>2020-11-09 05:24:16</td>
      <td>15759823</td>
      <td>900015235</td>
      <td>0.138638</td>
      <td>{"created_at": "2017-10-02 00:02:52+00:00", "o...</td>
      <td>{"store_id": 0.8791208791208791, "to_user_dist...</td>
      <td>0.032941</td>
      <td>1.0.0</td>
    </tr>
  </tbody>
</table>
</div>




```python

```
