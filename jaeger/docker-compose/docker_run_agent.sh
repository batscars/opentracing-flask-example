#!/usr/bin/env bash
docker run -d --name jaeger-agent \
    -p 5775:5775/udp \
    -p 6831:6831/udp \
    -p 6832:6832/udp \
    -p 5778:5778 \
    --restart=always \
    jaegertracing/jaeger-agent --reporter.grpc.host-port=localhost:14250
