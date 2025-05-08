FROM python:3.12.10-slim

# install libgomp1 for lightgbm
RUN apt-get update && apt-get install -y --no-install-recommends libgomp1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY sales_forecast_config.yaml /app/sales_forecast_config.yaml
COPY sales_forecast.py /app/sales_forecast.py

CMD ["serve", "run", "sales_forecast_config.yaml"]

