from sanic import Sanic
from sanic.response import json

class Algorithm:

    def __init__(self, group_id, config_id):
        self.group_id = group_id
        self.config_id = config_id
        self.info = 0
        self.config = self._load_config_from_db()
        self.group = self._load_group_from_db()
        self.run_composition()

    def _load_config_from_db(self):
        pass

    def _load_group_from_db(self):
        pass

    def run_composition(self):
        for i in range(0, 1000000):
            self.info += 1
        self.destroy()

    def get_algorithm_parameters(self):
        return self.group_id, self.config_id

    def get_info(self):
        return str(self.info)

    def save_to_db(self):
        pass

    def destroy(self):
        if self in algorithm_instances:
            algorithm_instances.remove(self)


algorithm_instances = []

app = Sanic()

@app.route("/")
async def test(request):
    return json({"hello": "world"})

@app.route("/create_algorithm_instance")
async def create_algorithm_instance(request):
    if "group_id" in request.args.keys() and "config_id" in request.args.keys():
        group_id, config_id = request.args["group_id"], request.args["config_id"]

        already_present = False
        for instance in algorithm_instances:
            if (group_id, config_id) == instance.get_algorithm_parameters():
                already_present = True
                break

        if already_present:
            return json({"status" : "bad", "response" : "Cannot create a duplicate Algorithm instance"})

        if not already_present:
            algorithm_instances.append(
                Algorithm(group_id, config_id)
            )
            response = {"status" : "good"}
            return json(response)
    else:
        return json({"status" : "bad", "response" : "Bad or absent Algorithm parameters"})

@app.route("/get_num_running_instances")
async def get_num_running_instances(request):
    return json({"num_running_instances" : str(len(algorithm_instances))})

@app.route("/get_info_on_running_instances")
async def get_info_on_running_instances(request):
    response = {"num_running_instances" : str(len(algorithm_instances))}

    algorithm_instances_info = {}
    for instance in algorithm_instances:
        algorithm_instances_info[str(instance.get_algorithm_parameters())] = instance.get_info()

    response["running_instances_info"] = algorithm_instances_info

    return json(response)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)
