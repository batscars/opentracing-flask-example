# -*- coding: utf-8 -*-
import os
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask, request, jsonify
import logging
import requests
from opentracing_instrumentation.client_hooks import install_all_patches
import time
from functools import wraps
from app.decorators import trace_rpc, trace_func

logging.basicConfig(level=logging.DEBUG)
app = Flask(__name__)



def init_jaeger_tracer(service_name='top_service', jaeger_host=os.getenv("JAEGER_HOST", "10.170.24.242")):
    config = Config(config={'sampler': {'type': 'const', 'param': 1}, 'local_agent': {'reporting_host': jaeger_host}},
                    service_name=service_name,
                    validate=True)
    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracing(jaeger_tracer, True, app)
    return tracer


flask_tracer = init_jaeger_tracer()
install_all_patches()


@trace_rpc
def call_app_01(url, data, headers=None):
    return requests.post(url=url, data=data, headers=headers)


@trace_func
def function_00(data):
    data["function_00"] = "function_00"
    return data


@app.route("/test_00", methods=["POST"])
def test_00():
    data = function_00(data=request.form.to_dict())
    resp_json = call_app_01(url="http://localhost:5001/test_01", data=data).json()
    return jsonify(resp_json)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

