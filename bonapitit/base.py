import requests


class Error:
    def __init__(self, data):
        self.content = data


class Warning:
    def __init__(self, data):
        self.content = data


class BaseResponse:
    def __init__(self, data):
        self.content = data
        self.error = None
        self.warning = None
        self.details = None
        if 'errorMessage' in data:
            self.error: Error = Error(data['errorMessage'])
        if 'warnings' in data:
            self.warning: Warning = Warning(data['warnings'])


class BaseClient:
    def __init__(self, dev_name, cert_name):
        self._headers = {
            'X-BONANZLE-API-DEV-NAME': dev_name,
            'X-BONANZLE-API-CERT-NAME': cert_name,
        }

    def _request(self, path, json=None, headers=None):
        endpoint = 'https://api.bonanza.com/api_requests/'
        url = endpoint + path
        if headers:
            return requests.post(url=url, json=json, headers=headers)
        return requests.post(url=url, json=json, headers=self._headers)




