# -*- coding: utf-8 -*-
from opentracing_flask.wrappers import func_call_wrapper

@func_call_wrapper
def function_call(data, service):
    data["function_call"] = "function_{}".format(service)
    return data

