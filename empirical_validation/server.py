from flask import Flask, request
from ontology_env import OntologyEnvironment
from python_env import PythonEnvironment
from questionnary1 import QuestionnaryModule1
from utils import dispatch_method, validate_object_data

app = Flask(__name__)

DEFAULT_METHOD = 'ontology'
DEBUG_MODE = False
RESULT_MODE =  'content' # 'time' or 'content'

smart_environment = PythonEnvironment()
ontology_environment = OntologyEnvironment()
questionnary1 = QuestionnaryModule1(RESULT_MODE)

@app.route('/questions')
def list_questions():
    queries = [
                questionnary1.cat1_qa,
                questionnary1.cat1_qb, 
                questionnary1.cat1_qc
            ]

    results = {
        questionnary1.module_name: {
            f"cat1_q{chr(97 + i)}": query() for i, query in enumerate(queries)
        }
    }
    return results, 200

@app.route('/sensors')
def list_sensors():
    method = request.args.get('method', DEFAULT_METHOD)
    return dispatch_method(
        method,
        lambda: ontology_environment.get_sensors(),
        lambda: smart_environment.get_sensors_names()
    )

@app.route('/sensors', methods=['POST'])
def add_sensor():
    if DEBUG_MODE:
        print("Adding sensor")
    data = request.get_json()
    if DEBUG_MODE:
        print(data)
    if not isinstance(data, dict) or "sensors" not in data:
        return {"error": "Invalid request format. Expected {'sensors': [...]}"}, 400

    sensors = data["sensors"]
    responses = []
    
    for sensor_data in sensors:
        error_response, status_code = validate_object_data(sensor_data, 'sensor_name', 'measure', 'data_format', 'device_name', 'device_type', 'room')
        
        if status_code != 200:
            responses.append({"sensor": sensor_data.get("sensor_name", "unknown"), "error": error_response})
            continue  # Skip this sensor if validation fails

        method = sensor_data.get('method', DEFAULT_METHOD)
        response = dispatch_method(
            method,
            lambda: ontology_environment.add_sensor(sensor_data),
            lambda: smart_environment.add_sensor(sensor_data)
        )
        
        responses.append({"sensor": sensor_data["sensor_name"], "response": response})

    return {"results": responses}, 200

@app.route('/get_ontology')
def get_ontology():
    ontology_environment.get_serialized_graph(),
    return "Ontology instance downloaded"

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