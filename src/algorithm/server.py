import CC
from flask import Flask, request, Response
import json
import mysql.connector
from flask_cors import CORS
from multiprocessing.pool import ThreadPool
from components.DBConfig import DBConfig

server_ip = "127.0.0.1"
server_port = "5000"

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

    cursor.close()

    connection.close()

    str_response = ""
    for configuration in configurations:
        str_response += '<option value="' + str(configuration[0]) + '">' + configuration[1] + '</option>'

    return str_response

@app.route('/refresh_configname_select', methods=['GET'])
def refresh_configname_select():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT id, nome FROM configurazioni;"

    cursor.execute(query)

    confignames = cursor.fetchall()

    cursor.close()

    connection.close()

    if len(confignames) > 0:
        str_response = ""
        for row in confignames:
            str_response += '<option value="' + str(row[0]) + '">' + row[1] + '</option>'
    else:
        str_response = '<option value="0" disabled>Impossibile connettersi al database.</option>'
    
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

    cursor.close()

    connection.close()

    str_response = ""
    for group in groups:
        group_type = " - Classi Terze" if group[2] == 3 else " - Classi Prime"
        str_response += '<option value="' + str(group[0]) + '">' + group[1] + group_type + '</option>'

    return str_response

@app.route('/refresh_visualizecc_table', methods=['GET'])
def refresh_visualizecc_table():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT gruppi.nome, configurazioni.nome, COUNT(*), groupid, configid FROM classi_composte LEFT JOIN gruppi ON classi_composte.groupid = gruppi.id LEFT JOIN configurazioni ON classi_composte.configid = configurazioni.id GROUP BY gruppi.id"

    cursor.execute(query)

    generations = cursor.fetchall()

    cursor.close()

    connection.close()

    str_response = '''<table style="box-shadow: 1px 1px 10px #BBBBBB;" class="striped centered">
                        <thead>
                         <tr>
                             <th>Nome Gruppo</th>
                             <th>Nome Configurazione</th>
                             <th>Numero di Studenti</th>
                             <th>Visualizzazione</th>
                             <th>Export CSV</th>
                         </tr>
                        </thead>

                        <tbody>'''
    for generation in generations:
        str_response += "<tr>"

        str_response += "<td>" + str(generation[0]) + "</td>"
        str_response += "<td>" + str(generation[1]) + "</td>"
        str_response += "<td>" + str(generation[2]) + "</td>"

        str_response += f'<td><a href="http://{server_ip}:{server_port}/infographics.html?groupid={generation[3]}&configid={generation[4]}" target="_blank">Visualizza</a></td>'
        str_response += f'<td><a href="http://{server_ip}:{server_port}/export_generatedcc_to_csv?groupid={generation[3]}&configid={generation[4]}">Esporta</a></td>'

        str_response += "</tr>"


    str_response += "</tbody></table>"

    return str_response

@app.route('/export_generatedcc_to_csv', methods=['GET'])
def export_generatedcc_to_csv():

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    groupid = request.args.get('groupid')
    configid = request.args.get('configid')

    query = f"SELECT classid, matricola, cognome, nome, sesso, voto FROM classi_composte LEFT JOIN alunni ON alunni.id = classi_composte.studentid WHERE groupid = {groupid} AND configid = {configid} ORDER BY classid, cognome, nome;"

    cursor.execute(query)

    records = cursor.fetchall()

    cursor.close()

    connection.close()

    generator = (
        str(record)
        .replace(', ', ';')
        .replace("'", "")
        .replace('(', '')
        .replace(')', '') + "\n"
        for record in records
    )

    return Response(generator,
                       mimetype="text/plain",
                       headers={"Content-Disposition":
                                    f"attachment;filename=EXPORT_GROUPID_{groupid}_CONFIGID_{configid}.csv"})


def get_chart_data_orderby_classid_matricola_voto(groupid, configid):
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = f"SELECT classid, matricola, voto FROM classi_composte LEFT JOIN alunni on classi_composte.studentid = alunni.id WHERE classi_composte.groupid = {groupid} AND classi_composte.configid = {configid} ORDER BY classi_composte.classid, alunni.voto;"

    cursor.execute(query)

    students = cursor.fetchall()

    cursor.close()

    connection.close()

    output_dict = {"1" : {}}
    current_index = 1
    for student in students:
        if student[0] != current_index:
            current_index += 1
            output_dict[str(current_index)] = {}

        output_dict[str(current_index)][student[1]] = student[2]

    return json.dumps(output_dict)
