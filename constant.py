from enum import Enum

HistoryTable = "-history-"


class MockDataParameters:
    REQUEST = "request"
    RESPONSE = "response"
    EXTRA = "Extra"


class MockDataParameterRequest:
    URL = "url"
    METHOD = "method"
    QUERY_PARAMETERS = "queryParameters"
    BODY_PATTERNS = "bodyPatterns"


class MockDataParameterResponse:
    HEADERS = "headers"
    STATUS = "status"
    BODY = "body"


class MockDataExtra:
    DISABLE = "Disable"
    COMMENTS = "Comments"
    DELAY = "Delay"
    PERMANENT = "Permanent"
    STEP = "Step"
    TIMES = "Times"
    USER = "User"
    ENCRYPT = "Encrypt"
    LASTCALLTIME = "LastCallTime"
    MATCHING_RATE = 'MatchingRate'
    CALLBACK = "CallBack"


class MockDataExtraCallBack:
    URL = "url"
    METHOD = "method"
    HEADERS = "headers"
    BODY = "body"
    DELAY = "Delay"
    TYPE = "Type"


# column name for data
class DataParameter_1:
    RULE = "rule"
    METHODS = "methods"
    QUERY_PARAMETERS = "queryParameters"
    BODY_PATTERNS = "bodyPatterns"
    HEADERS = "headers"
    CODE = "code"
    VALUE = "value"


# column name for extra
class DataExtraParameter_1:
    STATUS = "Status"
    COMMENTS = "Comments"
    DELAY = "Delay"
    PERMANENT = "Permanent"
    USER = "User"
    DATE = 'Date'
    OPERATION = 'Operation'
    STEP = "Step"
    TIMES = "Times"
    LASTCALLTIME = "LastCallTime"


# HTTP METHOD
class HTTPMethod:
    GET = "GET"
    POST = "POST"
    DELETE = "DELETE"
    PUT = "PUT"


# HttpMethods = Enum('HttpMethods', 'GET POST DELETE PUT')

# GET = "GET"
# POST = "POST"
# DELETE = "DELETE"
# PUT = "PUT"


# DB
class DatabaseName:
    DB_HCCN = "HCCN"
    DB_CAPPBE = "CAPPBE"
    DB_UTA = "UTA"


# Filter
# UnavailableStatus = ['FALSE', False, 'Duplicated']


# Data source Type
class DataBaseType:
    EXCEL = "Execl"
    MONGODB = "MongoDB"


class DataBaseService:
    EXCEL_SERVICE = "ExeclService"
    MONGODB_SERVICE = "MongoDBService"


class CacheDataService:
    LOCAL_SERVICE = "CustomResponsesLocalService"
    MONGODB_SERVICE = "CustomResponsesMongoDBService"


class OPERATION:
    ADD = 'Add'
    UPDATE = "Update"
    DELETE = "Delete"


class ExtraParameters:
    MATCHING_RATE = 'MatchingRate'
    LASTCALLTIME = "LastCallTime"


class VariablesInMockDatum:
    FROM_REQUEST_PREFIX = "${FromRequest"
    RANDOM_PREFIX = "${Random"
    HASH_PREFIX = "${Hash"
    Remove = "${Remove}"
    Time = "${Now}"


class HashType:
    MD5 = "md5"
    SHA256 = "sha256"


class CaseType:
    UPPER = "upper"
    LOWER = "lower"



