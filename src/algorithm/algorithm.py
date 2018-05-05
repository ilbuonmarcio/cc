import random
import time
import mysql.connector

class DBConfig:

    user = "root"
    password = ""
    host = "localhost"
    database = "composizioneclassi"


class CC:

    def __init__(self, process_id, group_id, config_id):
        self.process_id = process_id
        self.group_id = group_id
        self.config_id = config_id
        self.students_manager = StudentsManager(self.group_id)
        self.configuration = Configuration(self.config_id)
        self.containers_manager = ContainersManager()

        self.run()

    def run(self):
        print("Running")

        print(f"Loaded students from db with id {self.students_manager.group_id}:",
              self.students_manager.get_number_of_students())
        print(f"Loaded config from db with id {self.configuration.config_id}:",
              self.configuration.config_name)

        print("Done!")


class Configuration:

    def __init__(self, config_id):
        self.config_id = config_id
        self._load_configuration_from_db(self.config_id)

    def _load_configuration_from_db(self, config_id):
        connection = mysql.connector.connect(
                        user=DBConfig.user,
                        password=DBConfig.password,
                        host=DBConfig.host,
                        database=DBConfig.database)

        cursor = connection.cursor()

        query = f"SELECT * FROM configurazioni WHERE id = {config_id};"

        cursor.execute(query)

        for record in cursor:
            self.config_name = record[1]
            self.min_students = record[2]
            self.max_students = record[3]
            self.num_girls = record[4]
            self.num_boys = record[5]
            self.max_for_cap = record[6]
            self.max_for_naz = record[7]
            self.max_naz = record[8]
            self.max_170 = record[9]

        cursor.close()

        connection.close()

    def dict_parameters(self):
        return self.__dict__


class StudentsManager:

    def __init__(self, group_id):
        self.group_id = group_id
        self.students = []
        self._load_students_from_db(self.group_id)

    def _load_students_from_db(self, group_id):
        connection = mysql.connector.connect(
                        user=DBConfig.user,
                        password=DBConfig.password,
                        host=DBConfig.host,
                        database=DBConfig.database)

        cursor = connection.cursor()

        query = f"SELECT * FROM alunni WHERE id = {group_id};"

        cursor.execute(query)

        self.students = cursor.fetchall()

        cursor.close()

        connection.close()

    def get_number_of_students(self):
        return len(self.students)


class ContainersManager:

    def __init__(self):
        pass


class ClassContainer:

    def __init__(self):
        pass


class Student:

    def __init__(self):
        pass


def create_cc_instance(process_id, group_id, config_id):
    cc = CC(process_id, group_id, config_id)
