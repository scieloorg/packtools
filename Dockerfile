FROM python:3.7-alpine AS build
COPY . /src
RUN pip install --upgrade pip \
    && pip install wheel
RUN cd /src \
    && python setup.py bdist_wheel -d /deps


FROM python:3.7-alpine

COPY --from=build /deps/* /deps/
COPY requirements.txt .
COPY optional-requirements.txt .

RUN apk add --no-cache --virtual .build-deps \
    make gcc libxml2-dev libxslt-dev musl-dev g++ \
    && apk add libxml2 libxslt jpeg-dev \
    && pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir gunicorn \
    && pip install --no-cache-dir raven \
    && pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -r optional-requirements.txt \
    && pip install --no-index --find-links=file:///deps -U packtools[webapp] \
    && apk --purge del .build-deps \
    && rm requirements.txt \
    && rm -rf /deps

WORKDIR /app

ENV PYTHONUNBUFFERED 1

USER nobody

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:8000", "packtools.webapp.app:app"]

