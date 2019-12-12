from Projects.wechat_DD.constant import ScsPayResNotifyReqParameters, ScsPayResNotifyOptParameters, FalPayResNotifyReqParameters

key = "Hccopsrepaymentchannel2019082700"

fail_default_data = {
    FalPayResNotifyReqParameters.return_code: "SUCCESS",
    FalPayResNotifyReqParameters.result_code: "SUCCESS",
    FalPayResNotifyReqParameters.nonce_str: "${Random_letter+digits_32}",
}

success_pay_notify_reuse_parameters = [ScsPayResNotifyReqParameters.appid,
                                       ScsPayResNotifyOptParameters.attach,
                                       ScsPayResNotifyReqParameters.contract_id,
                                       ScsPayResNotifyReqParameters.mch_id,
                                       ScsPayResNotifyReqParameters.out_trade_no,
                                       ScsPayResNotifyReqParameters.total_fee]

fail_pay_notify_reuse_parameters = [FalPayResNotifyReqParameters.appid,
                                    FalPayResNotifyReqParameters.contract_id,
                                    FalPayResNotifyReqParameters.mch_id,
                                    FalPayResNotifyReqParameters.out_trade_no]

# Callback default values
# current_time=time.strftime('%Y%m%d%H%M%S', time.localtime())
success_pay_notify_default_data = {
    ScsPayResNotifyReqParameters.bank_type: "CFT",
    # pay_result_message_parameter.cash_fee_type: "CNY",
    # pay_result_message_parameter.fee_type: "CNY",
    # pay_result_message_parameter.is_subscribe: "Y",
    ScsPayResNotifyReqParameters.openid: "${Random_letter+digits_18}",
    ScsPayResNotifyReqParameters.transaction_id: "${Random_digits_32}",
    ScsPayResNotifyReqParameters.nonce_str: "${Random_letter+digits_32}",
    ScsPayResNotifyReqParameters.result_code: "SUCCESS",
    ScsPayResNotifyReqParameters.return_code: "SUCCESS",
    # pay_result_message_parameter.return_msg: "OK",
    ScsPayResNotifyReqParameters.trade_state: "SUCCESS",
    # pay_result_message_parameter.err_code: "TRADE_ERROR",
    # pay_result_message_parameter.err_code_des: "暂无可用的支付方式,请绑定其它银行卡完成支付",
    ScsPayResNotifyReqParameters.time_end: "${Now}"
}

dt_status = False