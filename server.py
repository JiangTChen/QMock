from flask import Flask, request, redirect

import json
from utils import data_handler
from utils import global_utils
# import utils.utils as utils
from global_vars import log
import config
from flasgger import Swagger, swag_from, LazyString, LazyJSONEncoder
from http import HTTPStatus
from constant import *
from datetime import datetime
from Object.steps_pool import StepsPool
from Object.mock_datum import MockDatum
from utils.data_handler import reassemble_response
from Object.custom_responses_mongoDB_service import CustomResponsesMongoDBService
from Object.mongoDB_service import MongoDBService
from concurrent.futures import ThreadPoolExecutor

executor = ThreadPoolExecutor()

app = Flask(__name__)
# IP = utils.get_host_ip()


app.json_encoder = LazyJSONEncoder

template = dict(swaggerUiPrefix=LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')))
# print(LazyString(lambda: request.environ.get('HTTP_X_SCRIPT_NAME', '')))
swagger = Swagger(app, template_file='API_Docs/template.json', template=template)
# swagger = Swagger(app, template_file='API_Docs/template.json')
# swagger = Swagger(app)

database_address = eval("config." + config.database_type + "_address")
steps_pool = StepsPool()
custom_response_service = eval(config.cache_data_service + '()')


@app.route(config.site_base_url + '/', methods=['GET'])
def get():
    # return 'Welcome to Mock Server'
    return redirect(config.site_base_url + '/apidocs/')


@app.route(config.site_base_url + '/', methods=['POST'])
def post():
    request_body = global_utils.get_post_body_content(request)
    # request_body=json.dumps(global_utils.get_request_contents(request))
    log.info("-----> Request Url:" + request.url)
    if isinstance(request_body, dict):
        request_body = json.dumps(global_utils.get_post_body_content(request))
    log.info("-----> Request Body:" + request_body)
    log.info("<----- Response Body:" + request_body)
    return request_body


@app.route(config.site_base_url + '/<project_name>/<module_name>/<path:url>',
           methods=['POST', 'GET', 'PUT', 'DELETE'])
def db_access(project_name, module_name, url):
    log.info('-----> Request Url:' + request.url + ' ')
    database_name = project_name
    table_name = module_name
    if global_utils.is_static_file(url):
        return app.send_static_file(project_name + "/" + module_name + "/" + url)
    else:
        db = eval(
            config.data_service + "('" + database_address + "','" + database_name + "')")
        data = steps_pool.get_data(request, table_name)
        log.debug("steps_pool:" + str(data))
        if not data:  # No steps_pool
            data = custom_response_service.get_data(request)
            log.debug("custom_response:" + str(data))
            if not data:
                data = data_handler.get_data_for_request(db, table_name, request)
                log.debug("DB_MockData:" + str(data))
            parameters = global_utils.get_request_contents(request)
            # print('url:' + url + " para:", parameters)
            while data.__len__() < 1:  # debug for not found
                info = str(
                    data.__len__()) + " Response here, please check database:" + database_name + " table:" + table_name + " rule:" + url + '\n' + request.method + ':' + request.url + '\n' + 'Body:' + json.dumps(
                    parameters)
                log.debug(info)
                # Retry
                if config.debug:
                    # return info, HTTPStatus.NOT_FOUND
                    data = data_handler.get_data_for_request(db, table_name, request)
                else:
                    return info, HTTPStatus.NOT_FOUND
            # if data.__len__() > 1:
            info = str(
                data.__len__()) + " Response here, please check database:" + database_name + " table:" + table_name + " rule:" + url + '\n' + request.method + ':' + request.url + '\n' + 'Body:' + json.dumps(
                parameters)
            log.debug(info)
            # append datum to steps_pool during steps_pool doesn't has matched data
            for mock_datum in data:
                if mock_datum.extra.step:
                    steps_pool.append(mock_datum)

        step_data = []  # filtered datum with step from data(steps_pool,custom_response,data)
        for mock_datum in data:
            if mock_datum.extra.step:
                step_data.append(mock_datum)
        if step_data.__len__() > 0:
            data = sorted(step_data, key=lambda one_mock_datum: one_mock_datum.extra.step, reverse=True)
            mock_datum = data.pop()
            # if steps_pool.pool.__len__()>0:
            index = steps_pool.pool.index(mock_datum)
            if config.cache_step_time > 0:
                steps_pool.pool[index].extra.last_call_time = datetime.now()
            else:
                steps_pool.pool[index].extra.times -= 1
        else:
            mock_datum = data[0]  # No steps datum
        body, headers, status = reassemble_response(mock_datum, request)
        global_utils.delay_for_response(mock_datum)
        log.info('<----- Response Body:' + str(body))
        return body, status, headers


@app.route(config.site_base_url + "/cache", methods=[HTTPMethod.POST, HTTPMethod.DELETE])
@swag_from('API_Docs/cache.yaml')
def cache():
    # """
    # file: API_Docs/cache.yaml
    # """
    code = 200
    if request.method == HTTPMethod.DELETE:
        req = request.form.to_dict()
        url = req.get(MockDataParameterRequest.URL) if req.get(MockDataParameterRequest.URL) else "/"
        method = req.get(MockDataParameterRequest.METHOD) if req.get(MockDataParameterRequest.METHOD) else "GET"
        user = req.get(MockDataExtra.USER) if req.get(MockDataExtra.USER) else None
        # mock_datum = MockDatum(req)
        # url = mock_datum.request.url
        # methods = mock_datum.request.method.split(",")
        # user = mock_datum.extra.user
        count = custom_response_service.remove(url, method, user)
        info = "Deleted:" + str(count) + " rule:" + url
        if count == 0:
            code = 400
    else:
        custom_datum = MockDatum(request.json)
        custom_response_service.add(request.json)
        info = "Added:" + custom_datum.request.url
    return info, code


@app.route(config.site_base_url + "/caches", methods=[HTTPMethod.GET, HTTPMethod.DELETE])
@swag_from('API_Docs/caches.yaml')
def caches():
    # """
    # file: API_Docs/caches.yaml
    # """
    if request.method == HTTPMethod.GET:
        return json.dumps(custom_response_service.json_obj), HTTPStatus.OK, config.default_header_dict
    else:
        custom_response_service.clean()
        return "Dropped all custom responses", HTTPStatus.OK


# app.run(host=IP, port=80, debug=config.debug)

if __name__ == "__main__":
    log.info("------- MongoDB:" + config.MongoDB_address)
    log.info("------- site_base_url:" + config.site_base_url)
    app.run(host='0.0.0.0', port=8080, debug=config.debug, threaded=True, processes=1)
