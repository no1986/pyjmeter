FROM python:3.11-slim as builder

WORKDIR /app

RUN pip install --upgrade pip wheel
RUN pip install poetry

COPY app /app

RUN poetry export -f requirements.txt --without-hashes --output /app/requirements.txt
RUN mkdir -p /app/wheelhouse
RUN pip wheel -w /app/wheelhouse -r /app/requirements.txt
RUN poetry build -f wheel
RUN mv dist/* /app/wheelhouse

FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /app/wheelhouse /app/wheelhouse
RUN pip install --upgrade pip wheelhouse \
    && pip install /app/wheelhouse/* \
    && rm -rf /app/wheelhouse
