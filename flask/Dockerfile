# IMAGE
# FROM tensorflow/tensorflow:2.12.0
FROM python:3.8-slim-buster

# Set working space directory
WORKDIR /app

# copy files to /app
COPY . .

# install audio libraries
# RUN apt-get update && apt-get install -y libsndfile1 libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg

RUN pip install --upgrade pip

# install python packages
# RUN pip install -r requirements.txt


# Runner
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]