import os
from constant import *

debug = False
MongoDB_Server = os.environ.get("MOCK_CONFIG_MONGODB_SERVER") if os.environ.get(
    "MOCK_CONFIG_MONGODB_SERVER") else "127.0.0.1"
MongoDB_Port = os.environ.get("MOCK_CONFIG_MONGODB_PORT") if os.environ.get("MOCK_CONFIG_MONGODB_PORT") else "27017"
site_base_url = os.environ.get("MOCK_CONFIG_SITE_BASEURL") if os.environ.get("MOCK_CONFIG_SITE_BASEURL") else ""
cache_step_time = os.environ.get("MOCK_CONFIG_CACHE_STEP_TIME") if os.environ.get("MOCK_CONFIG_CACHE_STEP_TIME") else 0
log_level = os.environ.get("MOCK_CONFIG_LOG_LEVEL") if os.environ.get("MOCK_CONFIG_LOG_LEVEL") else "INFO"

base_path = os.path.dirname(__file__)
projects = ["UTA", "HCCN", "CAPPBE"]
data_package = 'Data'
large_data_file_name = 'LargeData'

# DB info
database_type = DataBaseType.MONGODB  # Execl, MongoDB
data_service = DataBaseService.MONGODB_SERVICE  # ExeclService,MongoDBService
MongoDB_address = "mongodb://" + MongoDB_Server + ":" + MongoDB_Port + "/"
Execl_address = base_path + "/Data/"

# cache info
cache_data_service = CacheDataService.MONGODB_SERVICE  # Local,MongoDB
cache_database_name = "custom_response"
cache_table_name = "cache"
# data_path = base_path + "/Data/"

static_files_format_list = ['.html', '.css', '.js', 'ttf', 'jpg']
default_header_dict = {
    "Cache-Control": "no-cache, no-store, max-age=0, must-revalidate",
    "Content-Type": "application/json;charset=UTF-8"
}


class Projects:
    wechat_DD = "wechat-DD"
