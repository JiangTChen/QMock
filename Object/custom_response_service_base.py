from Object.singleton import Singleton

from Object.mock_response import MockResponse


class CustomResponsesServiceBase:
    __metaclass__ = Singleton

    def __init__(self):
        # print("No implement CustomResponsesServiceBase.__init__")
        pass

    def add(self, response: MockResponse):
        print("No implement CustomResponsesServiceBase.add")

    def remove(self, rule, methods, user=None):
        print("No implement CustomResponsesServiceBase.remove")

    def clean(self):
        print("No implement CustomResponsesServiceBase.clean")

    def get_responses(self, req, user=None):
        print("No implement CustomResponsesServiceBase.get_responses")

    @property
    def json_obj(self):
        print("No implement CustomResponsesServiceBase.json_obj")
        return "No implement"
