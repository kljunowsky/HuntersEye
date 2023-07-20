FROM python:3.10.6-alpine

RUN apk add --no-cache git
RUN git clone https://github.com/kljunowsky/HuntersEye

WORKDIR /HuntersEye
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python", "HuntersEye.py"]
