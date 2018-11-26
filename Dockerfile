FROM python:3.6-jessie
RUN mkdir /shield
WORKDIR /shield
ADD requirements.txt /shield
RUN pip install -r requirements.txt
ADD . /shield
CMD ["python", "-m", "unittest", "test_esentai.TestEsentai.test_signin"]