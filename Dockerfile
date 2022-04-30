FROM python:3.7

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY . /usr/src/app

RUN pip3 install -r requirements.txt --no-cache-dir

EXPOSE 8501

ENTRYPOINT [ "streamlit", "run", "app.py" ]