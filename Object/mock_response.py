from constant import DataParameter_1 as DP
from constant import DataExtraParameter_1 as DEP
import json


class MockResponse:
    # def __init__(self, rule, value, methods, query_parameters="", body_patterns="", headers="", code=200, delay=0,
    #              permanent=False):
    #     self._rule = rule
    #     self._value = value
    #     self._methods = methods
    #     self._query_parameters = query_parameters
    #     self._body_patterns = body_patterns
    #     self._headers = headers
    #     self._code = code
    #     self._delay = delay
    #     self._permanent = permanent

    def __init__(self, json_obj: dict):
        self._rule = '/' if json_obj.get(DP.RULE) is None else json_obj.get(DP.RULE)
        self._value = '' if json_obj.get(DP.VALUE) is None else json_obj.get(DP.VALUE)
        self._methods = 'GET' if json_obj.get(DP.METHODS) is None else json_obj.get(DP.METHODS)
        self._query_parameters = '' if json_obj.get(DP.QUERY_PARAMETERS) is None else json_obj.get(DP.QUERY_PARAMETERS)
        self._body_patterns = '' if json_obj.get(DP.BODY_PATTERNS) is None else json_obj.get(DP.BODY_PATTERNS)
        self._headers = '' if json_obj.get(DP.HEADERS) is None else json_obj.get(DP.HEADERS)
        self._code = 200 if json_obj.get(DP.CODE) is None else json_obj.get(DP.CODE)
        self._delay = 0 if json_obj.get(DEP.DELAY) is None else json_obj.get(DEP.DELAY)
        self._permanent = json_obj.get(DEP.PERMANENT)
        self._user = json_obj.get(DEP.USER)
        self._date = json_obj.get(DEP.DATE)
        self._status = json_obj.get(DEP.STATUS)
        self._comments = json_obj.get(DEP.COMMENTS)
        self._operation = json_obj.get(DEP.OPERATION)

    @property
    def custom_response_json_obj(self):
        json_obj = {
            DP.RULE: self._rule,
            DP.VALUE: self._value,
            DP.METHODS: self._methods,
            DP.QUERY_PARAMETERS: self._query_parameters,
            DP.BODY_PATTERNS: self._body_patterns,
            DP.HEADERS: self._headers,
            DP.CODE: self._code,
            DEP.DELAY: self._delay,
            DEP.PERMANENT: False if self._permanent is None else self._permanent,
            DEP.USER: self._user
        }
        return json_obj

    @property
    def mock_json_obj(self):
        json_obj = {
            DEP.DATE: self._date,
            DEP.STATUS: self._status,
            DEP.COMMENTS: self._comments
        }
        json_obj.update(self.custom_response_json_obj)
        del json_obj[DEP.PERMANENT]
        return json_obj

    @property
    def history_json_obj(self):
        json_obj = {
            DEP.OPERATION: self._operation
        }
        json_obj.update(self.mock_json_obj)
        return json_obj

    @property
    def rule(self):
        return self._rule

    @property
    def permanent(self):
        return self._permanent

    @property
    def methods(self):
        return self._methods

    @property
    def user(self):
        return self._user


if __name__ == '__main__':
    cc = MockResponse({})
