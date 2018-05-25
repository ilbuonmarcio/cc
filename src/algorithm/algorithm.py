import random
import math
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
        self.containers_manager = ContainersManager(
            math.ceil(self.students_manager.get_number_of_students() / self.configuration.min_students),
            self.configuration
        )

        self.run()

    def run(self):
        print("Running")

        print(f"Loaded students from db with id {self.students_manager.group_id}:",
              self.students_manager.get_number_of_students())
        print(f"Loaded config from db with id {self.configuration.config_id}:",
              self.configuration.config_name)

        # [print(student) for student in self.students_manager.get_remaining_students()]

        print(f"Created {self.containers_manager.get_number_of_containers()} empty classes")

        # TODO: data manipulation

        print(f"Sex priority: {self.configuration.sex_priority}")

        configured_sex_priority_array = self.students_manager.get_sex_prioritized_students_array(
            self.configuration.sex_priority,
            self.configuration.num_sex_priority
        )

        self._DEBUG_check_sex_prioritized_array(configured_sex_priority_array)

        if len(configured_sex_priority_array) > self.containers_manager.get_number_of_containers():
            print('<---WARNING---> Sex prioritized groups are more than possible containers!')
            print('ABORT!')
            return False # TODO change return value

        students_not_inserted = self.containers_manager.distribute_arrays_randomly_into_containers(configured_sex_priority_array)

        if len(students_not_inserted) > 0:
            print("Some students from prioritized group weren't inserted!")
            for student in students_not_inserted:
                print(f"Student with matricola {student.matricola} was not inserted!")

        print("Done!")

    def _DEBUG_check_sex_prioritized_array(self, configured_sex_priority_array):
        print("Checking sex-prioritized array...")
        for student_group in configured_sex_priority_array:
            print(f"Student group length: {len(student_group)}", end="")

            num_males, num_females = 0, 0
            for student in student_group:
                if student.sesso == "m":
                    num_males += 1
                if student.sesso == "f":
                    num_females += 1

            print(f" - M: {num_males} - F: {num_females}")
        print("Finished checking sex-prioritized array...")


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

        cursor.close()

        connection.close()

    def parameters(self):
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

        query = f"SELECT * FROM alunni WHERE id_gruppo = {group_id};"

        cursor.execute(query)

        self.students = cursor.fetchall()

        self.students = [Student(student_record) for student_record in self.students]

        cursor.close()

        connection.close()

    def get_number_of_students(self):
        return len(self.students)

    def get_remaining_students(self):
        return self.students

    def get_sex_prioritized_students_array(self, sex_priority, num_sex_priority):
        sex_priority_students = []
        othersex_students = []
        for student in self.students:
            if student.sesso == sex_priority:
                sex_priority_students.append(student)
            else:
                othersex_students.append(student)

        for student in sex_priority_students:
            self.students.remove(student)

        sex_priority_students_groupped = {
            "female-female" : {},
            "female-male" : {}
        }

        for student in sex_priority_students:
            for other in sex_priority_students:
                if student.check_desiderata(other):
                    if other.matricola + "-" + student.matricola \
                        not in sex_priority_students_groupped["female-female"].keys():
                        print(f"Matched S-S! {student.matricola} <--> {other.matricola}")
                        sex_priority_students_groupped["female-female"][
                            student.matricola + "-" + other.matricola
                        ] = [student, other]

        othersex_to_remove_from_students = []
        for student in sex_priority_students:
            for other in othersex_students:
                if student.check_desiderata(other):
                    if other.matricola + "-" + student.matricola \
                        not in sex_priority_students_groupped["female-male"].keys():
                        print(f"Matched S-O! {student.matricola} <--> {other.matricola}")
                        sex_priority_students_groupped["female-male"][
                            student.matricola + "-" + other.matricola
                        ] = [student, other]
                        othersex_to_remove_from_students.append(student)
                        othersex_to_remove_from_students.append(other)

        for student in othersex_to_remove_from_students:
            if student in self.students:
                self.students.remove(student)

        index = 0
        arranged_students_based_on_config = [[]]
        for student_couple in sex_priority_students_groupped["female-female"].values():
            if len(arranged_students_based_on_config[index]) + 2 > num_sex_priority:
                arranged_students_based_on_config.append([])
                index += 1

            arranged_students_based_on_config[index].append(student_couple[0])
            arranged_students_based_on_config[index].append(student_couple[1])

        index = 0
        for student_couple in sex_priority_students_groupped["female-male"].values():
            while len(arranged_students_based_on_config[index]) + 1 > num_sex_priority:
                index += 1
            arranged_students_based_on_config.append([])
            arranged_students_based_on_config[index].append(student_couple[0])
            arranged_students_based_on_config[index].append(student_couple[1])

        result_set = []
        for array in arranged_students_based_on_config:
            if len(array) > 0:
                result_set.append(array)

        return result_set


