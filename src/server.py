from algorithm import CC
from flask import Flask, request, Response, render_template, redirect, send_from_directory, session
import json
import mysql.connector
import authenticator
from flask_cors import CORS
from multiprocessing.pool import ThreadPool
from algorithm.components.DBConfig import DBConfig
import os
from werkzeug.utils import secure_filename
import csv
import io

server_ip = "127.0.0.1"
server_port = "80"
server_prefix = "/cc"

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = set(['csv'])

app = Flask(__name__, template_folder="")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = os.urandom(24)

@app.route(server_prefix + '/get_cc_result', methods=['POST'])
def get_cc_result():
    post_data = request.form
    pool = ThreadPool(processes=1)
    async_result = pool.apply_async(CC.create_cc_instance, (0, post_data["groupid"], post_data["configid"]))
    return_val = async_result.get()
    return return_val

@app.route(server_prefix + '/get_cc_visualization', methods=['POST'])
def get_cc_visualization():
    post_data = request.form
    group_id = post_data["groupid"]
    config_id = post_data["configid"]
    pass


@app.route(server_prefix + '/refresh_configid_select', methods=['GET'])
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

@app.route(server_prefix + '/refresh_configname_select', methods=['GET'])
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

@app.route(server_prefix + '/refresh_groupid_select', methods=['GET'])
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

@app.route(server_prefix + '/refresh_groupname_select', methods=['GET'])
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


@app.route(server_prefix + '/refresh_users_table', methods=['GET'])
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


@app.route(server_prefix + '/refresh_managegroups_table', methods=['GET'])
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

        str_response += '<td><a href="http://' + server_ip + ':' + server_port + server_prefix + '/groupviewer?groupid=' + str(row[0]) + '&groupname=' + str(row[1]) + '" target="_blank">Visualizza</a></td>'

        str_response += "</tr>"


    str_response += "</tbody></table>"

    return str_response


@app.route(server_prefix + '/groupviewer', methods=['GET'])
def groupviewer():
    groupid = request.args.get('groupid')
    groupname = request.args.get('groupname')

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    if connection:

        cursor = connection.cursor()

        query = "SELECT * FROM alunni WHERE id_gruppo = '" + groupid + "' ORDER BY sesso;"

        cursor.execute(query)

        rows = cursor.fetchall()

        group_table = '''<table class="striped centered box-shadow">
      						<thead>
      						  <tr>
      							  <th>Cognome</th>
      							  <th>Nome</th>
      							  <th>Matricola</th>
      							  <th>Codice Fiscale</th>
      							  <th>Desiderata</th>
      							  <th>Sesso</th>
      							  <th>Data di nascita</th>
      							  <th>Cap</th>
      							  <th>Nazionalita</th>
      							  <th>Legge 170</th>
      							  <th>Legge 104</th>
      							  <th>Classe precedente</th>
      							  <th>Classe sucessiva</th>
      							  <th>Scelta indirizzo</th>
      							  <th>Codice catastale</th>
      							  <th>Voto</th>
      							  <th>Id gruppo</th>
      						  </tr>
      						</thead>
      					<tbody>'''

        if len(rows) > 0:

            for row in rows:
                if row[6] == "m" or row[6] == "M":
                    group_table += '<tr style="background-color: #99ffff;">'
                else:
                    group_table += '<tr style="background-color: #ff9999;">'

                group_table += '''<td>''' + row[1] + '''</td>
                                        <td>''' + row[2] + '''</td>
                                        <td>''' + row[3] + '''</td>
                                        <td>''' + row[4] + '''</td>
                                        <td>''' + row[5] + '''</td>
                                        <td>''' + row[6] + '''</td>
                                        <td>''' + row[7] + '''</td>
                                        <td>''' + row[8] + '''</td>
                                        <td>''' + row[9] + '''</td>
                                        <td>''' + row[10] + '''</td>
                                        <td>''' + row[11] + '''</td>
                                        <td>''' + row[12] + '''</td>
                                        <td>''' + row[13] + '''</td>
                                        <td>''' + row[14] + '''</td>
                                        <td>''' + row[15] + '''</td>
                                        <td>''' + row[16] + '''</td>
                                        <td>''' + row[17] + '''</td>
                                    </tr>'''

            group_table += '''</tbody>
                                </table>


                                <div id="group-label">
                                    <p id="label">''' + groupname + '''</p>
                                </div>'''

        else:
            group_table = '<h2 style="color: red;" class="center-align">Tabella vuota!</h2>'
    
    else:
        group_table = '<h2 style="color: red;" class="center-align">Tabella non disponibile! Errore di connessione al database.</h2>'

    return render_template('viewer.html', group_table=group_table)


