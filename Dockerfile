FROM alpine
LABEL author='renothing' tags='openvpn,openvpn-sqlite-auth' description='openvpn server with sqlite auth based on alpine'
#set language enviroments
ENV LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 \
    TIMEZONE="Asia/Shanghai" 
#install software
#RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.ustc.edu.cn/g;s/http/https/g' /etc/apk/repositories && apk --upgrade update && \ 
RUN apk update && \ 
    apk add openvpn tzdata python execline && \
    cp /usr/share/zoneinfo/${TIMEZONE} /etc/localtime && \
    echo "${TIMEZONE}" > /etc/timezone && \
    rm -rf /var/cache/apk/* /tmp/* ~/.pearrc
ADD . /usr/lib/openvpn/plugins/openvpn-sqlite-auth
WORKDIR /etc/openvpn
