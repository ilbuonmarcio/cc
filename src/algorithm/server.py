import CC
import flask
from flask_cors import CORS
from multiprocessing.pool import ThreadPool

app = flask.Flask(__name__)
CORS(app)

@app.route('/get_cc_result', methods=['POST'])
def get_cc_result():
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(CC.create_cc_instance, (0, 1, 1))
    return_val = async_result.get()
    return return_val
