import random
import mysql.connector
from .DBConfig import DBConfig
from .Student import Student

class StudentsManager:

    def __init__(self, group_id):
        self.group_id = group_id
        self.students = []
        self._load_students_from_db(self.group_id)
        random.shuffle(self.students)

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


    def get_remaining_desiderata_students_array(self):
        result_set = {}

        to_remove_from_students = []
        for student in self.students:
            for other in self.students:
                if student.check_desiderata(other):
                    if other.matricola + "-" + student.matricola \
                        not in result_set.keys():
                        print(f"Matched O-O! {student.matricola} <--> {other.matricola}")
                        result_set[
                            student.matricola + "-" + other.matricola
                        ] = [student, other]
                        to_remove_from_students.append(student)
                        to_remove_from_students.append(other)

        for student in to_remove_from_students:
            if student in self.students:
                self.students.remove(student)

        result_set = [value for value in result_set.values()]
        return result_set

    def get_remaining_students_array(self):
        result_set = []

        for student in self.students:
            result_set.append(student)

        return result_set
