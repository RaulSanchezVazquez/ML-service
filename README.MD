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
cd rappi-app
docker build -t rappi-app .
docker run -d -p 5000:5000 --name rappi-app rappi-app -v rappi-app:/app
```

```bash
cd rappi-mysql
docker build -t rappi-mysql .
docker run -d -p 5001:5001 --name rappi-mysql -e MYSQL_ROOT_PASSWORD=rappi-secret rappi-mysql
```

## Test the API

```python
import os
import json
import urllib3

http = urllib3.PoolManager()

response = http.request(
     'GET',
     'http://0.0.0.0:5000',
     headers={'Content-Type': 'application/json'})

response = json.loads(
    response.data.decode('utf-8'))

response
```




    {'version': '1.1.0'}




```python
body = {
    'order_id': 1,
    'store_id': 2,
    'to_user_distance': 0.0,
    'to_user_elevation': 0.0,
    'total_earning': 10000,
    'created_at': '2020-09-07T20:02:17Z'}

response = http.request(
    'POST',
    'http://0.0.0.0:5000/score',
    body=json.dumps(body).encode('utf-8'),
    headers={'Content-Type': 'application/json'})

response = json.loads(
    response.data.decode('utf-8'))

response
```




    {'execution_time': 0.02066326141357422,
     'order_id': 1,
     'store_id': 2,
     'version': '1.1.0',
     'x': '{"store_id": NaN, "to_user_distance": 0.0, "to_user_elevation": 0.0, "total_earning": 10000.0, "weekday": 0.9083583369052722}',
     'x_raw': '{"order_id": "1", "store_id": "2", "to_user_distance": 0.0, "to_user_elevation": 0.0, "total_earning": 10000.0, "created_at": "2020-09-07 20:02:17+00:00", "weekday": "Monday"}',
     'y_score': 0.31567850708961487}
