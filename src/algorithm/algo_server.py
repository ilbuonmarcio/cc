from sanic import Sanic
from sanic.response import json

class Algorithm:

    def __init__(self, process_id, group_id, config_id):
        self.process_id = process_id
        self.group_id = group_id
        self.config_id = config_id

    def run_composition(self):
        for i in range(0, 1000000000):
            yield i

    def get_algo_parameters(self):
        return f"Group id: {self.group_id} - Config id: {self.config_id}"

algorithm_instances = []
algorithm_last_id_available = 0

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/create_algorithm_instance")
async def create_algorithm_instance(request):
    if "group_id" in request.args.keys() and "config_id" in request.args.keys():
        group_id, config_id = request.args["group_id"], request.args["config_id"]
        global algorithm_last_id_available
        algorithm_instances.append(
            Algorithm(algorithm_last_id_available, group_id, config_id)
        )
        response = {"status" : "good", "process_id" : str(algorithm_last_id_available)}
        algorithm_last_id_available += 1
        return json(response)
    else:
        return json({"status" : "bad", "response" : "Cannot generate Algorithm instance!"})

@app.route("/get_composition_status")
async def get_composition_status(request):
    return json({"request" : request.args})

@app.route("/get_num_running_instances")
async def get_num_running_instances(request):
    return json({"num_running_instances" : str(len(algorithm_instances))})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
