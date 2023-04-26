FROM fadawar/docker-pyqt5

WORKDIR /usr/src/app

COPY src/ .

CMD ["python3", "./main.py"]

