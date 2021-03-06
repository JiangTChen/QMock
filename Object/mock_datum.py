from constant import MockDataParameters as MDP
from constant import MockDataParameterRequest as MDRq
from constant import MockDataParameterResponse as MDRs
from constant import MockDataExtra as MDEx
from constant import MockDataExtraCallBack as MDECB

import json


class MockDatum:
    def __init__(self, json_obj: dict):
        self.request = MockRequest(json_obj.get(MDP.REQUEST) if json_obj.get(MDP.REQUEST) else {})
        self.response = MockResponse(json_obj.get(MDP.RESPONSE) if json_obj.get(MDP.RESPONSE) else {})
        self.extra = MockExtra(json_obj.get(MDP.EXTRA) if json_obj.get(MDP.EXTRA) else {})
        self.__original_json_obj = json_obj

    @property
    def json_obj(self):
        json_obj = {MDP.REQUEST: self.request.json_obj, MDP.RESPONSE: self.response.json_obj}
        if self.extra:
            json_obj[MDP.EXTRA] = self.extra.json_obj
        return json_obj

    def __str__(self):
        js_obj = self.json_obj
        return json.dumps(js_obj)

    def __repr__(self):
        return self.__str__()


class MockRequest:
    def __init__(self, json_obj: dict):
        self.url = json_obj.get(MDRq.URL) if json_obj.get(MDRq.URL) else '/'
        self.method = json_obj.get(MDRq.METHOD) if json_obj.get(MDRq.METHOD) else 'GET'
        self.query_parameters = json_obj.get(MDRq.QUERY_PARAMETERS)  # if json_obj.get(MDRq.QUERY_PARAMETERS) else ''
        self.body_patterns = json_obj.get(MDRq.BODY_PATTERNS)  # if json_obj.get(MDRq.BODY_PATTERNS) else ''

    @property
    def json_obj(self):
        json_obj = {MDRq.URL: self.url,
                    MDRq.METHOD: self.method}
        if self.query_parameters:
            json_obj[MDRq.QUERY_PARAMETERS] = self.query_parameters
        if self.body_patterns:
            json_obj[MDRq.BODY_PATTERNS] = self.body_patterns
        return json_obj


class MockResponse:
    def __init__(self, json_obj: dict):
        self.headers = json_obj.get(MDRs.HEADERS)
        self.status = json_obj.get(MDRs.STATUS) if json_obj.get(MDRs.STATUS) else 200
        self.body = json_obj.get(MDRs.BODY)

    @property
    def json_obj(self):
        json_obj = {MDRs.STATUS: self.status}
        if self.headers:
            json_obj[MDRs.HEADERS] = self.headers
        if self.body:
            json_obj[MDRs.BODY] = self.body
        return json_obj


class MockExtra:
    def __init__(self, json_obj: dict):
        self.delay = json_obj.get(MDEx.DELAY)  # if json_obj.get(MDEx.DELAY) else 0
        self.permanent = json_obj.get(MDEx.PERMANENT)
        self.user = json_obj.get(MDEx.USER)
        # self.date = json_obj.get(MDEx.DATE)
        self.disable = json_obj.get(MDEx.DISABLE)
        self.comments = json_obj.get(MDEx.COMMENTS)
        self.step = json_obj.get(MDEx.STEP)
        self.times = json_obj.get(MDEx.TIMES)
        self.last_call_time = json_obj.get(MDEx.LASTCALLTIME)
        self.matching_rate = json_obj.get(MDEx.MATCHING_RATE)
        self.callback = MockExtraCallBack(json_obj.get(MDEx.CALLBACK) if json_obj.get(MDEx.CALLBACK) else {})
        # self._matching_rate = json_obj.get(MDEx.MATCHING_RATE)
        # self.operation = json_obj.get(MDEx.OPERATION)

    # @property
    # def matching_rate(self):
    #     return self._matching_rate
    #
    # @matching_rate.setter
    # def matching_rate(self, value):
    #     self._matching_rate = value

    @property
    def json_obj(self):
        json_obj = {}
        if self.delay:
            json_obj[MDEx.DELAY] = self.delay
        if self.permanent:
            json_obj[MDEx.PERMANENT] = self.permanent
        if self.user:
            json_obj[MDEx.USER] = self.user
        if self.disable:
            json_obj[MDEx.DISABLE] = self.disable
        if self.comments:
            json_obj[MDEx.COMMENTS] = self.comments
        if self.step:
            json_obj[MDEx.STEP] = self.step
        if self.times:
            json_obj[MDEx.TIMES] = self.times
        if self.last_call_time:
            json_obj[MDEx.LASTCALLTIME] = self.last_call_time
        if self.matching_rate:
            json_obj[MDEx.MATCHING_RATE] = self.matching_rate
        return json_obj


class MockExtraCallBack:
    def __init__(self, json_obj: dict):
        self.url = json_obj.get(MDECB.URL)
        self.method = json_obj.get(MDECB.METHOD)
        self.headers = json_obj.get(MDECB.HEADERS)
        self.body = json_obj.get(MDECB.BODY)
        self.delay = json_obj.get(MDECB.DELAY)
        self.type = json_obj.get(MDECB.TYPE)

    @property
    def json_obj(self):
        json_obj = {}
        if self.url:
            json_obj[MDECB.URL] = self.url
        if self.method:
            json_obj[MDECB.METHOD] = self.method
        if self.headers:
            json_obj[MDECB.HEADERS] = self.headers
        if self.body:
            json_obj[MDECB.BODY] = self.body
        if self.delay:
            json_obj[MDECB.DELAY] = self.delay
        return json_obj


if __name__ == '__main__':
    data = {}
    mock_datum = MockDatum(data)
    ll = [mock_datum, mock_datum]
    dd = [data, data]
    dict
    print(ll)
    print(dd)
