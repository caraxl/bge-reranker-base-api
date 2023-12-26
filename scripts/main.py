from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import uvicorn
from datetime import datetime
from typing import List,Dict
import torch
import os,json,logging
from ast import literal_eval
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class MyAPI:
    def __init__(self,):
        self.app = FastAPI()
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model_path = "/home/app/model/bge-reranker-base"
        print(f"开始执行模型加载")
        self.load_model()
        print("模型加载成功")

    def get_current_time(self,):
        '''
        功能：获取当前时间，时间格式：yyyy-mm-dd hh:mm:ss
        '''
        # 获取当前时间
        current_time = datetime.now()
        # 格式化为 "yyyy-mm-dd hh:mm:ss" 格式
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return formatted_time

    # 加载模型
    def load_model(self,):
        print(
            f"本次加载模型的设备为：{'GPU: ' + torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU.'}"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(self.model_path).to(self.device)
        # self.model = model.eval()




    def rerank(self,text_pairs:List[List[str]]):
        '''
        功能：对检索出的文本进行重排序
        text_pairs示例：
        pairs = [['what is panda?', 'hi'],
                 ['what is panda?',
                   'The giant panda (Ailuropoda melanoleuca), sometimes called a panda bear or simply panda, is a bear species endemic to China.']]

        '''

        with torch.no_grad():
            inputs = self.tokenizer(text_pairs, padding=True, truncation=True, return_tensors='pt', max_length=512).to(self.device)
            scores = self.model(**inputs, return_dict=True).logits.view(-1, ).float()
            scores = scores.cpu().tolist()
        return scores


    def start(self):
        @self.app.post('/bge-reranker-base/post')
        # url = "http://192.168.31.232:6008/bge-reranker-base/post"
        async def handle_post_request(request: Request):
            data = await request.body()
            request_time = self.get_current_time()
            logger.info(f"接受到数据：\n{json.loads(data)}")
            try:
                data = json.loads(data)
                text_pairs = literal_eval(data["text_pairs"])
                rerank_scores = self.rerank(text_pairs=text_pairs)
                response_time = self.get_current_time()
                code = 200
                response_data = {
                                     "text_pairs": text_pairs,
                                     "rerank_scores": rerank_scores,
                                     "request_time":request_time,
                                     "response_time":response_time,
                                     "code": code
                                     }
                return JSONResponse(content=response_data)

            except Exception as e:
                logger.info(f"{data}embedding失败！原因：\n{e}")
                code = -1
                data = json.loads(data)
                text_pairs = data["text_pairs"]
                rerank_scores = []
                response_time = self.get_current_time()
                response_data = {
                                      "text_pairs": text_pairs,
                                     "rerank_scores": rerank_scores,
                                     "request_time":request_time,
                                     "response_time":response_time,
                                     "code":code
                }
                return JSONResponse(content=response_data)

        uvicorn.run(self.app, host='0.0.0.0', port=6009)


if __name__ == "__main__":
    log_dir = "/home/app/log"
    os.makedirs(log_dir,exist_ok=True)
    log_path = os.path.join(log_dir,"log.txt")
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s|%(levelname)s|%(thread)d|%(name)s-%(lineno)d| - %(message)s",
        handlers=[logging.FileHandler(filename=log_path, encoding='utf-8', mode='a+'),
                  logging.StreamHandler()]
    )
    logger = logging.getLogger(__name__)
    try:
        my_api = MyAPI()
        my_api.start()
    except Exception as e:
        logger.info(f"API启动失败！\n报错：\n{e}")

