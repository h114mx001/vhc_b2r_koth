FROM ubuntu:22.04 

RUN apt-get update -y && apt-get install -y python3 python3-pip python-is-python3 neovim gcc sudo

# debugging only, remove before releasing the chall
RUN echo "root:iloveyou" | chpasswd 

RUN useradd -m werkzeug

RUN adduser werkzeug sudo

WORKDIR /home/werkzeug

RUN mkdir /home/werkzeug/sources

COPY . /home/werkzeug/sources

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /home/werkzeug/sources/requirements.txt

# setuid cat - privesc gadget 1
RUN chmod +xs /usr/bin/cat

# crypto privesc gadget 
RUN chown root:werkzeug /home/werkzeug/sources/secret_box/crypto_me/crypto_me.py
RUN chmod +xs /home/werkzeug/sources/secret_box/crypto_me/crypto_me.py
RUN chown root:werkzeug /home/werkzeug/sources/secret_box/crypto_me/crypto_me_first
RUN chmod +xs /home/werkzeug/sources/secret_box/crypto_me/crypto_me_first

USER werkzeug

CMD ["python3", "/home/werkzeug/sources/main.py"]