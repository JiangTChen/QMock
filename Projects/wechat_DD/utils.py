import hashlib
import hmac
import time

import xmltodict
import json

import Projects.wechat_DD.constant
import utils.utils as utils
import requests
from Object.mock_datum import MockDatum
from Projects.wechat_DD.pay_result_notify import SuccessPayResultNotify, FailPayResultNotify
from constant import Variables
import Projects.wechat_DD.config as wechat_dd_config
import copy
from Projects.wechat_DD.constant import ScsPayResNotifyReqParameters as ScReqP
from Projects.wechat_DD.constant import PAPPayApplyReqParameters as PAPReqP
from constant import CaseType, HashType
from global_vars import log


def gen_response_xml(mock_datum: MockDatum, req: requests):
    res_dict = {}
    req_dict = xmltodict.parse(req.data)['xml']
    for key, value in mock_datum.response.body.items():
        if value == Variables.FROM_REQUEST:
            res_dict[key] = req_dict[key]
        elif value.startswith(Variables.RANDOM_PREFIX):
            keyword, types, size = value[2:-1].split("_")
            res_dict[key] = utils.gen_random_string(types, size)
        else:
            res_dict[key] = value
    res_dict_sorted_list = sorted(res_dict.items())
    stringA = compose_stringA(res_dict_sorted_list)
    stringSignTemp = compose_stringSignTemp(stringA, wechat_dd_config.key)
    sign = utils.gen_hash_str(stringSignTemp, HashType.MD5, case=CaseType.UPPER)
    res_dict_sorted = dict(res_dict_sorted_list)
    res_dict_sorted[Projects.wechat_DD.constant.sign] = sign
    signed_xml = dict_to_xml(res_dict_sorted)
    return signed_xml


def dict_to_xml(res_dict_sorted, cdata=True, no_cdata=[]):
    if cdata:
        for key, value in res_dict_sorted.items():
            if key not in no_cdata:
                res_dict_sorted[key] = "<![CDATA[" + value + "]]>"
    signed_xml = xmltodict.unparse({"xml": res_dict_sorted})
    signed_xml = signed_xml.replace("&lt;", "<")
    signed_xml = signed_xml.replace("&gt;", ">")
    return signed_xml


def generate_signed_xml(xml_string, tag, keyword, key, cdata=True):
    xml_dict = xmltodict.parse(xml_string)
    xml_content = xml_dict["xml"]
    xml_content.pop(tag)
    xml_sorted_list = sorted(xml_content.items())
    stringA = compose_stringA(xml_sorted_list)
    stringSignTemp = stringA + "&key=" + key
    keyword, types = keyword[2:-1].split("_")
    sign = utils.gen_hash_str(stringSignTemp, types.lower(), key, CaseType.UPPER)
    xml_sorted_list.append((tag, sign))
    xml_sorted_list.sort()
    xml_sorted_dict = dict(xml_sorted_list)
    if cdata:
        for key, value in xml_sorted_dict.items():
            xml_sorted_dict[key] = "<![CDATA[" + value + "]]>"
    signed_xml = xmltodict.unparse({"xml": xml_sorted_dict})
    signed_xml = signed_xml.replace("&lt;", "<")
    signed_xml = signed_xml.replace("&gt;", ">")
    return signed_xml


def compose_stringA(data_dict):
    content = ""
    for datum in data_dict:
        content += datum[0] + "=" + datum[1] + "&"
    stringA = content[0:content.__len__() - 1]
    return stringA


def compose_stringSignTemp(stringA, key):
    return stringA + "&key=" + key


