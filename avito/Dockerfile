FROM python:3
ENV PYTHONUNBUFFERED=1

WORKDIR /pfe/avito-scrapy-server


ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY ./scrapyd.conf /etc/scrapyd/

COPY ./requirements.txt ./

RUN pip install --upgrade pip
RUN pip install --default-timeout=100 future
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 6800


ENTRYPOINT ["scrapyd"]
