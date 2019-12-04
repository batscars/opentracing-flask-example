# -*- coding: utf-8 -*-
from decorators import trace_func, trace_rpc
import time
import grequests
import requests


@trace_func
def function_02():
    time.sleep(1)


@trace_func
def function_01(data):
    data["function_01"] = "function_01"
    return data


@trace_func
def function_00(data):
    data["function_00"] = "function_00"
    return data


@trace_rpc
def call_webapp(url, data, headers=None):
    # req_list = [grequests.post(url=url, data=data, headers=headers)]
    # ret_list = grequests.map(req_list)
    # return ret_list[0]
    return requests.post(url=url, data=data, headers=headers)