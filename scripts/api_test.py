import requests
import json
url = "http://localhost:6009/bge-reranker-base/post"
data = {
    "text_pairs":'''[['what is panda?', 'hi'],['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]'''
}
response = requests.post(url, data=json.dumps(data),headers={'Content-Type': 'application/json'})
# 打印响应
if response.status_code == 200:
    # 获取响应内容并打印
    response_data = response.json()
    print("Response:", response_data)
else:
    print("Request failed with status code:", response.status_code)
