import os
from constant import *

debug = False

base_path = os.path.dirname(__file__)
projects = ["UTA", "HCCN", "CAPPBE"]
data_package = 'Data'
large_data_file_name = 'LargeData'

# DB info
database_type = DataBaseType.MONGODB  # Execl, MongoDB
data_service = DataBaseService.MONGODB_SERVICE  # ExeclService,MongoDBService
#Local
#MongoDB_address = "mongodb://mongo:27017/"
#k8s
MongoDB_address = "mongodb://ura-mongo:27017/"
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
