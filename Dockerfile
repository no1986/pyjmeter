FROM ubuntu:20.04 as builder

ENV VER 5.5

RUN apt-get update
RUN apt-get install -y curl openjdk-8-jdk
RUN curl https://dlcdn.apache.org//jmeter/binaries/apache-jmeter-${VER}.tgz | tar -zx -C /opt

ENV PATH $PATH:/opt/apache-jmeter-${VER}/bin

RUN curl -O https://jmeter-plugins.org/files/packages/jpgc-tst-2.5.zip
RUN apt-get install -y unzip
RUN unzip jpgc-tst-2.5.zip -d /opt/apache-jmeter-${VER}

FROM ubuntu:20.04

ENV VER 5.5

COPY --from=builder /opt/apache-jmeter-${VER} /opt/apache-jmeter-${VER}
RUN apt-get update \
    && apt-get install -y openjdk-8-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV PATH $PATH:/opt/apache-jmeter-${VER}/bin