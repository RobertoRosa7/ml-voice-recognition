# IMAGE
FROM tensorflow/tensorflow:2.12.0

# Set working space directory
WORKDIR /app

# copy files to /app
COPY . /app

# install audio libraries
RUN apt-get update && apt-get install -y libsndfile1 libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0 ffmpeg libav-tools

# install python packages
RUN pip install -r requirements.txt

# Start application
CMD ["uwsgi", "app.ini"]