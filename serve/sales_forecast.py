import ray
from ray import serve
from fastapi import FastAPI

import numpy as np
from datetime import datetime
import lightgbm as lgb
from urllib.request import urlopen
import json

# Initialize fastapi server
app = FastAPI()

def load_model(model_registry_url):
    '''
    Load the model info from a Model Registry URL and load the model and guardrails
    :param model_registry_url: URL to the model registry
    :return: model, input guardrails, output guardrails
    '''
    with urlopen(model_registry_url) as url:
        model_info = json.load(url)
        print('==== Model registry info:', model_info) # leaving print for illustration, remove in prod

    # Load the model
    model_url = model_info['model_file']
    with urlopen(model_url) as url:
        model = lgb.Booster(model_str=url.read().decode('utf-8'))
    # print(model)
    return model, model_info['input_guardrails'], model_info['output_guardrails']

# Ray Serve deployment
# Multiple replicas serving the model, can be autoscaled with parameters.
@serve.deployment(num_replicas=2, ray_actor_options={"num_cpus": 0.2, "num_gpus": 0})
# @serve.deployment()
@serve.ingress(app)
class SalesForecast:
    def __init__(self):
        """ Initialize the model and guardrails """
        # load model from a simple Model Registry. Ideally, use something like MLFlow.
        self.model_registry_url = "https://raw.githubusercontent.com/shacholle/kagsales/refs/heads/main/model/model_registry.json"
        self.model, self.input_guardrails, self.output_guardrails = load_model(self.model_registry_url)

    @app.get("/")
    def root(self) -> str:
        """ Root endpoint """
        return "Sales Forecast Model is ready!"
    
    @app.get("/status")
    def status(self) -> str:
        """ Check if the model is alive """
        return "Alive"
    
    @app.get("/reload")
    def reload(self) -> str:
        """ Reload the model from the registry """
        self.model, self.input_guardrails, self.output_guardrails = load_model(self.model_registry_url)
        return "Model reloaded"

    @app.post("/predict")
    def pred(self, date: str, store: int, item: int) -> float:
        """
        predict sales for a given date, store, and item
        :param date: date in YYYY-MM-DD format
        :param store: store id
        :param item: item id
        :return: predicted sales
        """

        # Check input guardrails
        if not (self.input_guardrails['min_date'] <= date <= self.input_guardrails['max_date']):
            return -1.0 # Invalid input date
        if not (0 <= store <= self.input_guardrails['store_id_max']):
            return -2.0 # Invalid store id
        if not (0 <= item <= self.input_guardrails['item_id_max']):
            return -3.0 # Invalid item id
        

        # Pre-process input
        # Convert input text to a format suitable for the model
        print('==== input param: ', date, store, item) # leaving print for illustration, remove in prod
        dt = datetime.strptime(date, "%Y-%m-%d").date()
        # ['store', 'item', 'month', 'day', 'year']
        input = np.array([[store, item, dt.month, dt.weekday(), dt.year]])
        # print('input: ', input)
        # Run inference
        # input = np.array([[1,    1,    1,    0, 2018]])
        pred = self.model.predict(input)
        print('--pred', pred) # leaving print for illustration, remove in prod

        # Post-process output check output guardrails
        res = float(pred[0])
        MAX_SALES = 200
        if res > self.output_guardrails['max_value']:
            return MAX_SALES # Limit output to some max value
        return res

# Create the deployment
sales_app = SalesForecast.bind()