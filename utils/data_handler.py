# -*- coding: utf-8 -*-

import constant
# from constant import DataParameter, DataExtraParameter, HTTPMethod, UnavailableStatus
from flask import request
from Object.database_service_base import BaseDBService
from global_vars import log
import utils.utils as utils
import json
import re
from Object.mock_response import MockResponse


def get_responses_for_request(database: BaseDBService, table_name, req: request):
    filtered_responses = []
    responses = database.get_available_contents_from(table_name)
    if responses is None:
        log.info(
            "Please check " + database.database_name() + " table:" + table_name + '\n' + req.method + ':' + req.url)
    elif len(responses) > 0:
        # "_" for root
        # get rule
        api_rule_without_module = utils.get_api_rule_without_module(req, table_name)
        for response in responses:
            if req.method in response[constant.DataParameter.METHODS]:
                rule_match = is_rule_matched_response(api_rule_without_module, response)
                if rule_match:
                    query_match = is_query_parameters_matched(req, response)
                    body_match = is_body_patterns_matched(req, response)
                    if query_match > 0 and body_match > 0:
                        response[constant.ResponseExtraParameter.MATCHING_RATE] = query_match + body_match
                        filtered_responses.append(response)
    return sorted(filtered_responses, key=lambda keys: keys[constant.ResponseExtraParameter.MATCHING_RATE])


def get_response_id(database: BaseDBService, table_name, custom_response: MockResponse):
    responses = database.get_contents_from(table_name)
    for response in responses:
        if compare_response(custom_response, response):
            return response.get(database.id_name)
    return None


def compare_response(custom_response: MockResponse, response: dict):
    compare_keys = [constant.DataParameter.RULE, constant.DataParameter.METHODS,
                    constant.DataParameter.QUERY_PARAMETERS,
                    constant.DataParameter.BODY_PATTERNS]
    custom_res = custom_response.custom_response_json_obj
    for key in compare_keys:
        custom_value = custom_res.get(key)
        if custom_value is None or custom_value == "":
            pass
        else:
            response_value = response.get(key)
            if utils.is_json(response_value):
                if isinstance(custom_value, str):
                    custom_value = custom_value.replace("'", '"')
                if utils.is_json(custom_value):
                    if json.loads(response_value) != json.loads(custom_value):
                        return False
                else:
                    return False
            elif type(custom_value) == type(response_value):
                if custom_value != response_value:
                    return False
    return True


def is_body_patterns_matched(req, response):
    if req.method == constant.HTTPMethod.POST:
        body_patterns = response.get(constant.DataParameter.BODY_PATTERNS)
        body_patterns = data_to_json(body_patterns)
        body_content = utils.get_post_body_content(req)
        return is_dict_matched(body_content, body_patterns)
    return 1


def is_query_parameters_matched(req, response):
    args = json.loads(json.dumps(req.args))
    query_parameters = response.get(constant.DataParameter.QUERY_PARAMETERS)
    query_parameters = data_to_json(query_parameters)
    return is_dict_matched(args, query_parameters)


def data_to_json(query_or_body):
    if not isinstance(query_or_body, dict):
        if utils.is_json(query_or_body):
            query_or_body = json.loads(query_or_body)
        elif isinstance(query_or_body, str):
            query_or_body = query_or_body.replace("'", '"')
            if utils.is_json(query_or_body):
                query_or_body = json.loads(query_or_body)
            elif utils.is_json(query_or_body.replace('\\', '\\\\')):
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
            if utils.compare_obj(prepared_content, request_content):
                return 1  # equal
            else:
                for key in prepared_content.keys():
                    prepared_content_value = prepared_content.get(key)
                    request_content_value = request_content.get(key)
                    prepared_content_value_str = str(prepared_content_value).replace('-', '\\-') #re.match unsupport '-' in "dd-authorization.pop-up.template-code"
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


def is_rule_matched_response(api_rule, response):
    if '(' in response[constant.DataParameter.RULE]:  # assert rule
        res = re.match(response[constant.DataParameter.RULE], api_rule)
        if res is not None and res.group() == api_rule:
            return True
    elif response[constant.DataParameter.RULE].strip() == api_rule:
        return True
    else:
        return False


def remove_unable_response(responses):
    responses_temp = []
    for response in responses:
        if response.__contains__(constant.DataExtraParameter.STATUS):
            status = response[constant.DataExtraParameter.STATUS]
            if status in constant.UnavailableStatus:
                pass
            else:
                responses_temp.append(response)
        else:
            responses_temp.append(response)
    return responses_temp

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
