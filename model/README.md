# Notes
* This folder contains the model training code and the model registry.
* Serving the model is done in the serve directory.

# Set up the Python Environment

Install conda or mamba (recommended) and create a new environment with Python 3.12.10.
Mamba and conda can be installed from 
https://github.com/conda-forge/miniforge
https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html

## With Mamba
```shell
# mamba is faster than conda, so use mamba if you have it installed
mamba create -n kagsalesmdl python=3.12.10
mamba activate kagsalesmdl

pip install -r requirements.txt
```

## With Conda
```shell
# conda is slower than mamba, so use mamba if you have it installed
conda create -n kagsalesmdl python=3.12.10
conda activate kagsalesmdl

pip install -r requirements.txt
```

## Note about editor
* I used vscode. If you use Jupyter Lab or Jupyter Notebook, you might need to install them in the environment as well.

# Model Training

* Original notebook: https://www.kaggle.com/code/ashishpatel26/light-gbm-demand-forecasting/notebook
* Data: https://www.kaggle.com/c/demand-forecasting-kernels-only/data

* Edited Notebook: light-gbm-demand-forecasting.ipynb
* For this task, since the focus on model serving, in the interest of time, I used the sample notebook to build the model and save the Light GBM model.
* Since the code is from many years ago, I had to make a few changes to the code to make it work with the latest version of Light GBM and other libraries.
* There is practically no feature engineering done in the notebook.
* Also, the training and validation split is done randomly instead proper time-series split of non-overlapping data.
* Happy to discuss the modeling aspects, during the call, if needed.
* The model is saved in the model directory as lgb_model.txt

# Simple Model Registry
* The model registry is a simple json file *model_registry.json* with the model type, the model path, sample input and output guardrails.

* Model Registry:
```json
{
  "model_type": "lightgbm",
  "model_file": "https://raw.githubusercontent.com/shacholle/shatemp/refs/heads/main/model/lgb_model.txt",
  "input_guardrails": {
    "min_date": "2018-01-01",
    "max_date": "2018-03-31",
    "store_id_max": 10,
    "item_id_max": 50
  },
  "output_guardrails": {
    "max_value": 200.0
  }
}
```
* The model registry is used by the model serving code to load the model from the url, validate the input and output, and serve the model.