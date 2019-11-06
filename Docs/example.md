# Mock Server API Document

### Portal: Mongo-express is used as a front end for input data
- Address: http://qa-gov.cn.lab/mongo/mock

### Parameters
|  Name |Parametes | Type | Comment  |  Example  | Mandatory  | Default  |
| ------------ | ------------ | ------------ | ------------ | ------------ | ------------ | ------------ |
| request  | url  | string  | url of requests  | getcontracts  | Yes  |   |
|   |  method | string/array  | http method  | GET or [GET,POST]  | No  | GET  |
| |queryParameters|json/jsonString|query parameters of requests, support regular expression|{"personId":".*"}|No||
| |bodyPatterns|json/jsonString|query parameters of requests, support regular expression|{"personId":".*"}|No||
|response|headers|json/jsonString|headers of responses|{ "Content-Type": "application/xml"}|No| default headers|
| |code|int|http status|200|No|200|
| |body|json/string|response body|"Hello"|No|""|
|extra|status|string|disable the data|"FALSE",  False, "Duplicated"|No||
| |Comments|string|comments of the data||No||
| |Delay|int|delay the response (second)|10|No||
| |Permanent|boolean|keep the response for custom response|True|No|False
| |Step|int|the number of steps|3|No||
| |Times|int|the times of the response|5|No||
| |ENCRYPT|string| | MD5| | |


### Example
##### Base Example

    {
        "request": {
            "url": "string",
            "method": "GET"
        },
        "response": {
            "body": "string"
        }
    }

#### XML Example
    {
        "request": {
            "url": "xml",
            "method": "GET"
        },
        "response": {
            "headers": {
                "Content-Type": "application/xml"
            },
            "body": "<?xml version=\"1.0 \" encoding=\"ISO - 8859 - 1\"?><note><to>George</to><from>John</from><heading>Reminder</heading><body>Don't forget the meeting!</body></note>"
        }
    }

