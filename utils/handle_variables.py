from utils import global_utils
import time, json, xmltodict
from utils.global_utils import get_request_contents, is_json_str


def fromrequest(args: list, **kwargs):
    if args.__len__() > 0:
        keyword = args[0]
    else:
        keyword = kwargs.get("key")
    req = kwargs.get("req")
    contents = get_request_contents(req)
    if contents.get("json"):
        contents = contents.get("json")
    else:
        contents = contents.get("data")
    if isinstance(contents, dict):
        return contents[keyword]
    elif is_json_str(contents):
        return json.loads(contents)[keyword]
    elif isinstance(contents, str) and contents.startswith("<?xml"):
        return xmltodict.parse(contents)["xml"][keyword]
    else:
        return ""


def random(args: list, **kwargs):
    if args.__len__() > 1:
        types = args[0]
        size = args[1]
        return global_utils.gen_random_string(types, size)
    else:
        return global_utils.gen_random_string()


def now(args: list, **kwargs):
    if args.__len__() > 1:
        time_format = args[0]
    else:
        time_format = '%Y%m%d%H%M%S'
    return time.strftime(time_format, time.localtime())

# def
#     FROM_REQUEST = "${from_request}"
#     RANDOM_PREFIX = "${Random"
#     HASH_PREFIX = "${hash"
#     Remove = "${Remove}"
#     Time = "${Now}"


# def func(arg, *args, **kwargs):
#     print(arg, args, kwargs)
#
#
# func(1, [2, 3, 4, 5, 6, 7], name='xiaoming', age=18)
