# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import gevent
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from gevent.pywsgi import WSGIServer
from jaeger_client import Config
from flask_opentracing import FlaskTracing
from flask import Flask, request, jsonify
import logging
logging.basicConfig(level=logging.DEBUG)
from lib.funcs import function_00, call_webapp
from opentracing_instrumentation import get_current_span

app = Flask(__name__)


def init_jaeger_tracer(service_name='svc-0', jaeger_host=os.getenv("JAEGER_HOST", "10.170.24.242")):
    config = Config(config={'sampler': {'type': 'const', 'param': 1}, 'local_agent': {'reporting_host': jaeger_host}},
                    service_name=service_name,
                    validate=True)
    jaeger_tracer = config.initialize_tracer()
    tracer = FlaskTracing(jaeger_tracer, True, app)
    return tracer


flask_tracer = init_jaeger_tracer(service_name="svc-0")


@app.route("/test_00", methods=["POST"])
def test_00():
    task_list = []
    data = function_00(data=request.form.to_dict())
    task_list.append(gevent.spawn(call_webapp, url="http://localhost:5001/test_01", data=data, span=get_current_span()))
    task_list.append(gevent.spawn(call_webapp, url="http://localhost:5002/test_02", data=data, span=get_current_span()))
    gevent.joinall(task_list)
    resp_json = task_list[0].value.json().update(task_list[1].value.json())
    return jsonify(resp_json)


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


