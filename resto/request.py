

class RequestProxyLoader:
    def __init__(self):
        self.request = None

    def set_request(self, request_proxy):
        self.request = request_proxy
        return self.request


RequestProxy: RequestProxyLoader = RequestProxyLoader()