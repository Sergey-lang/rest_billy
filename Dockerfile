FROM  python:3.11.5

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

COPY . /usr/src/app/
RUN pip install --no-cache-dir -r requrements.tsx

ENV TZ Europe/Moskow
ENV TOKEN_USER=os.getenv('TOKEN_USER')
ENV VERSION=os.getenv('VERSION')
ENV DOMAIN=os.getenv('DOMAIN')

CMD ["python", "manage.py"]