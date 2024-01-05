FROM robd003/python3.10:latest
WORKDIR /home/app
# 添加本地项目文件添加到镜像
COPY . /home/app
RUN pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install --no-cache-dir -r /home/app/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 6009
CMD [ "python3", "/home/app/scripts/main.py" ]
