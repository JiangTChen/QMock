FROM qa-gov.cn.lab/mock-server-base:v1

# create app directory
WORKDIR /usr/src/app

COPY . .

EXPOSE 8080

CMD ["python", "server.py"]

LABEL version="1.0" description="Mock Server" by="Frank.Chen" name="Mock Server"