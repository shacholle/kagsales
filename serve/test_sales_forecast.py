import requests

host = "127.0.0.1"
# port = 8111
port = 8000


# Test the / endpoint
response = requests.get(f"http://{host}:{port}/")
res = response.json()
print("==Testing: /: ", res)

# Test the /status endpoint
response = requests.get(f"http://{host}:{port}/status")
res = response.json()
print("==Testing: /status:", res)

# Test the /predict endpoint
inp = {"date": "2018-01-02", "store": 1, "item": 1}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

inp = {"date": "2018-01-19", "store": 2, "item": 9}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

inp = {"date": "2018-01-21", "store": 10, "item": 23}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

# Input that fails guardrails

# past max date
inp = {"date": "2018-04-21", "store": 10, "item": 23}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

# pre min date
inp = {"date": "2017-04-21", "store": 10, "item": 23}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

# store id out of range
inp = {"date": "2018-01-21", "store": 100, "item": 25}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

# item id out of range
inp = {"date": "2018-01-21", "store": 10, "item": 100}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)

# Test the /reload endpoint
response = requests.get(f"http://{host}:{port}/reload")
res = response.json()
print("==Testing: /reload:", res)

# Test the /predict endpoint
inp = {"date": "2018-01-02", "store": 1, "item": 1}
print("=== Testing: /predict: ", "Input: ", inp)
response = requests.post(f"http://{host}:{port}/predict", params=inp)
res = response.json()
print("-- Sales:", res)