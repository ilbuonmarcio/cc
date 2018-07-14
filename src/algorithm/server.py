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

@app.route('/refresh_groupname_select', methods=['GET'])
def refresh_groupname_select():
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

    if len(groups) > 0:
        str_response = ""
        for group in groups:
            group_type = " - Classi Terze" if group[2] == 3 else " - Classi Prime"
            str_response += '<option value="' + str(group[0]) + '">' + group[1] + group_type + '</option>'
    else:
        str_response = '<option value="0" disabled>Impossibile connettersi al database.</option>'

    return str_response


@app.route('/refresh_users_table', methods=['GET'])
def refresh_users_table():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT id, username, diritti FROM utenti;"

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    connection.close()

    str_response = '''<table style="box-shadow: 1px 1px 10px #BBBBBB;" class="striped centered">
         <thead>
           <tr>
               <th>ID</th>
               <th>Username</th>
               <th>Tipologia</th>
           </tr>
         </thead>

         <tbody>'''
    
    for row in rows:
        user_type = "Amministratore" if row[2] == 0 else str("Editor" if row[2] == 1 else "Visualizzatore")

        str_response += "<tr>"

        str_response += "<td>" + str(row[0]) + "</td>"
        str_response += "<td>" + str(row[1]) + "</td>"
        str_response += "<td>" + user_type + "</td>"

        str_response += "</tr>"


    str_response += "</tbody></table>"

    return str_response


@app.route('/refresh_managegroups_table', methods=['GET'])
def refresh_managegroups_table():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT gruppi.id, gruppi.nome, gruppi.descrizione, gruppi.tipo, COUNT(alunni.id_gruppo) as numero_alunni FROM alunni RIGHT JOIN gruppi ON alunni.id_gruppo = gruppi.id GROUP BY gruppi.id;"

    cursor.execute(query)

    rows = cursor.fetchall()

    cursor.close()

    connection.close()

    str_response = '''<table style="box-shadow: 1px 1px 10px #BBBBBB;" class="striped centered">
         <thead>
           <tr>
               <th>Nome</th>
               <th>Descrizione</th>
               <th>Tipo</th>
               <th>Numero Alunni</th>
               <th>Link</th>
           </tr>
         </thead>

         <tbody>'''
    for row in rows:
        group_type = "Classi Terze" if row[3] == 3 else "Classi Prime"

        str_response += "<tr>"

        str_response += "<td>" + str(row[1]) + "</td>"
        str_response += "<td>" + str(row[2]) + "</td>"
        str_response += "<td>" + group_type + "</td>"
        str_response += "<td>" + str(row[4]) + "</td>"

        str_response += f'<td><a href="http://{server_ip}:{server_port}/groupviewer?groupid={row[0]}">Visualizza</a></td>'

        str_response += "</tr>"


    str_response += "</tbody></table>"

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


@app.route('/routine_createconfig', methods=['POST'])
def routine_createconfig():
    post_data = request.form
    
    configname = post_data["configname"]
    rangeslider_down = post_data["rangeslider_down"]
    rangeslider_up = post_data["rangeslider_up"]
    nummales = post_data["nummales"]
    numfemales = post_data["numfemales"]
    numcap = post_data["numcap"]
    num170 = post_data["num170"]
    numnaz = post_data["numnaz"]
    nummaxforeachnaz = post_data["nummaxforeachnaz"]

    if nummales == "":
        nummales = 'NULL'

    if numfemales == "":
        numfemales = 'NULL'

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)


    if connection:

        cursor = connection.cursor()

        query = f"SELECT * FROM configurazioni WHERE nome = '{configname}'";

        cursor.execute(query)

        if len(cursor.fetchall()) > 0:

            query = f"""UPDATE configurazioni
                        SET
                            min_alunni = {rangeslider_down},
                            max_alunni = {rangeslider_up},
                            numero_femmine = {numfemales},
                            numero_maschi = {nummales},
                            max_per_cap = {numcap},
                            max_per_naz = {nummaxforeachnaz},
                            max_naz = {numnaz},
                            num_170 = {num170}
                        WHERE nome = '{configname}';"""

            cursor.execute(query)

            connection.commit()

            return json.dumps(
                {
                    "status" : "Update Query Executed",
                    "querystatus" : "good"
                }
            )
        
        else:
            query = f"""INSERT INTO configurazioni VALUES (
                            NULL,
                            '{configname}',
                            {rangeslider_down},
                            {rangeslider_up},
                            {numfemales},
                            {nummales},
                            {numcap},
                            {nummaxforeachnaz},
                            {numnaz},
                            {num170}
                        );"""
            
            cursor.execute(query)

            connection.commit()

            return json.dumps(
                {
                    "status" : "Insert Query Executed",
                    "querystatus" : "good"
                }
            )

    else:
        return json.dumps(
            {
                "status" : "No Database Connection",
                "querystatus" : "bad"
            }
        )


@app.route('/routine_creategroup', methods=['POST'])
def routine_creategroup():
    post_data = request.form
    
    groupname = post_data["groupname"]
    groupdesc = post_data["groupdesc"]
    grouptype = post_data["grouptype"]

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    if connection:

        cursor = connection.cursor()

        query = f"INSERT INTO gruppi (id, nome, tipo,  descrizione) VALUES (NULL, '{groupname}', {grouptype}, '{groupdesc}');"

        try:
            cursor.execute(query)

            connection.commit()

            return json.dumps(
                {
                    "status" : "Insert Query Executed",
                    "querystatus" : "good"
                }
            )

        except mysql.connector.errors.IntegrityError:
            
            return json.dumps(
                {
                    "status" : "Insert Query Executed",
                    "querystatus" : "bad",
                    "executedquery" : query
                }
            )

    else:
        return json.dumps(
            {
                "status" : "No Database Connection",
                "querystatus" : "bad"
            }
        )


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
