FROM ubuntu
EXPOSE 5000
RUN ["/bin/bash", "-c", "apt-get update > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "apt-get install -y python3 > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "apt-get install -y python3-pip > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "apt-get install -y python3-venv > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "apt-get install -y python3-dev > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "apt-get install -y libpq-dev > /dev/null 2>&1"]
RUN mkdir /Musify
RUN mkdir /Musify/Musify
RUN mkdir /Musify/MusifyVenv
COPY ./Musify /Musify/Musify
WORKDIR /Musify/MusifyVenv
RUN ["/bin/bash", "-c", "python3 -m venv venv > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "source venv/bin/activate; python -m pip install grpcio > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "source venv/bin/activate; python -m pip install grpcio-tools > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "source venv/bin/activate; python -m pip install --upgrade wheel > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "source venv/bin/activate; python -m pip install psycopg2-binary==2.8.3 > /dev/null 2>&1"]
RUN ["/bin/bash", "-c", "source venv/bin/activate; python -m pip install --upgrade pip > /dev/null 2>&1"]
CMD ["/bin/bash", "-c", "cp /Musify/Musify/requirements.txt requirements.txt; source venv/bin/activate; pip install --no-cache-dir -r requirements.txt; cd /Musify/Musify; python run.py"]
