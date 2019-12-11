# -*- coding: utf-8 -*-


import copy
import sys

from flask import request

import config
from Object.database_service_base import BaseDBService
from config import data_package
from global_vars import log
import json
import re
from constant import MockDataParameters as MDPa
from constant import MockDataExtra as MDEx
from constant import HTTPMethod
from constant import VariablesInMockDatum
from Object.mock_datum import MockDatum
from utils import global_utils
# from utils.util import is_json
from Projects.wechat_DD.wechat_dd_utils import gen_response_xml, send_pay_res_notify
from utils import handle_variables

import threading

from utils.global_utils import is_json_str, send_request_with_specified_params


def get_data_for_request(database: BaseDBService, table_name, req: request):
    filtered_data = []
    data = database.get_available_contents_from(table_name)
    if data is None:
        log.info(
            "Please check " + database.database_name() + " table:" + table_name + '\n' + req.method + ':' + req.url)
    elif len(data) > 0:
        # "_" for root
        # get rule
        url_path_without_module = global_utils.get_url_without_module(req, table_name)
        for datum in data:
            mock_datum = MockDatum(datum)
            if req.method in mock_datum.request.method:
                url_path_match = is_url_matched_response(url_path_without_module, mock_datum)
                if url_path_match:
                    query_match = is_query_parameters_matched(req, mock_datum)
                    body_match = is_body_patterns_matched(req, mock_datum)
                    if query_match > 0 and body_match > 0:
                        # datum[ExtraParameters.MATCHING_RATE] = query_match + body_match
                        mock_datum.extra.matching_rate = query_match + body_match
                        filtered_data.append(mock_datum)
    # return filtered_data.sort(key=MockDatum.extra.matching_rate)
    return sorted(filtered_data, key=lambda one_mock_datum: one_mock_datum.extra.matching_rate)
    # return sorted(filtered_data, key=lambda keys: keys[ExtraParameters.MATCHING_RATE])


# def get_response_id(database: BaseDBService, table_name, custom_response: MockResponse):
#     responses = database.get_contents_from(table_name)
#     for response in responses:
#         if compare_response(custom_response, response):
#             return response.get(database.id_name)
#     return None
#
#
# def compare_response(custom_response: MockResponse, response: dict):
#     compare_keys = [constant.DataParameter_1.RULE, constant.DataParameter_1.METHODS,
#                     constant.DataParameter_1.QUERY_PARAMETERS,
#                     constant.DataParameter_1.BODY_PATTERNS]
#     custom_res = custom_response.custom_response_json_obj
#     for key in compare_keys:
#         custom_value = custom_res.get(key)
#         if custom_value is None or custom_value == "":
#             pass
#         else:
#             response_value = response.get(key)
#             if util.is_json(response_value):
#                 if isinstance(custom_value, str):
#                     custom_value = custom_value.replace("'", '"')
#                 if util.is_json(custom_value):
#                     if json.loads(response_value) != json.loads(custom_value):
#                         return False
#                 else:
#                     return False
#             elif type(custom_value) == type(response_value):
#                 if custom_value != response_value:
#                     return False
#     return True


def is_body_patterns_matched(req, mock_datum: MockDatum):
    if req.method == HTTPMethod.POST:
        body_patterns = data_to_json(mock_datum.request.body_patterns)
        body_content = global_utils.get_post_body_content(req)
        return is_dict_matched(body_content, body_patterns)
    return 1


def is_query_parameters_matched(req, mock_datum: MockDatum):
    args = json.loads(json.dumps(req.args))
    query_parameters = data_to_json(mock_datum.request.query_parameters)
    return is_dict_matched(args, query_parameters)


def data_to_json(query_or_body):
    if not isinstance(query_or_body, dict):
        if global_utils.is_json_str(query_or_body):
            query_or_body = json.loads(query_or_body)
        elif isinstance(query_or_body, str):
            query_or_body = query_or_body.replace("'", '"')
            if global_utils.is_json_str(query_or_body):
                query_or_body = json.loads(query_or_body)
            elif global_utils.is_json_str(query_or_body.replace('\\', '\\\\')):
                query_or_body = json.loads(query_or_body.replace('\\', '\\\\'))
            else:
                query_or_body = {}
        else:
            query_or_body = {}
    return query_or_body


