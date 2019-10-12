from flask import Flask, request, redirect

import json
import utils.utils as utils
from Object.mock_response import MockResponse
from global_vars import log
import config
import utils.data_handler as data_handle
from flasgger import Swagger
from http import HTTPStatus
from constant import *
from Object.custom_responses_mongoDB_service import CustomResponsesMongoDBService
from Object.mongoDB_service import MongoDBService
from datetime import datetime
from Object.steps_pool import StepsPool

app = Flask(__name__)
IP = utils.get_host_ip()

swagger = Swagger(app, template_file='API_Docs/template.json')

# swagger = Swagger(app)

database_address = eval("config." + config.database_type + "_address")
steps_pool = StepsPool()
custom_response_service = eval(config.cache_data_service + '()')
IP = utils.get_host_ip()


@app.route('/')
def hello_world():
    # return 'Welcome to Mock Server'
    return redirect('/apidocs/')


@app.route('/<project_name>/<module_name>/<path:api_rule>', methods=['POST', 'GET', 'PUT', 'DELETE'])
def db_access(project_name, module_name, api_rule):
    database_name = project_name
    table_name = module_name
    if utils.is_static_file(api_rule):
        return app.send_static_file(project_name + "/" + module_name + "/" + api_rule)
    else:
        db = eval(
            config.data_service + "('" + database_address + "','" + database_name + "')")
        responses = steps_pool.get_responses(request, table_name)
        if not responses:
            responses = custom_response_service.get_responses(request)
            if not responses:
                responses = data_handle.get_responses_for_request(db, table_name, request)
            parameters = utils.get_request_contents(request)
            print(api_rule + ":", parameters)
            while responses.__len__() < 1:
                info = str(
                    responses.__len__()) + " Response here, please check database:" + database_name + " table:" + table_name + " rule:" + api_rule + '\n' + request.method + ':' + request.url + '\n' + 'Body:' + parameters
                log.info(info)
                # Retry
                if config.debug:
                    # return info, HTTPStatus.NOT_FOUND
                    responses = data_handle.get_responses_for_request(db, table_name, request)
                else:
                    return info, HTTPStatus.NOT_FOUND
            if responses.__len__() > 1:
                info = str(
                    responses.__len__()) + " Response here, please check database:" + database_name + " table:" + table_name + " rule:" + api_rule + '\n' + request.method + ':' + request.url + '\n' + 'Body:' + parameters
                log.info(info)
                print("---------------------", responses)
                for response in responses:
                    if DataExtraParameter.STEP in response:
                        steps_pool.append(response)
        step_responses = []
        for response in responses:
            if response.get(DataExtraParameter.STEP):
                step_responses.append(response)
        if step_responses.__len__() > 0:
            responses = sorted(step_responses, key=lambda keys: keys[DataExtraParameter.STEP], reverse=True)
            response = responses.pop()
            steps_pool.set_last_call_time(response)
            # steps_pool.remove(response)
        else:
            response = responses[0]
        headers = utils.merge_headers(response)
        code = int("200" if response.get(DataParameter.CODE) == "" else response.get(DataParameter.CODE))
        value = response.get(DataParameter.VALUE)
        value = utils.replace_large_data(config.large_data_file_name, value)
        body = utils.format_body_to_string(headers, value)
        print(api_rule + ': Response Body:', body)
        utils.delay_for_response(response)
        return body, code, headers


@app.route("/cache", methods=[HTTPMethod.POST, HTTPMethod.DELETE])
def cache():
    """
    file: API_Docs/cache.yaml
    """
    code = 200
    if request.method == HTTPMethod.DELETE:
        req = request.form.to_dict()
        rule = req.get(DataParameter.RULE)
        methods = req.get(DataParameter.METHODS).split(",")
        user = req.get(DataExtraParameter.USER)
        count = custom_response_service.remove(rule, methods, user)
        info = "Deleted:" + str(count) + " rule:" + rule
        if count == 0:
            code = 400
    else:
        custom_response = MockResponse(request.json)
        custom_response_service.add(custom_response)
        info = "Added:" + custom_response.rule
    return info, code


@app.route("/caches", methods=[HTTPMethod.GET, HTTPMethod.DELETE])
def caches():
    """
    file: API_Docs/caches.yaml
    """
    if request.method == HTTPMethod.GET:
        return json.dumps(custom_response_service.json_obj), HTTPStatus.OK, config.default_header_dict
    else:
        custom_response_service.clean()
        return "Dropped all custom responses", HTTPStatus.OK


# app.run(host=IP, port=80, debug=config.debug)

app.run(host='0.0.0.0', port=8080, debug=config.debug)
