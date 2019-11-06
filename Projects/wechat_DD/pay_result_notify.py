from Projects.wechat_DD.constant import ScsPayResNotifyReqParameters as ReqParms, ScsPayResNotifyOptParameters as OptParms


class PayResultNotifyBase:
    def __init__(self, json_obj: dict):
        self.return_code = json_obj.get(ReqParms.return_code)
        # self.return_msg = json_obj.get(parms.return_msg)


class SuccessPayResultNotify(PayResultNotifyBase):
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.appid = json_obj.get(ReqParms.appid)
        self.mch_id = json_obj.get(ReqParms.mch_id)
        self.nonce_str = json_obj.get(ReqParms.nonce_str)
        self.result_code = json_obj.get(ReqParms.result_code)
        self.openid = json_obj.get(ReqParms.openid)
        self.bank_type = json_obj.get(ReqParms.bank_type)
        self.total_fee = json_obj.get(ReqParms.total_fee)
        self.cash_fee = json_obj.get(ReqParms.cash_fee)
        self.trade_state = json_obj.get(ReqParms.trade_state)
        self.transaction_id = json_obj.get(ReqParms.transaction_id)
        self.out_trade_no = json_obj.get(ReqParms.out_trade_no)
        self.time_end = json_obj.get(ReqParms.time_end)
        self.contract_id = json_obj.get(ReqParms.contract_id)
        self.sign = None
        self._json_obj=json_obj


class FailPayResultNotify(PayResultNotifyBase):
    def __init__(self, json_obj):
        super().__init__(json_obj)
        self.appid = json_obj.get(ReqParms.appid)
        self.mch_id = json_obj.get(ReqParms.mch_id)
        self.nonce_str = json_obj.get(ReqParms.nonce_str)
        self.result_code = json_obj.get(ReqParms.result_code)
        self.out_trade_no = json_obj.get(ReqParms.out_trade_no)
        self.contract_id = json_obj.get(ReqParms.contract_id)
        self.sign = None
