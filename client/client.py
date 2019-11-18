import requests

url = "http://localhost:5000/test_00"
data = dict(a=1, b=2, c=3)
resp = requests.post(url=url, data=data)
print resp.json()
