FROM python
COPY . /command
WORKDIR /command
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

RUN python parse.py