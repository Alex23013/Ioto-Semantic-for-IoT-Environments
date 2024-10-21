# Constants
METHOD_ONTOLOGY = 'ontology'
METHOD_WEB = 'web'
ERROR_METHOD_NOT_RECOGNIZED = 'Method not recognized'
ERROR_SENSOR_NOT_PROVIDED = 'Sensor not provided'
ERROR_INVALID_DATA = 'Invalid data'

def dispatch_method(method, ontology_func, web_func):
    if method == METHOD_ONTOLOGY:
        return ontology_func()
    elif method == METHOD_WEB:
        return web_func()
    else:
        return ERROR_METHOD_NOT_RECOGNIZED, 400

def validate_object_data(data, *fields):
    for field in fields:
        if not data.get(field):
            return ERROR_INVALID_DATA, 422
    return None, 200
