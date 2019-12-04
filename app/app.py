# -*- coding: utf-8 -*-
from functools import wraps
from opentracing_instrumentation import get_current_span
from opentracing import global_tracer, Format


def trace_func(func):
    @wraps(func)
    def _wrappper(*args, **kwargs):
        with global_tracer().start_active_span(func.__name__, child_of=get_current_span()):
            result = func(*args, **kwargs)
        return result
    return _wrappper


def trace_rpc(func):
    @wraps(func)
    def _wrappper(*args, **kwargs):
        with global_tracer().start_active_span(operation_name=func.__name__, child_of=get_current_span()) as scope:
            headers = {}
            global_tracer().inject(scope.span.context, Format.HTTP_HEADERS, headers)
            print headers
            kwargs["headers"] = headers
            result = func(*args, **kwargs)
        return result
    return _wrappper