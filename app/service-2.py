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


app = Flask(__name__)
flask_tracer = create_tracer(service_name="svc-2", flask_app=app)


@app.route("/test_02", methods=["POST"])
def test_02():
    data = function_call(data=request.form.to_dict(), service="svc-2")
    return jsonify(data)


if __name__ == "__main__":
    http_server = WSGIServer(('0.0.0.0', 5002), app)
    http_server.serve_forever()
