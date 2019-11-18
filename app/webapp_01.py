# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
from gevent.pywsgi import WSGIServer
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask, request, jsonify
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


def init_jaeger_tracer(service_name='test-flask-app-01', jaeger_host=os.getenv("JAEGER_HOST", "localhost")):
    config = Config(config={'sampler': {'type': 'const', 'param': 1}, 'local_agent': {'reporting_host': jaeger_host}},
                    service_name=service_name,
                    validate=True)
    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracing(jaeger_tracer, True, app)
    return tracer


flask_tracer = init_jaeger_tracer()


@app.route("/test_01", methods=["POST"])
def test():
    return jsonify(request.form.to_dict())


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
