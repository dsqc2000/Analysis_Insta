
 

FROM python:3.8

ENV PYTHONUNBUFFERED 1

WORKDIR /app

RUN apt-get -qq update \
	&& apt-get -qq install -y --no-install-recommends \
	libgl1-mesa-glx\
	&& apt-get -qq autoremove \
	&& apt-get -qq clean

# RUN apt-get install -y unzip && \
#     curl -Lo "/tmp/chromedriver.zip" "https://chromedriver.storage.googleapis.com/111.0.5563.64/chromedriver_linux64.zip" && \
#     curl -Lo "/tmp/chrome-linux.zip" "https://www.googleapis.com/download/storage/v1/b/chromium-browser-snapshots/o/Linux_x64%2F1097615%2Fchrome-linux.zip?alt=media" && \
#     unzip /tmp/chromedriver.zip -d /opt/ && \
#     unzip /tmp/chrome-linux.zip -d /opt/



# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/



# RUN apt-get update && apt-get install -y wget gnupg ca-certificates && \
#     wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
#     echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
#     apt-get update && apt-get install -y google-chrome-stable 

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .


EXPOSE 8000