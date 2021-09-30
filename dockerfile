FROM alpine
LABEL maintainer="cjt0226@qq.com"
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories
RUN apk --update --upgrade --no-cache add python3 py3-pip

# create app directory
WORKDIR /usr/src/app

# Install app dependencies
ADD requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python3", "server.py"]

LABEL version="1.0" description="Mock Server" by="Frank.Chen" name="Mock Server"