def gen_pay_res_notify_xml(mock_datum: MockDatum, req: requests):
    req_body = xmltodict.parse(req.data)['xml']
    if mock_datum.extra.callback.type == Projects.wechat_DD.constant.CallBackType.SUCCESS:
        message_dict = copy.deepcopy(wechat_dd_config.success_pay_notify_default_data)
        reuse_parameters = wechat_dd_config.success_pay_notify_reuse_parameters
    else:
        message_dict = copy.deepcopy(wechat_dd_config.fail_default_data)
        reuse_parameters = wechat_dd_config.fail_pay_notify_reuse_parameters
    # add parameters from request
    for key, value in req_body.items():
        if key in reuse_parameters:
            message_dict[key] = value
            if key == ScReqP.total_fee:
                message_dict[ScReqP.cash_fee] = value
    # add custom parameters
    cb_body = mock_datum.extra.callback.body
    for key, value in cb_body.items():
        if value == Variables.Remove:
            message_dict.pop(key)
        else:
            message_dict[key] = value
    res_dict = {}
    for key, value in message_dict.items():
        if value.startswith(Variables.RANDOM_PREFIX):
            keyword, types, size = value[2:-1].split("_")
            res = utils.gen_random_string(types, size)
            res_dict[key] = res
        elif value == Variables.Remove:
            pass
        elif value == Variables.Time:
            res_dict[key] = time.strftime('%Y%m%d%H%M%S', time.localtime())
        else:
            res_dict[key] = value
    sorted_res_list = sorted(res_dict.items())
    stringA = compose_stringA(sorted_res_list)
    stringSignTemp = compose_stringSignTemp(stringA, wechat_dd_config.key)
    sign = utils.gen_hash_str(stringSignTemp, HashType.MD5)
    sorted_res_dict = dict(sorted_res_list)
    sorted_res_dict[ScReqP.sign] = sign
    res_xml = dict_to_xml(sorted_res_dict, no_cdata=[ScReqP.total_fee])
    return res_xml


def send_pay_res_notify(mock_datum: MockDatum, req: requests):
    body = gen_pay_res_notify_xml(mock_datum, req)
    method = mock_datum.extra.callback.method
    if mock_datum.extra.callback.url == Variables.FROM_REQUEST:
        url = xmltodict.parse(req.data)['xml'][PAPReqP.notify_url]
    else:
        url = mock_datum.extra.callback.url
    delay = int(mock_datum.extra.callback.delay)
    for i in range(delay):
        info = "sleep:" + str(i) + "/" + str(delay)
        log.debug(info)
        time.sleep(1)
    # time.sleep(int(mock_datum.extra.callback.delay))
    res = requests.request(method, url, headers=mock_datum.extra.callback.headers, data=body)
    log.info("<--------CallBack:" + res.url)
    log.info("-------->CallBack response:" + res.content.decode())


xm = """<?xml version="1.0" encoding="UTF-8"?>
<xml>
    <err_code>
        <![CDATA[INVALID_REQUEST]]>
    </err_code>
    <err_code_des>
        <![CDATA[201 商户订单号重复]]>
    </err_code_des>
    <mch_id>
        <![CDATA[1552478241]]>
    </mch_id>
    <nonce_str>
        <![CDATA[q0VkxW2gkP5a7hnm]]>
    </nonce_str>
    <result_code>
        <![CDATA[FAIL]]>
    </result_code>
    <return_code>
        <![CDATA[SUCCESS]]>
    </return_code>
    <return_msg>
        <![CDATA[OK]]>
    </return_msg>
    <sign>
        <![CDATA[5D0CB267C3C277760B134907E226911E]]>
    </sign>
    <appid>
        <![CDATA[wx1ab03d138685d78d]]>
    </appid>
</xml>"""

if __name__ == '__main__':
    signed_xml = generate_signed_xml(xm, "123")
    print(signed_xml)

# xmo = xmltodict.parse(xm)
# xmo_content = xmo["xml"]
# xmo_sorted = sorted(xmo["xml"].items())
# xmd = json.loads(json.dumps(xmo))
# content_list = sorted(xmd["xml"].items())
# xmd["xml"] = dict(sorted(content_list))
# print(xmd)
# content = ""
# for con in content_list:
#     content += con[0] + "=" + con[1] + "&"
# stringA = content[0:content.__len__() - 1]
# print(stringA)
# key = "192006250b4c09247ec02edce69f6a2d"
# stringSignTemp = stringA + "&key=" + key
# sign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()
# print(sign)
# sign_md5 = hmac.new(key.encode('utf-8'), stringSignTemp.encode('utf-8')).hexdigest().upper()
# print(sign_md5)
# sign_256 = hmac.new(key.encode('utf-8'), stringSignTemp.encode('utf-8'), "sha256").hexdigest().upper()
# print(sign_256)
