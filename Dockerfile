FROM deeppavlov/base-gpu:0.17.6

RUN mkdir -p /app/
WORKDIR /app

RUN apt-get update && apt-get install git -y

COPY requirements.txt .

RUN pip install -r requirements.txt

RUN pip uninstall -y websockets

RUN pip install websockets

COPY . /app
