from Object.singleton import Singleton
from Object.custom_response_service_base import CustomResponsesServiceBase
from Object.mongoDB_service import MongoDBService
import config
from Object.mock_response import MockResponse
from constant import DataParameter as DP
from constant import DataExtraParameter as DEP
from constant import DataParameter
from utils.data_handler import is_rule_matched_response, is_dict_matched, is_query_parameters_matched, \
    is_body_patterns_matched


class CustomResponsesMongoDBService(CustomResponsesServiceBase):
    # __metaclass__ = Singleton

    def __init__(self):
        CustomResponsesServiceBase.__init__(self)
        self._db_service = MongoDBService(config.MongoDB_address, config.cache_database_name)
        self._db = self._db_service.database
        self._cache_table = self._db[config.cache_table_name]

    def add(self, response: MockResponse):
        inserted_id = self._cache_table.insert_one(response.custom_response_json_obj)
        return inserted_id

    def remove(self, rule, methods, user=None):
        query = {DP.RULE: rule, DP.METHODS: methods, DEP.USER: user}
        return self._cache_table.delete_many(query).deleted_count

    def clean(self):
        self._cache_table.drop()

    def get_responses(self, req, user=None):
        filtered_responses = []
        for response in self._cache_table.find():
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
        table = self._cache_table.find({}, {"_id": 0})
        temp = []
        for res in table:
            temp.append(res)
        return temp
