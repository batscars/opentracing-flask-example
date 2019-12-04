# -*- coding: utf-8 -*-
from decorators import trace_func, trace_rpc
import grequests
from requests import Session
g_session = Session()

@trace_func
def function_02(data):
    data["function_02"] = "function_02"
    return data


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
    req_list = [grequests.post(url=url, data=data, headers=headers, session=g_session)]
    ret_list = grequests.map(req_list)
    return ret_list[0]
    # return requests.post(url=url, data=data, headers=headers)