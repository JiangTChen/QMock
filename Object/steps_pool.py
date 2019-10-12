from Object.singleton import Singleton
from constant import DataParameter, DataExtraParameter
from utils.data_handler import is_rule_matched_response, is_query_parameters_matched, is_body_patterns_matched
from utils import utils
from datetime import datetime


class StepsPool:
    __metaclass__ = Singleton

    def __init__(self):
        self._pool = []

    def extend(self, responses, user=None):
        self._pool.extend(responses)

    def append(self, response, user=None):
        if DataExtraParameter.TIMES not in response:
            response[DataExtraParameter.TIMES] = 1
        self._pool.append(response)

    # def remove(self, response):
    #     last_call_time = response.get(DataExtraParameter.LASTCALLTIME)
    #     if last_call_time:
    #         current = datetime.now()
    #         if (current - last_call_time).seconds > 3:
    #             self._pool.remove(response)
    #             print("---removed---")
    #     else:
    #         self._pool.remove(response)

    def set_last_call_time(self, response):
        last_call_time = response.get(DataExtraParameter.LASTCALLTIME)
        if not last_call_time:
            self._pool[self._pool.index(response)][DataExtraParameter.LASTCALLTIME] = datetime.now()

    def get_responses(self, req, table_name, user=None):
        filtered_responses = []
        api_rule_without_module = utils.get_api_rule_without_module(req, table_name)
        # for response in self._pool:
        #     last_call_time = response.get(DataExtraParameter.LASTCALLTIME)
        #     if last_call_time:
        #         current = datetime.now()
        #         if (current - last_call_time).seconds > 3:
        #             self._pool.remove(response)
        for response in self._pool:
            if req.method in response[DataParameter.METHODS]:
                rule_match = is_rule_matched_response(api_rule_without_module, response)
                if rule_match and response.get(user) == user:
                    query_match = is_query_parameters_matched(req, response)
                    body_match = is_body_patterns_matched(req, response)
                    if query_match > 0 and body_match > 0:
                        filtered_responses.append(response)
        # if filtered_responses.__len__() > 1:
        for response in filtered_responses:
            last_call_time = response.get(DataExtraParameter.LASTCALLTIME)
            if last_call_time:
                current = datetime.now()
                if (current - last_call_time).seconds > 3:
                    times = response[DataExtraParameter.TIMES]
                    if times == 0:
                        self._pool.remove(response)
                        filtered_responses.remove(response)
                    elif times >= 99:
                        if (current - last_call_time).seconds > 600:
                            self._pool.remove(response)
                            filtered_responses.remove(response)
                    else:
                        index = filtered_responses.index(response)
                        filtered_responses[index][DataExtraParameter.TIMES] = times - 1

        # elif filtered_responses.__len__() == 1:
        #     response = filtered_responses[0]
        #     last_call_time = response.get(DataExtraParameter.LASTCALLTIME)
        #     if last_call_time:
        #         current = datetime.now()
        #         if (current - last_call_time).seconds > 600:
        #             self._pool.remove(filtered_responses[0])
        #             filtered_responses.remove(response)
        return filtered_responses
