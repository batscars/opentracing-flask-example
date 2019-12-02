# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
from gevent.pywsgi import WSGIServer
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask, request, jsonify
import logging
import grequests
from opentracing_instrumentation.client_hooks import install_all_patches
import time
from functools import wraps

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)


def init_jaeger_tracer(service_name='flask-webapp-00', jaeger_host=os.getenv("JAEGER_HOST", "localhost")):
    config = Config(config={'sampler': {'type': 'const', 'param': 1}, 'local_agent': {'reporting_host': jaeger_host}},
                    service_name=service_name,
                    validate=True)
    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracing(jaeger_tracer, True, app)
    return tracer


flask_tracer = init_jaeger_tracer()
install_all_patches()


def trace_func(func):
    @wraps(func)
    def _wrappper(*args, **kwargs):
        with flask_tracer.tracer.start_active_span(func.__name__):
            result = func(*args, **kwargs)
        return result
    return _wrappper


@trace_func
def function_00():
    time.sleep(1)


@app.route("/test_00", methods=["POST"])
def test_00():
    function_00()
    data = request.form.to_dict()
    req = grequests.post("http://localhost:5002/test_01", data=data)
    resp_json = grequests.map([req])[0].json()
    return jsonify(resp_json)


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()

