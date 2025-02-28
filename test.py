# @Version  : 1.0
# @Author   : 故河
import requests

data = 'This is some raw data'
response = requests.post('http://127.0.0.1:5000/articles', data=data)
print(response.text)