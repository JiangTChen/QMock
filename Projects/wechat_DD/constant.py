# required parameter for SUCCESS
class ScsPayResMsgReqParameters:
    return_code = "return_code"
    appid = "appid"
    contract_id = "contract_id"
    mch_id = "mch_id"
    out_trade_no = "out_trade_no"
    total_fee = "total_fee"
    cash_fee = "cash_fee"
    bank_type = "bank_type"
    openid = "openid"
    transaction_id = "transaction_id"
    nonce_str = "nonce_str"
    result_code = "result_code"
    trade_state = "trade_state"
    time_end = "time_end"
    sign = "sign"


class ScsPayResMsgOptParameters:
    return_msg = "return_msg"
    device_info = "device_info"
    err_code = "err_code"
    err_code_des = "err_code_des"
    is_subscribe = "is_subscribe"
    fee_type = "fee_type"
    cash_fee_type = "cash_fee_type"
    coupon_fee = "coupon_fee"
    coupon_count = "coupon_count"
    attach = "attach"

# required parameter for Fail
class FalPayResMsgReqParameters:
    return_code = "return_code"
    appid = "appid"
    mch_id = "mch_id"
    nonce_str = "nonce_str"
    sign = "sign"
    result_code = "result_code"
    out_trade_no = "out_trade_no"
    contract_id = "contract_id"


class FalPayResMsgOptParameters:
    err_code = "err_code"
    err_code_des = "err_code_des"


class PAPPayApplyReqParameters:
    appid = "appid"
    mch_id = "mch_id"
    nonce_str = "nonce_str"
    sign = "sign"
    body="body"
    out_trade_no="out_trade_no"
    total_fee="total_fee"
    spbill_create_ip="spbill_create_ip"
    notify_url="notify_url"
    trade_type="trade_type"
    contract_id="contract_id"
    receipt="receipt"


class PAPPayApplyOptParameters:
    detail="detail"
    attach="attach"
    fee_type="fee_type"
    goods_tag="goods_tag"


class PAPPayApplyResReqParameters:
    return_code="return_code"
    return_msg="return_msg"
    appid = "appid"
    mch_id = "mch_id"
    nonce_str = "nonce_str"
    sign = "sign"
    result_code="result_code"


class PAPPayApplyResOptParameters:
    err_code="err_code"
    err_code_des="err_code_des"


class CallBackType:
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"


sign = "sign"

