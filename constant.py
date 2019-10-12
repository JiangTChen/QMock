from enum import Enum

HistoryTable = "-history-"


# column name for data
class DataParameter:
    RULE = "rule"
    METHODS = "methods"
    QUERY_PARAMETERS = "queryParameters"
    BODY_PATTERNS = "bodyPatterns"
    HEADERS = "headers"
    CODE = "code"
    VALUE = "value"


# column name for extra
class DataExtraParameter:
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
UnavailableStatus = ['FALSE', False, 'Duplicated']


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


class ResponseExtraParameter:
    MATCHING_RATE = 'MatchingRate'
