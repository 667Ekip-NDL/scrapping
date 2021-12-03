FROM python:3.9.9-slim

WORKDIR /parser
COPY ./Pipfile .
COPY ./Pipfile.lock .

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

RUN mkdir result

COPY . .

VOLUME ["./result"]

ENTRYPOINT ["python", "./main.py"]