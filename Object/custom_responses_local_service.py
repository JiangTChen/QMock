from copy import deepcopy

from Object.singleton import Singleton
from Object.custom_response_service_base import CustomResponsesServiceBase
from Object.mock_response import MockResponse
from constant import DataParameter
from utils.data_handler import is_rule_matched_response, is_dict_matched, is_query_parameters_matched, \
    is_body_patterns_matched


class CustomResponsesLocalService(CustomResponsesServiceBase):

    def __init__(self):
        CustomResponsesServiceBase.__init__(self)
        self._custom_responses_pool = []

    def add(self, response: MockResponse):
        self._custom_responses_pool.append(response)

    def remove(self, rule, methods, user=None):
        count = 0
        temp = self._custom_responses_pool.copy()
        for response in temp:
            if response.rule == rule and response.user == user:
                for method in methods:
                    if method in response.methods:
                        self._custom_responses_pool.remove(response)
                        count = count + 1
                    break
        return count

    def clean(self):
        self._custom_responses_pool = []

    def get_response(self, rule, method, user='', request_query=None, request_body=None):
        for response in self._custom_responses_pool:
            response = response.json_obj
            if method in response[DataParameter.METHODS]:
                rule_match = is_rule_matched_response(rule, response)
                if rule_match and response.user == user:
                    query_match = is_dict_matched(request_query, response)
                    body_match = is_dict_matched(request_body, response)
                    if query_match > 0 and body_match > 0:
                        if response.permanent:
                            return response
                        else:
                            temp = response
                            self._custom_responses_pool.remove(response)
                            return temp
        return None

    def get_responses(self, req, user=None):
        filtered_responses = []
        for response in self._custom_responses_pool:
            response = response.json_obj
            if req.method in response[DataParameter.METHODS]:
                rule_match = is_rule_matched_response(req.path, response)
                if rule_match and response.get(user) == user:
                    query_match = is_query_parameters_matched(req, response)
                    body_match = is_body_patterns_matched(req, response)
                    if query_match and body_match:
                        filtered_responses.append(response)
        return filtered_responses

    @property
    def json_obj(self):
        res = []
        for response in self._custom_responses_pool:
            res.append(response.json_obj)
        return res
