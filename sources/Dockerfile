FROM ubuntu:22.04 

RUN apt-get update -y && apt-get install -y python3 python3-pip python-is-python3 neovim gcc 

# debugging only, remove before releasing the chall
RUN echo "root:root" | chpasswd 

RUN useradd -m werkzeug

WORKDIR /home/werkzeug

RUN mkdir /home/werkzeug/sources

COPY . /home/werkzeug/sources

RUN chown -R werkzeug:werkzeug /home/werkzeug

USER werkzeug

RUN pip install -r /home/werkzeug/sources/requirements.txt

CMD ["python3", "/home/werkzeug/sources/main.py"]