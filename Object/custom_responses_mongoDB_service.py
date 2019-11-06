from Object.singleton import Singleton
from Object.custom_response_service_base import CustomResponsesServiceBase
from Object.mongoDB_service import MongoDBService
import config
# from Object.mock_response import MockResponse
from Object.mock_datum import MockDatum
from constant import MockDataParameterRequest as MDRq
from constant import MockDataParameterResponse as MDRs
from constant import MockDataExtra as MDEx
from constant import MockDataParameters as MDPa
# from constant import DataParameter_1 as DP
# from constant import DataExtraParameter_1 as DEP
# from constant import DataParameter_1
from utils.data_handler import is_url_matched_response, is_dict_matched, is_query_parameters_matched, \
    is_body_patterns_matched


class CustomResponsesMongoDBService(CustomResponsesServiceBase):
    # __metaclass__ = Singleton

    def __init__(self):
        CustomResponsesServiceBase.__init__(self)
        self._db_service = MongoDBService(config.MongoDB_address, config.cache_database_name)
        self._db = self._db_service.database
        self._cache_table = self._db[config.cache_table_name]

    def add_mock_datum(self, mock_datum: MockDatum):
        inserted_id = self._cache_table.insert_one(mock_datum.json_obj)
        return inserted_id

    def add(self, mock_json_obj: dict):
        inserted_id = self._cache_table.insert_one(mock_json_obj)
        return inserted_id

    def remove(self, url, method, user=None):
        query = {MDPa.REQUEST+'.'+MDRq.URL: url, MDPa.REQUEST+'.'+MDRq.METHOD: method, MDPa.EXTRA+'.'+MDEx.USER: user}
        return self._cache_table.delete_many(query).deleted_count

    def clean(self):
        self._cache_table.drop()

    def get_data(self, req, user=None):
        filtered_responses = []
        for mock_datum_json in self._cache_table.find():
            mock_datum=MockDatum(mock_datum_json)
            if req.method in mock_datum.request.method:
                rule_match = is_url_matched_response(req.path, mock_datum)
                if rule_match and mock_datum.extra.user == user:
                    query_match = is_query_parameters_matched(req, mock_datum)
                    body_match = is_body_patterns_matched(req, mock_datum)
                    if query_match and body_match:
                        filtered_responses.append(mock_datum)
        return filtered_responses

    @property
    def json_obj(self):
        table = self._cache_table.find({}, {"_id": 0})
        temp = []
        for res in table:
            temp.append(res)
        return temp
