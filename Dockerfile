FROM python:3.5-alpine
ENV PYTHONUNBUFFERED 1

# Build-time metadata as defined at http://label-schema.org
ARG PACKTOOLS_BUILD_DATE
ARG PACKTOOLS_VCS_REF
ARG PACKTOOLS_WEBAPP_VERSION

ENV PACKTOOLS_BUILD_DATE ${PACKTOOLS_BUILD_DATE}
ENV PACKTOOLS_VCS_REF ${PACKTOOLS_VCS_REF}
ENV PACKTOOLS_WEBAPP_VERSION ${PACKTOOLS_WEBAPP_VERSION}

LABEL org.label-schema.build-date=$PACKTOOLS_BUILD_DATE \
      org.label-schema.name="Packtools WebApp - development build" \
      org.label-schema.description="PACKTOOLS WebApp main app" \
      org.label-schema.url="https://github.com/scieloorg/packtools/" \
      org.label-schema.vcs-ref=$PACKTOOLS_VCS_REF \
      org.label-schema.vcs-url="https://github.com/scieloorg/packtools/" \
      org.label-schema.vendor="SciELO" \
      org.label-schema.version=$PACKTOOLS_WEBAPP_VERSION \
      org.label-schema.schema-version="1.0"

RUN apk --update add --no-cache \
    gcc build-base linux-headers git libc-dev libxml2-dev libxslt-dev py3-lxml

COPY . /app
WORKDIR /app

RUN pip --no-cache-dir install -e .[webapp]

RUN make compile_messages
RUN chown -R nobody:nogroup /app

USER nobody
EXPOSE 8000

HEALTHCHECK --interval=5m --timeout=3s \
  CMD curl -f http://localhost:8000/ || exit 1

CMD webapp runserver --processes 3 --host 0.0.0.0 --port 8000
