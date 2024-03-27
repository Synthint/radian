FROM python:3.12 AS radian
WORKDIR /opt

RUN pip install poetry
COPY pyproject.toml poetry.lock ./
RUN poetry install
COPY ./radian/ ./radian
EXPOSE 80
CMD ["poetry", "run", "uvicorn", "--factory", "radian.backend.main:get_app", "--host", "0.0.0.0", "--port", "80", "--reload"]
