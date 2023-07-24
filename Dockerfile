FROM python:3.8-slim-buster

COPY . .

RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple

CMD ["python", "app.py"]
