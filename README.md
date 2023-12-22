# bge-reranker-base-api
reranker模型的应用价值是在检索场景，在大模型的RAG场景下也经常被使用，核心目标是对Query召回的Answer们进行相关度重排序，reranker模型的输入是list of pairs，如：
```text
[['what is panda?', 'hi'],['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]
```
其中，'what is panda?'是Query，'hi'、 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.'是召回的Answer们。reranker模型的输入就是一个个QA对。
reranker模型的输出是list of score，如：
```text
 [-8.154394149780273, 6.182112216949463]
```
score列表中第一个元素表示第一个QA对的得分，列表中第二个元素表示第二个QA对的得分，然后可以按照得分对QA对进行排序，排序越靠前的Answer表示是与Query真正相关的Answer。

## 0.下载模型文件
- 模型文件存储路径：/home/app/model/bge-reranker-base
- 使用git clone下载模型文件：git clone https://www.modelscope.cn/Xorbits/bge-reranker-base.git
- 下载完毕后，需要安装git-lfs，代码如下：
```shell
cd /home/app/model/bge-reranker-base
sudo apt-get install git-lfs
git lfs install
git lfs pull

```

## 1.构建镜像
在Dockerfile所在路径执行下面命令创建镜像。
```shell
docker build -t bge-reranker-base-api:v1.0 .
```
## 2.启动镜像
### CPU

```sh
docker run -d -p 6009:6009  --name bge-reranker-base-api bge-reranker-base-api:v1.0
```

### GPU

> required nvidia-docker2

```sh
docker run -d -p 6009:6009 --gpus all --name bge-reranker-base-api bge-reranker-base-api:v1.0
```

## 3.测试服务

```python
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
    print("Response:", response.json())
else:
    print("Request failed with status code:", response.status_code)
```
返回结果：
```text
Response: {'text_pairs': [['what is panda?', 'hi'], ['what is panda?', 'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']], 'rerank_scores': [-8.154394149780273, 6.182112216949463], 'request_time': '2023-12-22 17:07:54', 'response_time': '2023-12-22 17:07:54', 'code': 200}

```

