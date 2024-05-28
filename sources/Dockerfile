FROM ubuntu:22.04 

RUN apt-get update -y && apt-get install -y systemctl python3 python3-pip python-is-python3 neovim gcc sudo gdb wget locales cron binutils file

RUN systemctl enable cron
RUN systemctl start cron

RUN sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8  
ENV LANGUAGE en_US:en  
ENV LC_ALL en_US.UTF-8    

# debugging only, remove before releasing the chall
RUN echo "root:iloveyou" | chpasswd 

RUN useradd -m werkzeug

RUN adduser werkzeug sudo

WORKDIR /home/werkzeug

RUN mkdir /home/werkzeug/sources

COPY ./vinuni_cloud /home/werkzeug/sources

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /home/werkzeug/sources/requirements.txt

RUN chown werkzeug:werkzeug /home/werkzeug/sources/uploads

# setuid cat - privesc gadget 1
RUN chmod +xs /usr/bin/cat 

# ansible + cron - privesc gadget 2

RUN mkdir -p /opt/automated/tasks/webapp/
COPY ./ansible /opt/automated/tasks/webapp/
COPY ./ansible/cron /etc/cron.d/cron

# rwx: root, r: group, r: others
RUN chmod 0644 /etc/cron.d/cron
RUN crontab /etc/cron.d/cron

COPY ./ansible/reset_machine.sh /root/reset_machine.sh

# rwr: root, no access for group and others
RUN chmod 0700 /root/reset_machine.sh

# setup mini ctf challs
COPY ./secret_box /home/werkzeug/secret_box

# crypto privesc gadget 
RUN chown root:root /home/werkzeug/secret_box/crypto_me/crypto_me.py
RUN chmod +xs /home/werkzeug/secret_box/crypto_me/crypto_me.py
RUN chown root:root /home/werkzeug/secret_box/crypto_me/crypto_me_first
RUN chmod +xs /home/werkzeug/secret_box/crypto_me/crypto_me_first

# pwn privesc gadget
RUN chown root:root /home/werkzeug/secret_box/rop_me/rop_me
RUN chmod +xs /home/werkzeug/secret_box/rop_me/rop_me

# reverse privesc gadget
RUN chown root:root /home/werkzeug/secret_box/re_me/re_me
RUN chmod +xs /home/werkzeug/secret_box/re_me/re_me

# setup gef for players
RUN wget -O ./.gdbinit-gef.py -q https://gef.blah.cat/py
RUN echo source /home/werkzeug/.gdbinit-gef.py >> /home/werkzeug/.gdbinit

CMD ["cron", "-f"]