@app.route(server_prefix + '/infographics')
def infographics():
    if 'authenticated' not in session:
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')
    elif not session['authenticated']:
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')
    return render_template('infographics.html')


@app.route(server_prefix + '/refresh_visualizecc_table', methods=['GET'])
def refresh_visualizecc_table():
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT gruppi.nome, configurazioni.nome, COUNT(*), groupid, configid FROM classi_composte LEFT JOIN gruppi ON classi_composte.groupid = gruppi.id LEFT JOIN configurazioni ON classi_composte.configid = configurazioni.id GROUP BY gruppi.id, configurazioni.id"

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

        str_response += '<td><a href="http://' + server_ip + ':' + server_port + server_prefix + '/infographics?groupid=' + str(generation[3]) + '&configid=' + str(generation[4]) + '" target="_blank">Visualizza</a></td>'
        str_response += '<td><a href="http://' + server_ip + ':' + server_port + server_prefix + '/export_generatedcc_to_csv?groupid=' + str(generation[3]) + '&configid=' + str(generation[4]) + '">Esporta</a></td>'

        str_response += "</tr>"


    str_response += "</tbody></table>"

    return str_response

@app.route(server_prefix + '/export_generatedcc_to_csv', methods=['GET'])
def export_generatedcc_to_csv():

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    groupid = request.args.get('groupid')
    configid = request.args.get('configid')

    query = "SELECT classid, matricola, cognome, nome, sesso, voto FROM classi_composte LEFT JOIN alunni ON alunni.id = classi_composte.studentid WHERE groupid = " + groupid + " AND configid = " + configid + " ORDER BY classid, cognome, nome;"

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
                                    "attachment;filename=EXPORT_GROUPID_" + groupid + "_CONFIGID_" + configid + ".csv"})


