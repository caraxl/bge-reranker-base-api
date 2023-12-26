FROM robd003/python3.10:latest
WORKDIR /app
ADD ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
# 添加本地项目文件添加到镜像
COPY . /home/app
EXPOSE 6009
CMD [ "python3", "/home/app/scripts/main.py" ]
