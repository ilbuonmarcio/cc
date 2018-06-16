import mysql.connector
from .DBConfig import DBConfig

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
            self.sex_priority = "m" if self.num_girls is None and self.num_boys is not None else "f"
            self.num_sex_priority = self.num_boys if self.sex_priority == "m" else self.num_girls
            self.default_naz = "ITALIANA"

        cursor.close()

        connection.close()

    def parameters(self):
        return self.__dict__

    def __str__(self):
        return self.config_name
