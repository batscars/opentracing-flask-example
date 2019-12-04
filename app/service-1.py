# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import logging
logging.basicConfig(level=logging.DEBUG)

from gevent.pywsgi import WSGIServer
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask, request, jsonify
# from opentracing_instrumentation.client_hooks import install_all_patches
from lib.funcs import function_01, call_webapp

app = Flask(__name__)


def init_jaeger_tracer(service_name='svc-1', jaeger_host=os.getenv("JAEGER_HOST", "10.170.24.242")):
    config = Config(config={'sampler': {'type': 'const', 'param': 1}, 'local_agent': {'reporting_host': jaeger_host}},
                    service_name=service_name,
                    validate=True)
    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracing(jaeger_tracer, True, app)
    return tracer


flask_tracer = init_jaeger_tracer(service_name="svc-1")
# install_all_patches()


@app.route("/test_01", methods=["POST"])
def test_01():
    data = function_01(request.form.to_dict())
    resp_json = call_webapp(url="http://localhost:5003/test_03", data=data).json()
    return jsonify(resp_json)


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()