class ContainersManager:

    def __init__(self, num_of_containers, configuration):
        self.containers = [ClassContainer(configuration) for _ in range(0, num_of_containers)]
        self.configuration = configuration

    def get_number_of_containers(self):
        return len(self.containers)

    def distribute_arrays_randomly_into_containers(self, input_array):
        print("Distributing arrays randomly into containers...")

        containers_already_filled = []
        students_to_reinsert = []
        for students_array in input_array:
            while True:
                container_to_fill = random.choice(self.containers)
                if container_to_fill not in containers_already_filled:
                    students_not_inserted = container_to_fill.add_students(students_array)

                    if len(students_not_inserted) > 0:
                        print("Warning! Student to reinsert found!")
                        for student in students_not_inserted:
                            students_to_reinsert.append(student)
                    containers_already_filled.append(container_to_fill)
                    break

        print("Finished distributing arrays randomly into containers!")

        return students_to_reinsert


class ClassContainer:

    def __init__(self, configuration):
        self.db_group_configuration = configuration
        self.num_students = 0
        self.num_max_students = 0
        self.num_girls = 0
        self.num_boys = 0
        self.num_104 = 0
        self.num_107 = 0
        self.caps = []
        self.nationalities = {}
        self.students = []
        self.maxed_out = False

    def add_students(self, input_array):
        self.refresh_statistics()

        students_not_inserted = []
        for student in input_array:
            addition_result = self.add_student(student)
            if addition_result is not None:
                students_not_inserted.append(student)

        self.refresh_statistics()

        return students_not_inserted

    def add_student(self, student):
        self.refresh_statistics()

        print(f"Adding {student.matricola}...", end=" ")

        if student.legge_104:
            self.db_group_configuration.max_students = 20

        if self.num_students >= self.db_group_configuration.max_students:
            self.maxed_out = True
            return student

        if len(self.caps) >= self.db_group_configuration.max_for_cap \
            and student.cap not in self.caps:
            return student

        if len(self.nationalities.keys()) >= self.db_group_configuration.max_naz \
            and student.nazionalita not in self.nationalities.keys():
            return student

        if student.nazionalita in self.nationalities.keys():
            if self.nationalities[student.nazionalita] >= self.db_group_configuration.max_for_naz:
                return student

        if self.db_group_configuration.num_girls is not None:
            if self.num_girls >= self.db_group_configuration.num_girls:
                return student

        if self.db_group_configuration.num_boys is not None:
            if self.num_boys >= self.db_group_configuration.num_boys:
                return student

        self.students.append(student)

        print("Done!")

        self.refresh_statistics()

    def refresh_statistics(self):
        self.num_students = len(self.students)
        self.num_girls = len([s for s in self.students if s.sesso == 'f'])
        self.num_boys = len([s for s in self.students if s.sesso == 'm'])
        self.num_104 = len([s for s in self.students if s.legge_104 == 's'])
        self.num_107 = len([s for s in self.students if s.legge_170 == 's'])
        self.caps = list(set([s.cap for s in self.students]))

        nationalities_with_num_of_students = {}
        nationalities = list(set([s.nazionalita for s in self.students]))
        for nationality in nationalities:
            num_of_students = len([s for s in self.students if s.nazionalita == nationality])
            nationalities_with_num_of_students[nationality] = num_of_students

        self.nationalities = nationalities_with_num_of_students

        self.maxed_out = self.db_group_configuration.max_students == self.num_students


class Student:

    def __init__(self, student_record):
        self.id = student_record[0]
        self.cognome = student_record[1]
        self.nome = student_record[2]
        self.matricola = student_record[3]
        self.cf = student_record[4]
        self.desiderata = student_record[5]
        self.sesso = student_record[6]
        self.data_nascita = student_record[7]
        self.cap = student_record[8]
        self.nazionalita = student_record[9]
        self.legge_170 = student_record[10]
        self.legge_104 = student_record[11]
        self.classe_precedente = student_record[12]
        self.classe_successiva = student_record[13]
        self.scelta_indirizzo = student_record[14]
        self.cod_cat = student_record[15]
        self.voto = student_record[16]
        self.id_gruppo = student_record[17]

    def __repr__(self):
        return str(self.__dict__)

    def check_desiderata(self, other):
        if self.matricola != other.matricola and \
           self.id != other.id and \
           self.desiderata == other.cf and \
           other.desiderata == self.cf:
           return True
        return False


def create_cc_instance(process_id, group_id, config_id):
    cc = CC(process_id, group_id, config_id)
