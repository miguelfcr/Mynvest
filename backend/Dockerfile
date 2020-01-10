FROM python:3.7
LABEL maintainer="miguel rodrigues <miguel.fcr@hotmail.com>"
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD [ "python", "run.py" ]