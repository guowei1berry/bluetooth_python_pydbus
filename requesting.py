import requests

r = requests.post('http://localhost:8000/post', json={"key": "value"})