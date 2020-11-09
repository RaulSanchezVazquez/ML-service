# Reproduce the experiment and train the model.

In order to reproduce the model and its artifacs.
Create a conda environment as follow:

```
$ cd notebooks
notebooks $ conda env create -f environment.yml
notebooks $ conda activate rappi-train
(rappi-train) notebooks$ which python
/some-path/anaconda3/envs/rappi-train/bin/python
```
Then, launch the jupyter notebook:
```
$ jupyter notebook
```

# Run locally

```
cd rappi-app
docker build -t rappi-app .
docker run -d -p 5000:5000 --name rappi-app rappi-app -v rappi-app:/app
```

```
cd rappi-mysql
docker build -t rappi-mysql .
docker run -d -p 5001:5001 --name rappi-mysql -e MYSQL_ROOT_PASSWORD=rappi-secret rappi-mysql
```

And run the notebook named:  `Test API.ipynb`
