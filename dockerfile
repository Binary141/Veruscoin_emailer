FROM python:3
WORKDIR /usr/src/app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

RUN pip install requests
COPY . .
CMD ["verus_mining_emailer.py"]

ENTRYPOINT ["python3"]
