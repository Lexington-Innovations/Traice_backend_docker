

FROM python:3.8
WORKDIR '/app'
COPY . .
RUN pip install flask
RUN pip install pickle-mixin
RUN pip install pandas
RUN pip install numpy
RUN pip install scipy
RUN pip install lime
RUN pip install mysql-connector-python==8.0.23
RUN pip install json5==0.9.5
RUN pip install mpmath==1.1.0
ENTRYPOINT ["python"]
CMD ["flaskapp copy.py"]

