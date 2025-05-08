
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
