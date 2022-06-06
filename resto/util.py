from logging import Logger
log = Logger(__name__)

class BaseUtil:
    def error(*args):
        log.error(args)
        
    def listify(data) -> list:
        if type(data) == list:
            return data

        return [data]
    
class RESTError(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        super().__init__()
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv