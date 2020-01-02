# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import gevent
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
import logging
logging.basicConfig(level=logging.DEBUG)
from lib.funcs import function_call
from opentracing_flask.tracer import create_tracer, get_global_span
from opentracing_flask import g_requests
from opentracing_flask.wrappers import func_call_wrapper

app = Flask(__name__)
flask_tracer = create_tracer(service_name="svc-0", flask_app=app)


@func_call_wrapper
def parreal_request(data):
    task_list = [gevent.spawn(g_requests.post, url="http://localhost:5001/test_01", data=data, parent_greenlet_span=get_global_span()),
                 gevent.spawn(g_requests.post, url="http://localhost:5002/test_02", data=data, parent_greenlet_span=get_global_span())]
    gevent.joinall(task_list)
    return dict(value_0=task_list[0].value.json(), value_1=task_list[1].value.json())


@app.route("/test_00", methods=["POST"])
def test_00():
    data = function_call(data=request.form.to_dict(), service="svc-0")
    return jsonify(parreal_request(data))


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()