def is_dict_matched(request_content, prepared_content):
    if request_content == prepared_content:
        return 1
    if request_content is None:
        request_content = {}
    if prepared_content is None:
        prepared_content = {}
    if request_content:
        unmatch_key_list = [key for key in prepared_content.keys() if key not in request_content.keys()]
        if not unmatch_key_list:
            if global_utils.compare_obj(prepared_content, request_content):
                return 1  # equal
            else:
                for key in prepared_content.keys():
                    prepared_content_value = prepared_content.get(key)
                    request_content_value = request_content.get(key)
                    prepared_content_value_str = str(prepared_content_value).replace('-',
                                                                                     '\\-')  # re.match unsupport '-' in "dd-authorization.pop-up.template-code"
                    request_content_value_str = str(request_content_value)
                    m = re.match(prepared_content_value_str, request_content_value_str)
                    if m is None:
                        return -1  # unmatch regular
                return 2  # match regular
        else:
            return -2  # key unmatch
    elif not prepared_content:
        return 3  # don't care
    else:
        return -3  # request content is null but  prepared content isn't null


# def is_dict_matched1(request_content, prepared_content):
#     unmatch_key_list = [key for key in request_content.keys() if key not in prepared_content.keys()]
#     if not unmatch_key_list:
#         for key in request_content.keys():
#             m = re.match(request_content.get(key), prepared_content.get(key))
#             if m is None:
#                 return False
#         return True
#     return False


def is_url_matched_response(url, mock_datum: MockDatum):
    mock_url = mock_datum.request.url.strip().lstrip('/')
    if '(' in mock_datum.request.url:  # assert rule
        res = re.match(mock_url, url)
        if res is not None and res.group() == url:
            return True
    elif mock_url == url:
        return True
    else:
        return False


def remove_disable_datum(responses):
    data_temp = []
    for response in responses:
        if response.__contains__(MDPa.EXTRA) and response.get(MDPa.EXTRA).__contains__(MDEx.DISABLE):
            disable = response.get(MDPa.EXTRA).get(MDEx.DISABLE)
            if disable:
                pass
            else:
                data_temp.append(response)
        else:
            data_temp.append(response)
    return data_temp


# class DataBaseHandler:
#     def __init__(self, db):
#         self._db = db
#
#     def get_tables(self):
#         return self._db.list_collection_names()
#
#     def is_table_exist(self, table_name):
#         table_list = self.get_tables()
#         if table_name in table_list:
#             return True
#         else:
#             return False

# def merge_headers(mock_datum: MockDatum):
    # if mock_datum.response.headers == {}:
    #     return mock_datum.response.headers
    # header_dict = copy.deepcopy(default_header_dict)
    # if mock_datum.response.headers and mock_datum.response.headers != "":
    #     mock_datum_headers = mock_datum.response.headers
    #     mock_datum_headers = json.loads(mock_datum_headers) if isinstance(mock_datum_headers,
    #                                                                       str) else mock_datum_headers
    #     header_dict.update(mock_datum_headers)
    # return header_dict


def replace_xml_for_random(xml_string, keyword, cdata=True):
    start = xml_string.find(keyword)
    if start > 0:
        end = xml_string[start:].find("}") + start
        keyword_full = xml_string[start:end + 1]
        keyword, types, size = keyword_full[2:-1].split("_")
        random_string = global_utils.gen_random_string(types, size)
        if cdata:
            random_string = "<![CDATA[" + random_string + "]]>"
        xml_string = xml_string.replace(keyword_full, random_string, 1)
        return replace_xml_for_random(xml_string, keyword, cdata)
    return xml_string


def replace_value_for_tag(xml_string, tag, value):
    start = xml_string.find(tag)
    keyword_list = list(tag)
    keyword_list.insert(1, "/")
    keyword_end = "".join(keyword_list)
    end = xml_string.find(keyword_end)
    orig_text = xml_string[start:end]
    xml_string = xml_string.replace(orig_text, value, 1)
    return xml_string


def get_xml_tag_keyword(xml_string, key):
    keyword_start = tag_end = xml_string.find(key)
    keyword_end = xml_string[keyword_start:].find("}") + keyword_start
    keyword_full = xml_string[keyword_start:keyword_end + 1]
    tag_start = xml_string[0:tag_end].rfind("<")
    tag = xml_string[tag_start + 1:tag_end - 1]
    return tag, keyword_full


