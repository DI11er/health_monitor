FROM python:3.7-alpine


ADD ./requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
# the steps above only depend on the requirements.txt file!
ADD . /app