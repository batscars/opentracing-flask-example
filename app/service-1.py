# -*- coding: utf-8 -*-
from gevent import monkey
monkey.patch_all()

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import logging
logging.basicConfig(level=logging.DEBUG)

from gevent.pywsgi import WSGIServer
from flask import Flask, request, jsonify
from lib.funcs import function_call
from opentracing_flask.tracer import create_tracer
from opentracing_flask import g_requests

app = Flask(__name__)
flask_tracer = create_tracer(service_name="svc-1", flask_app=app)


@app.route("/test_01", methods=["POST"])
def test_01():
    data = function_call(data=request.form.to_dict(), service="svc-1")
    resp_json = g_requests.post(url="http://localhost:5003/test_03", data=data).json()
    return jsonify(resp_json)


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()