def reassemble_response(mock_datum: MockDatum, req: request):
    # headers = merge_headers(mock_datum)
    headers = mock_datum.response.headers
    status = int(mock_datum.response.status if mock_datum.response.status else 200)
    body = mock_datum.response.body
    # body = replace_large_data(config.large_data_file_name, body)  # for execl resource
    if req.view_args.get("project_name") == config.Projects.wechat_DD and 'xml' in get_content_type_from(
            mock_datum.response.headers):
        body = gen_response_xml(mock_datum, req)

    if mock_datum.extra.callback.url:
        req_temp = copy.copy(req)
        if req.view_args.get("project_name") == config.Projects.wechat_DD:
            threading.Thread(target=send_pay_res_notify, args=(mock_datum, req_temp)).start()
            # executor.submit(wechat_dd_utils.send_callback(mock_datum, req))
        else:
            # send_callback(mock_datum, req_temp)
            threading.Thread(target=send_callback, args=(mock_datum, req_temp)).start()

    body = format_body_to_string(headers, body)
    body = handle_variables_for_str_dict(body, req)
    body = body if body else ''
    return body, headers, status


def get_first_value_from_dict_by_key(keyword, data: dict, cdata=True):
    for key, value in data.items():
        if isinstance(value, dict):
            return get_first_value_from_dict_by_key(keyword, value)
        elif keyword == key:
            if cdata:
                return "<![CDATA[" + value + "]]>"
            else:
                return value


def replace_xml_from_dict(xml_string, keyword, org_dict, cdata=True):
    end = xml_string.find(keyword)
    if end > 0:
        start = xml_string[0:end].rfind("<")
        tag = xml_string[start + 1:end - 1]
        value = get_first_value_from_dict_by_key(tag, org_dict)
        xml_string = xml_string.replace(keyword, value, 1)
        return replace_xml_from_dict(xml_string, keyword, org_dict, cdata)
    return xml_string


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


def format_body_to_string(headers, value):
    if 'json' in get_content_type_from(headers):
        if isinstance(value, dict):
            body = json.dumps(value)
        elif global_utils.is_json_str(value):
            body = json.dumps(json.loads(value))
        else:
            body = value
    else:
        body = value
    return body


def send_callback(mock_datum: MockDatum, req: request):
    method = mock_datum.extra.callback.method
    url = mock_datum.extra.callback.url
    if url.startswith(VariablesInMockDatum.FROM_REQUEST_PREFIX):
        res, orig_keyword = call_handle_variables_fun(url, req)
        url = res
    headers = mock_datum.extra.callback.headers
    body = mock_datum.extra.callback.body
    body = json.loads(body) if is_json_str(body) else body
    body = handle_variables_for_str_dict(body, req)
    delay = int(mock_datum.extra.callback.delay)
    send_request_with_specified_params(method, url, headers, body, delay)


def handle_variables_for_str_dict(body, req):
    if isinstance(body, dict):
        for key, value in body.items():
            if value.startswith("${"):
                res, orig_keyword = call_handle_variables_fun(value, req, key=key)
                body[key] = res
    elif isinstance(body, str):
        while body.find("${") >= 0:
            res, orig_keyword = call_handle_variables_fun(body, req)
            body = body.replace(orig_keyword, res, 1)
    return body


def call_handle_variables_fun(value, req, key=None):
    # value is a string with variables or the variables
    func_name, args, orig_keyword = covert_variable_mockdatum(value)
    obj_for_variable = getattr(handle_variables, func_name.lower())
    # args.append(req)
    res = obj_for_variable(args, req=req, key=key)
    return res, orig_keyword


def covert_variable_mockdatum(variable: str):
    start = variable.find("${")
    end = variable.find("}", start)
    orig_keyword = variable[start:end + 1]
    orig_keyword = orig_keyword.replace("'", "").replace('"', "")
    keywords = orig_keyword[2:- 1]
    split_pos = keywords.find("(")
    if split_pos > 0:
        fun_name = keywords[:split_pos]
        args = keywords[split_pos + 1:-1].split(",")
    else:
        fun_name = keywords
        args = []
    return fun_name, args, orig_keyword


def get_content_type_from(headers):
    if headers and "Content-Type" in headers:
        return headers.get("Content-Type")
    else:
        return ""
