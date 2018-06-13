import CC
from flask import Flask, request
import json
import mysql.connector
from flask_cors import CORS
from multiprocessing.pool import ThreadPool
from components.DBConfig import DBConfig

app = Flask(__name__)
CORS(app)

@app.route('/get_cc_result', methods=['POST'])
def get_cc_result():
    post_data = request.form
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(CC.create_cc_instance, (0, post_data["groupid"], post_data["configid"]))
    return_val = async_result.get()
    return return_val

@app.route('/get_cc_visualization', methods=['POST'])
def get_cc_visualization():
    post_data = request.form
    group_id = post_data["groupid"]
    config_id = post_data["configid"]
    pass


@app.route('/refresh_configid_select', methods=['GET'])
def refresh_configid_select():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT id, nome FROM configurazioni;"

    cursor.execute(query)

    configurations = cursor.fetchall()

    str_response = ""
    for configuration in configurations:
        str_response += '<option value="' + str(configuration[0]) + '">' + configuration[1] + '</option>'

    cursor.close()

    connection.close()

    return str_response

@app.route('/refresh_groupid_select', methods=['GET'])
def refresh_groupid_select():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT id, nome, tipo FROM gruppi;"

    cursor.execute(query)

    groups = cursor.fetchall()

    str_response = ""
    for group in groups:
        group_type = " - Classi Terze" if group[2] == 3 else " - Classi Prime"
        str_response += '<option value="' + str(group[0]) + '">' + group[1] + group_type + '</option>'

    cursor.close()

    connection.close()

    return str_response
