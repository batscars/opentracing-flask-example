# -*- coding: utf-8 -*-
from opentracing import global_tracer
from opentracing_instrumentation import get_current_span
from functools import wraps
from opentracing import Format


def trace_rpc(func):
    @wraps(func)
    def _wrappper(*args, **kwargs):
        with global_tracer().start_active_span(func.__name__, child_of=get_current_span()) as scope:
            headers = {}
            global_tracer().inject(scope.span.context, Format.HTTP_HEADERS, headers)
            kwargs["headers"] = headers
            result = func(*args, **kwargs)
        return result
    return _wrappper


def trace_func(func):
    @wraps(func)
    def _wrappper(*args, **kwargs):
        with global_tracer().start_active_span(func.__name__, child_of=get_current_span()):
            result = func(*args, **kwargs)
        return result
    return _wrappper