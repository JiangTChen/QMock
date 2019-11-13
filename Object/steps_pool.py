from Object.singleton import Singleton
from constant import ExtraParameters
from utils.data_handler import is_url_matched_response, is_query_parameters_matched, is_body_patterns_matched
from utils import global_utils
from datetime import datetime
from Object.mock_datum import MockDatum
import config


class StepsPool:
    __metaclass__ = Singleton

    def __init__(self):
        self.__pool = []

    @property
    def pool(self):
        return self.__pool

    def extend(self, mock_data, user=None):
        self.__pool.extend(mock_data)

    # def append(self, response, user=None):
    #     if DataExtraParameter_1.TIMES not in response:
    #         response[DataExtraParameter_1.TIMES] = 1
    #     self._pool.append(response)

    def append(self, mock_datum: MockDatum, user=None):
        if not mock_datum.extra.times:
            mock_datum.extra.times = 1
        self.__pool.append(mock_datum)

    # def remove(self, response):
    #     last_call_time = response.get(DataExtraParameter.LASTCALLTIME)
    #     if last_call_time:
    #         current = datetime.now()
    #         if (current - last_call_time).seconds > 3:
    #             self._pool.remove(response)
    #             print("---removed---")
    #     else:
    #         self._pool.remove(response)

    def set_last_call_time(self, datum):
        last_call_time = datum.get(ExtraParameters.LASTCALLTIME)
        if not last_call_time:
            self.__pool[self.__pool.index(datum)][ExtraParameters.LASTCALLTIME] = datetime.now()

    def get_data(self, req, table_name, user=None):
        filtered_data = []
        url_without_module = global_utils.get_url_without_module(req, table_name)
        # get matched data from pool and give filtered_data
        for mock_datum in self.__pool:
            if req.method in mock_datum.request.method and mock_datum.extra.times > 0:
                rule_match = is_url_matched_response(url_without_module, mock_datum)
                if rule_match and mock_datum.extra.user == user:
                    query_match = is_query_parameters_matched(req, mock_datum)
                    body_match = is_body_patterns_matched(req, mock_datum)
                    if query_match > 0 and body_match > 0:
                        filtered_data.append(mock_datum)
        res = []
        if config.cache_step_time > 0:
            for mock_datum in filtered_data:
                last_call_time = mock_datum.extra.last_call_time
                res.append(mock_datum)
                if last_call_time:
                    current = datetime.now()
                    if (current - last_call_time).seconds > config.cache_step_time:
                        times = mock_datum.extra.times
                        if times <= 1:
                            self.__pool.remove(mock_datum)
                            res.remove(mock_datum)
                        # elif times >= 99:  # delete datum if time out
                        #     if (current - last_call_time).seconds > 600:
                        #         self._pool.remove(mock_datum)
                        #         res.remove(mock_datum)
                        else:
                            index = res.index(mock_datum)
                            res[index].extra.times = times - 1
        else:
            res = filtered_data
        return res
