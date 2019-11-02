# -*- coding: utf-8 -*-
import socket, json
from flask import request
import config
from collections import Iterable
from config import *
import time
from constant import *
from Object.mock_datum import MockDatum


def format_body_to_string(headers, value):
    if 'json' in headers.get("Content-Type"):
        if isinstance(value, dict):
            body = json.dumps(value)
        elif is_json(value):
            body = json.dumps(json.loads(value))
        else:
            body = value
    else:
        body = value
    return body


def get_post_body_content(req: request):
    # get raw in json
    try:
        body_content = req.json
    except:
        body_content = {}
    # get form
    if not body_content:
        form_body = req.form.to_dict()
        if len(form_body) != 0:
            body_content = form_body
    # get data
    if not body_content:
        data_body = req.data
        # convert the json string in data to json format
        if str(data_body).find('{') == 2 and str(data_body).find('}') == len(str(data_body)) - 2:
            body_content = json.loads(str(req.data)[str(req.data).find('{'):str(req.data).find('}') + 1])
    return body_content


def get_url_without_module(req, table_name):
    path = req.path[1:]
    url_path = path[path.find('/') + 1:]
    if table_name == url_path[1:]:  # for root
        url_path = '/'
    else:
        pos = url_path.find('/', 1)
        if pos == -1:
            pass
        else:
            url_path = url_path[pos + 1:]
    url_path = url_path.strip()
    return url_path


def replace_large_data(file_name, value):
    # file_name = 'LargeData'
    # import  file_name
    large_data_key = '${' + file_name
    file_name = data_package + '.' + file_name
    if value and large_data_key in value:
        start_position = value.find(large_data_key)
        end_position = value[start_position:].find('}')
        variable = value[start_position:start_position + end_position + 1]
        variable_name = value[start_position + len(large_data_key) + 1:start_position + end_position]
        large_data = eval(file_name + '.' + variable_name)
        if variable == value:
            value = eval(file_name + '.' + variable_name)
        elif isinstance(large_data, str):
            value = value.replace(variable, eval(file_name + '.' + variable_name))
    return value


def delay_for_response(mock_datum:MockDatum):
    try:
        delay = int(mock_datum.extra.delay)
        for i in range(delay):
            time.sleep(1)
            print("-------------delay:" + str(i) + "/" + str(delay))
    except:
        delay = None


def get_value_from_dict(my_dict: dict, my_key):
    res = []
    for key, value in my_dict.items():
        if key == my_key:
            res.append(value)
        elif isinstance(value, dict):
            res.extend(get_value_from_dict(value, my_key))
    return res


def is_json(obj):
    try:
        json.loads(obj)
    except Exception as e:
        return False
    return True


def is_static_file(rule):
    for suffix in config.static_files_format_list:
        if rule.endswith(suffix):
            return True
    return False


def database_router(rule):
    project = rule[:rule.find('/')]
    database_name = None
    if project in projects:
        database_name = project
    return database_name


def get_table_name(api_rule):
    if api_rule.count('/') < 1:
        table_name = api_rule
    else:
        table_name = api_rule[:api_rule.find('/')]
    return table_name


def get_request_contents(req: request):
    try:
        if len(req.values) != 0:
            parameters = 'values:' + str(req.values)
        elif req.json is not None:
            parameters = 'json:' + json.dumps(req.json)
        else:
            parameters = 'data:' + req.data.decode()
    except Exception as ex:
        parameters = 'error:' + str(ex)
    return parameters


def compare_obj(obj1, obj2):
    if obj1 == obj2:
        return True
    elif isinstance(obj1, Iterable) and isinstance(obj2, Iterable):
        if type(obj1) == type(obj2):
            if isinstance(obj1, str) and isinstance(obj1, str):
                if obj1 == obj2:
                    return True
                else:
                    return False
            elif isinstance(obj1, dict) and isinstance(obj2, dict):
                if sorted(obj1.keys()) == sorted(obj2.keys()):
                    for key in obj1.keys():
                        if not compare_obj(obj1.get(key), obj2.get(key)):
                            return False
                    return True
                else:
                    return False
            elif isinstance(obj1, (list, tuple)) and isinstance(obj2, (list, tuple)):
                try:
                    if sorted(obj1) == sorted(obj2):
                        return True
                    else:
                        return False
                except TypeError as err:
                    # [1,{1:2},2] have no idea
                    print(err)
                    return False
            else:
                print('Unsupported Iterable Type for:' + str(obj1) + 'and ' + str(obj2))
                return False

        else:
            return False
    else:
        return False


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

