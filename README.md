# Mock Server

## Functions

1. Return the responses according to the http requests.
2. Support custom response for API automation testing.
3. Support replay the different response for same url.
4. Support asyn callback
5. Support variables: FromRequest, Random, Now
6. Support access Database
7. Support json to xml body



## Start Mock Server

```shell
docker-compose up
```



## Portal: Mongo-express is used as a front end for input data

- Address: http://localhost:8081



## Mock Server Address

- Address: http://localhost:8080



## Parameters

| Name     | Parameters      | Type            | Comment                                                  | Example                                                      | Mandatory | Default                                            |
| :------- | :-------------- | :-------------- | :------------------------------------------------------- | :----------------------------------------------------------- | :-------- | :------------------------------------------------- |
| request  | url             | string          | url of requests                                          | getcontracts                                                 | Yes       |                                                    |
|          | method          | string/array    | http method                                              | GET or [GET,POST]                                            | No        | GET                                                |
|          | queryParameters | json/jsonString | query parameters of requests, support regular expression | {"personId":".*"}                                            | No        |                                                    |
|          | bodyPatterns    | json/jsonString | query parameters of requests, support regular expression | {"personId":".*"}                                            | No        |                                                    |
| response | headers         | json/jsonString | headers of responses                                     | { "Content-Type": "application/xml"}{} # empty header        | No        | {"Content-Type": "application/json;charset=UTF-8"} |
|          | code            | int             | http status                                              | 200                                                          | No        | 200                                                |
|          | body            | json/string     | response body                                            | "Hello"                                                      | No        | ""                                                 |
| Extra    | Disable         | boolean         | disable the data                                         | True                                                         | No        | False                                              |
|          | Comments        | string          | comments of the data                                     |                                                              | No        |                                                    |
|          | Delay           | int             | delay the response (second)                              | 10                                                           | No        |                                                    |
|          | Permanent       | boolean         | keep the response for custom response                    | True                                                         | No        | False                                              |
|          | Step            | int             | the number of steps                                      | 3                                                            | No        |                                                    |
|          | Times           | int             | the times of the response                                | 5                                                            | No        |                                                    |
|          | CallBack        | string          | The request for async                                    | {"url": "http://qa-gov.cn.lab/mock/","method": "POST","headers": {"Content-Type": "application/json"},"body": {"key": "value"},"Delay": 5} | No        |                                                    |



## Example

- #### Base Example


1. Open Portal add Create Database.The project name is recommended, ex:example
2. Create collection in the Database. The module name is recommended, ex:wechat-dd
3. Add new Document as below:
4. Access http://qa-gov.cn.lab/mock/example/wechat-dd/string
5. Receive response: {"body":"string"}

```json
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



- #### Advanced Example

```json
{
    "request": {
        "url": "proxy",
        "method": "POST",
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
        },
        "Disable": false,
        "Delay":3,
        "Step":1,
        "Times":3,
        "Permanent": false 
    }
}
```
"Permanent": false  #custom response only




- #### For Custom Response:

1. Upload custom response:
   Url:http://localhost:8080/cache
   Method:POST
   Header:{"Content-Type":"application/json"}


   ```json
{
	"request": {
		"url": "/prject/uploadBankCard",
		"method": "GET",
		"queryParameters": "",
		"bodyPatterns": ""
	},
	"response": {
		"headers": "",
		"status": 200,
		"body": {
			"id": 1234,
			"name": "projectName"
		}
	},
	"Extra": {
		"Delay": 10,
		"Permanent": false
	}
}
   ```

   

2. Get all custom responses:
   Url:http://localhost:8080/caches
   Method:GET

3. Delete custom response:
   Url:http://localhost:8080/cache
   Method:DELETE
   Header:{"Content-Type":"application/x-www-form-urlencoded"}
   BODY:{"url":"/HCCN/hccn-be/uploadBankCard","method":"GET"}

4. Drop all custom responses:
   Url:http://localhost:8080/caches
   Method:DELETE





## Variables in Response

- ${FromRequest}
  - Get the value from request and the key is equal the response's
- ${FromRequest("key")}
  - Get the value from request with the specified key.
- ${Random(type,size)}
  - Generate a Random according the specified type and size
  - type: letter+digits，letter，digits
- ${Now}
  - Return current time.(Ex:20191211060708)
- ${Now(format)}
  - Return current time for the specified format. (Ex:${Now('%Y%m%d%H%M%S')})
- ${Remove}
  - The item of the dict will be remove
- ${DB(db_name,table_name,query,key,number)}
  - optional: query, key, number
  - example:
    - "${DB(wechat-DD,err_code,{\"group\":1},err_code,?)}"
  - number:
    - start from 0
    - ? for random