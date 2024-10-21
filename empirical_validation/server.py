from flask import Flask, request
from ontology_env import OntologyEnvironment
from python_env import PythonEnvironment
from utils import dispatch_method, validate_object_data

app = Flask(__name__)

smart_environment = PythonEnvironment()
ontology_environment = OntologyEnvironment()
DEFAULT_METHOD = 'web'

@app.route('/sensors')
def list_sensors():
    method = request.args.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.get_serialized_graph(), #TODO: implement custom method
        lambda: smart_environment.get_sensors_names()
    )

@app.route('/sensors', methods=['POST'])
def add_sensor():
    data = request.get_json()
    error_response, status_code= validate_object_data(data, 'name', 'measure')
    if status_code != 200:
        return error_response
    method = data.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.add_sensor(data),
        lambda: smart_environment.add_sensor(data)
    )

@app.route('/observations')
def get_observations():
    method = request.args.get('method', DEFAULT_METHOD)
    sensor = request.args.get('sensor')
    return dispatch_method(
        method,
        lambda: ontology_environment.get_serialized_graph(), #TODO: implement custom method
        lambda: smart_environment.get_sensor_observation(sensor)
    )

@app.route('/observations', methods=['POST'])
def add_observation():
    data = request.get_json()
    error_response, status_code= validate_object_data(data, 'sensor', 'value')
    if status_code != 200:
        return error_response
    method = data.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.add_observation(data),
        lambda: smart_environment.add_observation(data)
    )

@app.route('/env_current_state', methods=['GET'])
def list_last_observations():
    method = request.args.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.get_serialized_graph(), #TODO: implement custom method
        lambda: smart_environment.get_last_observations()
    )

@app.route('/visitors', methods=['POST'])
def add_visitor():
    data = request.get_json()
    error_response, status_code= validate_object_data(data, 'name', 'role')
    if status_code != 200:
        return error_response
    method = data.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.add_visitor(data), #TODO: implement custom method
        lambda: smart_environment.add_visitor(data)
    )

@app.route('/count_visitors', methods=['GET'])
def count_visitors():
    method = request.args.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.get_serialized_graph(), #TODO: implement custom method
        lambda: smart_environment.count_visitors()
    )

@app.route('/list_visitors', methods=['GET'])
def list_visitors():
    method = request.args.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.get_serialized_graph(), #TODO: implement custom method
        lambda: smart_environment.list_visitors()
    )


@app.route("/")
def welcome_message():
    return "Hello, from smart building!"

# create a method that initiate the building instance (set ethic mode and info about data controllers)


if __name__ == '__main__':
    app.run(port=5000)