@app.route(server_prefix + '/routine_createconfig', methods=['POST'])
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

        query = "SELECT * FROM configurazioni WHERE nome = '" + configname + "'"

        cursor.execute(query)

        if len(cursor.fetchall()) > 0:

            query = """UPDATE configurazioni
                        SET
                            min_alunni = """ + rangeslider_down + """,
                            max_alunni = """ + rangeslider_up + """,
                            numero_femmine = """ + numfemales + """,
                            numero_maschi = """ + nummales + """,
                            max_per_cap = """ + numcap + """,
                            max_per_naz = """ + nummaxforeachnaz + """,
                            max_naz = """ + numnaz + """,
                            num_170 = """ + num170 + """
                        WHERE nome = '""" + configname + """';"""

            cursor.execute(query)

            connection.commit()

            query = """DELETE FROM classi_composte
                        WHERE configid = (
                            SELECT id FROM configurazioni WHERE nome = '""" + configname + """'
                        );"""

            cursor.execute(query)

            connection.commit()

            return json.dumps(
                {
                    "status" : "Update Query Executed",
                    "querystatus" : "good"
                }
            )

        else:
            query = """INSERT INTO configurazioni VALUES (
                            NULL,
                            '""" + configname + """',
                            """ + rangeslider_down + """,
                            """ + rangeslider_up + """,
                            """ + numfemales + """,
                            """ + nummales + """,
                            """ + numcap + """,
                            """ + nummaxforeachnaz + """,
                            """ + numnaz + """,
                            """ + num170 + """
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


@app.route(server_prefix + '/routine_creategroup', methods=['POST'])
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

        query = "INSERT INTO gruppi (id, nome, tipo,  descrizione) VALUES (NULL, '" + groupname + "', " + grouptype + ", '" + groupdesc + "');"

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


@app.route(server_prefix + '/routine_deletegroup', methods=['POST'])
def routine_deletegroup():
    post_data = request.form

    groupid = post_data["groupname"]

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    if connection:

        cursor = connection.cursor()

        removeAlumniQuery = "DELETE FROM alunni WHERE alunni.id_gruppo = " + groupid + ";"
        removeGroupQuery = "DELETE FROM gruppi WHERE gruppi.id = " + groupid + ";"
        removeCCQuery = "DELETE FROM classi_composte WHERE groupid = " + groupid + ";"

        try:
            cursor.execute(removeAlumniQuery)
            cursor.execute(removeGroupQuery)
            cursor.execute(removeCCQuery)

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
                    "executedquery" : removeAlumniQuery + " " + removeGroupQuery + " " + removeCCQuery
                }
            )

    else:
        return json.dumps(
            {
                "status" : "No Database Connection",
                "querystatus" : "bad"
            }
        )

    


@app.route(server_prefix + '/routine_uploadcsv', methods=['POST'])
def routine_uploadcsv():
    if request.method == 'POST':

        post_data = request.form

        groupname = post_data["groupname"]

        if 'filepath' not in request.files:
            return json.dumps(
                {
                    "status" : "No File in POST request",
                    "querystatus" : "bad"
                }
            )

        csv_file = request.files['filepath']

        if csv_file.filename == '':
            return json.dumps(
                {
                    "status" : "File with no name uploaded",
                    "querystatus" : "bad"
                }
            )
        if csv_file and allowed_file(csv_file.filename):

            stream = io.StringIO(csv_file.stream.read().decode("UTF8"), newline=None)
            csv_file = csv.reader(stream)

            connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

            right, wrong = 0, {}

            if connection:

                cursor = connection.cursor()

                stringarraypositions = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 14]

                index = 0
                for row in csv_file:
                    index += 1

                    query = "INSERT INTO alunni VALUES"
                    query += "(NULL, "

                    for i in range(0, len(row)):
                        if row[i] == "":
                            query += "NULL, "
                            continue
                        
                        if i in stringarraypositions:
                            query += "'" + row[i] + "', "
                        else:
                            query += row[i] + ", "

                    query += groupname + ");"

                    try:
                        cursor.execute(query)
                        connection.commit()

                        right += 1
                    except:
                        wrong[str(index)] = "Error on line index " + index + "!"

                query = "UPDATE alunni SET sesso = LOWER(sesso);"

                cursor.execute(query)
                connection.commit()

                return json.dumps(
                    {
                        "status" : "Query Executed!",
                        "querystatus" : "good",
                        "right" : right,
                        "wrong" : json.dumps(wrong)
                    }
                )

            else: 
                return json.dumps(
                    {
                        "status" : "No Database Connection",
                        "querystatus" : "bad",
                        "right" : right,
                        "wrong" : json.dumps(wrong)
                    }
                )





@app.route(server_prefix + '/routine_loadconfig', methods=['POST'])
def routine_loadconfig():
    post_data = request.form

    configid = post_data["configid"]

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    if connection:

        cursor = connection.cursor()

        query = "SELECT * FROM configurazioni WHERE id = '" + configid + "';"

        cursor.execute(query)

        try:
            row = cursor.fetchall()[0]

            return json.dumps(
                {
                    "status" : 'Query Executed',
                    "querystatus" : 'good',
                    "values" : {
                        "configid" : row[0],
                        "configname" : row[1],
                        "min_alunni" : row[2],
                        "max_alunni" : row[3],
                        "numero_femmine" : row[4] if row[4] != None else "",
                        "numero_maschi" : row[5] if row[5] != None else "",
                        "max_per_cap" : row[6],
                        "max_per_naz" : row[7],
                        "max_naz" : row[8],
                        "num_170" : row[9]
                    }
                }
            )

        except:
            return json.dumps(
                {
                    "status" : "Query Executed",
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



@app.route(server_prefix + '/routine_createuser', methods=['POST'])
def routine_createuser():
    post_data = request.form

    username = post_data["username"]
    password = post_data["password"]
    priviledges = post_data["priviledges"]

    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    if connection:

        cursor = connection.cursor()

        query = "SELECT * FROM utenti WHERE username = '" + username + "';"

        cursor.execute(query)

        rows = cursor.fetchall()

        if len(rows) > 0:
            return json.dumps(
                {
                    "status" : "Username already present!",
                    "querystatus" : "bad"
                }
            )

        else:

            hashed_password, salt = authenticator.generate_hashed_password_and_salt_by_password(password)

            query = "INSERT INTO utenti (id, username, hashed_password, salt, diritti) VALUES (NULL, '" + username + "', '" + hashed_password + "', '" + salt + "', " + priviledges + ");"

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


@app.route(server_prefix + '/authenticate', methods=["POST"])
def authenticate():
    post_data = request.form

    username = post_data["username"]
    password = post_data["password"]

    try:
        user_authenticated = authenticator.authenticate_user(username, password)
        # print("User " + username + " authenticated: " + user_authenticated)
    except Exception as e:
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')

    if user_authenticated:
        session['username'] = username
        session['authenticated'] = True
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/index')
    else:
        session['authenticated'] = False
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')


@app.route(server_prefix + '/')
def root():
    session['authenticated'] = False
    return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/login')

@app.route(server_prefix + '/login')
def login():
    session['authenticated'] = False
    return render_template('login.html', server_ip=server_ip, server_port=server_port, server_prefix=server_prefix)

@app.route(server_prefix + '/logout')
def logout():
    session['authenticated'] = False
    return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')

@app.route(server_prefix + '/index')
def index():
    if 'authenticated' not in session:
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')
    elif not session['authenticated']:
        return redirect('http://' + server_ip + ':' + server_port + server_prefix + '/')
    return render_template('index.html', username=session["username"], server_ip=server_ip, server_port=server_port, server_prefix=server_prefix)

@app.route(server_prefix + '/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route(server_prefix + '/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


@app.route(server_prefix + '/get_charts_data', methods=["GET"])
def get_charts_data():

    groupid = request.args.get('groupid')
    configid = request.args.get('configid')
    
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT classid, matricola, voto FROM classi_composte LEFT JOIN alunni on classi_composte.studentid = alunni.id WHERE classi_composte.groupid = " + groupid + " AND classi_composte.configid = " + configid + " ORDER BY classi_composte.classid, alunni.voto;"

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
	
@app.route(server_prefix + '/get_charts_data_cap', methods=["GET"])
def get_charts_data_cap():

    groupid = request.args.get('groupid')
    configid = request.args.get('configid')
    
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT classid, matricola, cap FROM classi_composte LEFT JOIN alunni on classi_composte.studentid = alunni.id WHERE classi_composte.groupid = " + groupid + " AND classi_composte.configid = " + configid + " ORDER BY classi_composte.classid, alunni.cap;"

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

@app.route(server_prefix + '/get_charts_data_naz', methods=["GET"])
def get_charts_data_naz():

    groupid = request.args.get('groupid')
    configid = request.args.get('configid')
    
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT classid, matricola, nazionalita FROM classi_composte LEFT JOIN alunni on classi_composte.studentid = alunni.id WHERE classi_composte.groupid = " + groupid + " AND classi_composte.configid = " + configid + " ORDER BY classi_composte.classid, alunni.nazionalita;"

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
	
@app.route(server_prefix + '/get_charts_data_male_female', methods=["GET"])
def get_charts_data_male_female():

    groupid = request.args.get('groupid')
    configid = request.args.get('configid')
    
    connection = mysql.connector.connect(
                    user=DBConfig.user,
                    password=DBConfig.password,
                    host=DBConfig.host,
                    database=DBConfig.database)

    cursor = connection.cursor()

    query = "SELECT classid, matricola, sesso FROM classi_composte LEFT JOIN alunni on classi_composte.studentid = alunni.id WHERE classi_composte.groupid = " + groupid + " AND classi_composte.configid = " + configid + " ORDER BY classi_composte.classid, alunni.sesso;"

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    CORS(app)
