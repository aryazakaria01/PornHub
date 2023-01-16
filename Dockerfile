FROM python:3.10.6

WORKDIR /PornHub

RUN apt-get -y update

RUN apt-get -y install git gcc python3-dev

COPY requirements.txt requirements.txt

RUN pip3 install -U -r requirements.txt

COPY . .

CMD [ "python3", "-m" , "PornHub"]
