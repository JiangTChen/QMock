from Projects.wechat_DD.constant import ScsPayResMsgReqParameters, ScsPayResMsgOptParameters, FalPayResMsgReqParameters

key = "Hccopsrepaymentchannel2019082700"

fail_default_data = {
    FalPayResMsgReqParameters.return_code: "SUCCESS",
    FalPayResMsgReqParameters.result_code: "SUCCESS",
    FalPayResMsgReqParameters.nonce_str: "${Random_letter+digits_32}",
}

success_reuse_parameters = [ScsPayResMsgReqParameters.appid,
                            ScsPayResMsgOptParameters.attach,
                            ScsPayResMsgReqParameters.contract_id,
                            ScsPayResMsgReqParameters.mch_id,
                            ScsPayResMsgReqParameters.out_trade_no,
                            ScsPayResMsgReqParameters.total_fee]

fail_reuse_parameters = [FalPayResMsgReqParameters.appid,
                         FalPayResMsgReqParameters.contract_id,
                         FalPayResMsgReqParameters.mch_id,
                         FalPayResMsgReqParameters.out_trade_no]

# Callback default values
# current_time=time.strftime('%Y%m%d%H%M%S', time.localtime())
success_default_data = {
    ScsPayResMsgReqParameters.bank_type: "CFT",
    # pay_result_message_parameter.cash_fee_type: "CNY",
    # pay_result_message_parameter.fee_type: "CNY",
    # pay_result_message_parameter.is_subscribe: "Y",
    ScsPayResMsgReqParameters.openid: "${Random_letter+digits_18}",
    ScsPayResMsgReqParameters.transaction_id: "${Random_digits_32}",
    ScsPayResMsgReqParameters.nonce_str: "${Random_letter+digits_32}",
    ScsPayResMsgReqParameters.result_code: "SUCCESS",
    ScsPayResMsgReqParameters.return_code: "SUCCESS",
    # pay_result_message_parameter.return_msg: "OK",
    ScsPayResMsgReqParameters.trade_state: "SUCCESS",
    # pay_result_message_parameter.err_code: "TRADE_ERROR",
    # pay_result_message_parameter.err_code_des: "暂无可用的支付方式,请绑定其它银行卡完成支付",
    ScsPayResMsgReqParameters.time_end: "${Now}"
}


