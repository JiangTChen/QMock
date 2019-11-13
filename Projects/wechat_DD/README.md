## Wechat-DD
### Information:
Ref Document:[https://pay.weixin.qq.com/wiki/doc/api/pap.php?chapter=18_3&index=8](https://pay.weixin.qq.com/wiki/doc/api/pap.php?chapter=18_3&index=8)
DB Name: wechat-DD
Url: http://qa-gov.cn.lab/mock/wechat-DD/{module_name}/{url}

### Example:
```
{
    "request": {
        "url": "proxy",
        "method": "POST"
    },
    "response": {
        "headers": {
            "Content-Type": "application/xml"
        },
        "body": {
            "appid": "${FromRequest}",
            "mch_id": "${FromRequest}",
            "nonce_str": "${Random(letter+digits,16)}",
            "result_code": "SUCCESS",
            "return_code": "SUCCESS",
            "return_msg": "OK"
        } # It will be converted to XML, and the sign of the content is automatically inserted
    },
    "Extra": {
        "CallBack": {
            "url": "${FromRequest}", # get notify_url from request
            "method": "POST",
            "headers": {
                "Content-Type": "application/xml"
            },
            "body": {},
            "Type": "SUCCESS", # The callback for pappayapply. The value should be SUCCESS or FAIL
            "Delay": 5
        } # The CallBack is customed for wechat-dd
    }
}
```