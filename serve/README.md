
# Kaggle Sales Forecasting Model Serving
Model serving is implemented using Ray Serve and FastAPI. Ray Serve creates a Ray cluster and able to scales as the number of requests go up or down.

* Ray Serve: https://docs.ray.io/en/latest/serve/index.html

* FastAPI: https://fastapi.tiangolo.com/

This service can be deployed locally or using docker. See below for instructions and the Serving API.

# Local Model Serving
## Python Environment
* Do this if you want to run the model serving application locally.
* Don't need this if you are running the model serving in a docker container.

* Install conda or mamba (recommended) and create a new environment with Python 3.12.10.
* See ../model/README.md for details on how to install conda or mamba.
```shell
mamba create -n kagsalesserve python=3.12.10
mamba activate kagsalesserve
pip install -r requirements.txt

## Run the model serving application locally
serve run sales_forecast:sales_app
```

# Docker Container Model Serving

## Install docker
Install docker, if needed:

https://www.docker.com/

## docker build
```shell
docker build -t kag_sales_serve_image .
```

## Run docker container
  ```shell
  docker run -d --name kag_sales_serve_cont -p 8000:8000 kag_sales_serve_image
  ```
* This will run the container in detached mode (-d) and map port 8000 in the container to port 8000 on the host machine. 
* You can access the model serving application at http://localhost:8000/
* In case, host:8000 is in use, change the option to -p 8111:8000 if you want to change the host machine port to 8111.

### Notes
* You can ignore this, used to create config file for Ray serve.
* Create Ray serve run config
* creates a config with host as 0.0.0.0 (instead of default 127.0.0.1) and port as 8000
```shell
serve build sales_forecast:sales_app -o sales_forecast_config.yaml

# run with config
serve run sales_forecast_config.yaml
```

# Test the model serving
* Tests the model serving application's API endpoints.
```shell
python test_sales_forecast.py
```

# API Endpoints

* GET / - Root endpoint
* GET /status - Check if the model is alive
* GET /reload - Reload the model from the registry. Useful if the model is updated in the registry.
* POST /predict - Predict sales for a given date, store, and item
   - {"date": "2018-01-21", "store": 10, "item": 23}

When the serve application is running, the documentation of the API endpoints is available at: http://localhost:8000/docs#/

# Notes on Model Serving with Ray Serve

Model serving is the process of deploying machine learning models to production so that they can be accessed and used by applications or users. It involves creating an API or interface that allows users to send requests to the model and receive predictions in response. There are several libraries and frameworks available for model serving, each with its own features and capabilities. Cloud providers like AWS, Azure, and GCP also offer their own model serving solutions. For this project, we are using Ray Serve and FastAPI.


### What is Ray Serve?
Ray Serve is a scalable model serving library that allows you to deploy and manage machine learning models in production. With Ray Serve, you can easily create a scalable and distributed serving architecture that can handle high traffic and large workloads. It is built on top of Ray, a distributed computing framework that allows you to run Python code in parallel across multiple machines. Ray Serve provides a simple API for deploying and managing models, as well as features like autoscaling, load balancing, and versioning.

Ray Serve is designed to be easy to use and integrate with existing machine learning workflows. It supports a wide range of machine learning frameworks, including TensorFlow, PyTorch, and Scikit-learn. Ray Serve also provides a simple way to deploy models as REST APIs, using FastAPI, making it easy to integrate with web applications and other services.

More information: https://docs.ray.io/en/latest/serve/index.html

### Why not use just FastAPI or Flask?
We could have simply used FastAPI or Flask to create a REST API for the model, but Ray Serve provides additional features like autoscaling and load balancing that make it a better choice for production deployments. Ray Serve also allows you to easily deploy multiple models and manage their versions, which can be useful in a production environment where you may need to deploy multiple models or update existing ones.

### Status endpoint
'/status' and also the root endpoint '/' are used to check if the model is alive and running. This is useful for monitoring and debugging purposes.


### Loading the model and making predictions
When the application starts, the model is loaded into memory from the registry using the `load_model` function. The `predict` function is called when a request is received. The model is not reloaded for each request, which can improve performance. If the frequency of requests is low, we can offload the model to disk and reload it when a request is received. However, for this project, want to showcase the scalability of Ray Serve, so we are keeping the model in memory. 

### Reloading the model

In a production environment, the model may be updated or replaced with a new version. To show case reloading the model, we can use the `/reload` endpoint. This will reload the model from the registry and update the predictions. This is useful when we want to update the model without restarting the application. The assumption is that the model is updated in the registry and the new version is available. Ideally, we should have a versioning system in place to manage the different versions of the model. This can be done using a model registry like MLflow.