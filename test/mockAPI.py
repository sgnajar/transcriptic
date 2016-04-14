from builtins import object
from collections import deque

"""Keys in mockDB correspond to (method, route) calls"""
mockDB = dict()


class MockResponse(object):
    """Mocks requests.Response"""

    def __init__(self, status_code=None, json=None, text=None):
        self.status_code = status_code
        self.json_data = json
        self.text_data = text

    def status_code(self):
        return self.status_code

    def json(self):
        return self.json_data

    def text(self):
        return self.text_data


def _req_call(method, route, **kwargs):
    key = (method, route)
    if key in mockDB:
        if len(mockDB[key]['call_queue']) == 0:
            if mockDB[key]['default']:
                return mockDB[key]['default']
            else:
                raise RuntimeError("Method: {method}, Route: {route} has run out of max calls.")
        else:
            return mockDB[key]['call_queue'].popleft()
    else:
        raise RuntimeError("Method: {method} and Route: {route} needs to be mocked.".format(**locals()))


def mockRoute(method, route, response, max_calls=None):
    if not isinstance(response, MockResponse):
        raise TypeError("Response needs to be a MockResponse object.")
    key = (method, route)
    if key not in mockDB:
        mockDB[key] = {}
        mockDB[key]['default'] = None
        mockDB[key]['call_queue'] = deque()
    if max_calls:
        mockDB[key]['call_queue'].extend([response] * max_calls)
    else:
        mockDB[key]['default'] = response