# Mock Server

### Functions:

1. Return the responses according to the http requests.
2. Support custom response for API automation testing.
3. Support replay the different response for same url.


* * *

### Portal: Mongo-express is used as a front end for input data
- Address: [http://qa-gov.cn.lab/mongo/mock](http://qa-gov.cn.lab/mongo/mock)

* * *

### Mock Server Address:
- Address: http://qa-gov.cn.lab/mock


* * *

### Parameters
|  Name |Parameters | Type | Comment  |  Example  | Mandatory  | Default  |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| request  | url  | string  | url of requests  | getcontracts  | Yes  |   |
|   |  method | string/array  | http method  | GET or [GET,POST]  | No  | GET  |
| |queryParameters|json/jsonString|query parameters of requests, support regular expression|{"personId":".*"}|No||
| |bodyPatterns|json/jsonString|query parameters of requests, support regular expression|{"personId":".*"}|No||
|response|headers|json/jsonString|headers of responses|{ "Content-Type": "application/xml"}|No| {"Content-Type": "application/json;charset=UTF-8"}|
| |code|int|http status|200|No|200|
| |body|json/string|response body|"Hello"|No|""|
|Extra|Disable|boolean|disable the data|True|No|False|
| |Comments|string|comments of the data||No||
| |Delay|int|delay the response (second)|10|No||
| |Permanent|boolean|keep the response for custom response|True|No|False
| |Step|int|the number of steps|3|No||
| |Times|int|the times of the response|5|No||
| |CallBack|string| The request for async|{"url": "http://qa-gov.cn.lab/mock/","method": "POST","headers": {"Content-Type": "application/json"},"body": {"key": "value"},"Delay": 5} | No | |


* * *

### Example
##### Base Example

1. Open Portal add Create Database.The project name is recommended, ex:example
2. Create collection in the Database. The module name is recommended, ex:wechat-dd
3. Add new Document as below:
4. Access http://qa-gov.cn.lab/mock/example/wechat-dd/string
5. Receive response: {"body":"string"}

```
{
    "request": {
        "url": "string",
        "method": "GET"
    },
    "response": {
        "body": "string"
    }
}
```

##### Full Example
```
{
    "request": {
        "url": "proxy",
        "method": "POST"
        "queryParameters":{"personId":".*"},
        "bodyPatterns":{"personId":".*"}
    },
    "response": {
        "headers": {
            "Content-Type": "application/xml"
        },
        "code": 200,
        "body": {
            "appid": "${FromRequest}",
            "mch_id": "${FromRequest}",
            "nonce_str": "${Random(letter+digits,16)}",
            "result_code": "SUCCESS",
            "return_code": "SUCCESS",
            "return_msg": "OK"
        }
    },
    "Extra": {
        "CallBack": {
            "url": "${FromRequest}",
            "method": "POST",
            "headers": {
                "Content-Type": "application/xml"
            },
            "body": {"key":"value"},
            "Delay": 5
        }
        "Disable":False,
        "Delay":3,
        "Step":1,
        "Times":3,
        "Permanent":False #custom response only
    }
}
```


* * *

### For Custom Response:

1. Upload custom response:
Url:http://qa-gov.cn.lab/mock/cache
Method:POST
Header:{"Content-Type":"application/json"}
```
{
	"request": {
		"url": "/HCCN/hccn-be/uploadBankCard",
		"method": "GET",
		"queryParameters": "",
		"bodyPatterns": ""
	},
	"response": {
		"headers": "",
		"status": 200,
		"body": {
			"id": 1234,
			"name": "HomeCredit"
		}
	},
	"Extra": {
		"Delay": 10,
		"Permanent": false
	}
}
```

2. Get all custom responses:
Url:http://qa-gov.cn.lab/mock/caches
Method:GET

3. Delete custom response:
Url:http://qa-gov.cn.lab/mock/cache
Method:DELETE
Header:{"Content-Type":"application/x-www-form-urlencoded"}
BODY:{"url":"/HCCN/hccn-be/uploadBankCard","method":"GET"}

4. Drop all custom responses:
Url:http://qa-gov.cn.lab/mock/caches
Method:DELETE

### Variables:

* ${FromRequest} 
    * Get the value from request and the key is equal the response's
* ${FromRequest("key")}
    * Get the value from request with the specified key.
* ${Random(type,size)}
    * Generate a Random according the specified type and size
    * type:letter+digits，letter，digits
* ${Now}
    * Return current time.(Ex:20191211060708)


* * *
# Custom Projects
* Wechat-DD

