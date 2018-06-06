import random
import math
import time
import mysql.connector
import copy


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
        global configuration
        configuration = self.configuration
        self.containers_manager = ContainersManager(
            math.ceil(self.students_manager.get_number_of_students() / self.configuration.max_students + 1),
            self.configuration
        )

        self.run()

    def run(self):
        print("Running CC...")

        self.total_number_of_students = self.students_manager.get_number_of_students()


        print(f"Loaded students from db with id {self.students_manager.group_id}:",
              self.total_number_of_students)

        print(f"Loaded config from db with id {self.configuration.config_id}:",
              self.configuration.config_name)

        print(f"Created {self.containers_manager.get_number_of_containers()} empty classes")

        print(f"Sex priority: {self.configuration.sex_priority}")

        configured_sex_priority_array = self.students_manager.get_sex_prioritized_students_array(
            self.configuration.sex_priority,
            self.configuration.num_sex_priority
        )

        self.check_sex_prioritized_array(configured_sex_priority_array)

        if len(configured_sex_priority_array) > self.containers_manager.get_number_of_containers():
            print('<---WARNING---> Sex prioritized groups are more than possible containers!')
            print('ABORT!')
            return False # TODO change return value

        students_not_inserted = self.containers_manager.distribute_sex_prioritized_groups_randomly_into_containers(
            configured_sex_priority_array
        )

        if len(students_not_inserted) > 0:
            print("Some students from prioritized group weren't inserted!")
            for student in students_not_inserted:
                print(f"Student with matricola {student.matricola} was not inserted!")
        else:
            print("No students need to be reinserted, this is a good sign! :))")

        # self.containers_manager.show_containers_statistics()

        print("Pairing and getting remaining students, matching by desiderata when possible...")

        remaining_desiderata_students_array = self.students_manager.get_remaining_desiderata_students_array()

        print(f"Found {len(remaining_desiderata_students_array)} paired students!")

        students_not_inserted = self.containers_manager.distribute_couples_randomly_into_containers(remaining_desiderata_students_array)

        if len(students_not_inserted) > 0:
            print("Some O-O desiderata couple weren't inserted!")
            for couple in students_not_inserted:
                for student in couple:
                    print(f"Student with matricola {student.matricola} was not inserted!")
            print(f"In total there are {len(remaining_desiderata_students_array)} paired students to be reinserted!")
        else:
            print("No students need to be reinserted, this is a good sign! :))")

        print("Getting remaining students on the database...")

        remaining_students_array = self.students_manager.get_remaining_students_array()

        remaining_students_after_random_insert = self.containers_manager.distribute_remaining_students_randomly_into_containers(remaining_students_array)

        print(f"After random fill of remaining students, there are {len(remaining_students_after_random_insert)} students to fill, still!")

        if len(remaining_students_after_random_insert) == 0:
            print("Well done, there is no students to swap of classroom, there!")
        else:
            print("Next move is to implement student of different class' swapping...")

        print("BEFORE OPTIMIZATION:")
        std_sum_before = 0
        for container in self.containers_manager.containers:
            print(f"ContainerID: {id(container)} - Container AVG: {container.get_avg()} - Container STD: {container.get_std()}")
            std_sum_before += container.get_avg()
        print(f"AVG: [{self.containers_manager.get_avg()}] - STD: [{self.containers_manager.get_std()}]")

        self.optimize()

        print("AFTER OPTIMIZATION:")
        std_sum_after = 0
        for container in self.containers_manager.containers:
            print(f"ContainerID: {id(container)} - Container AVG: {container.get_avg()} - Container STD: {container.get_std()}")
            std_sum_after += container.get_avg()
        print(f"AVG: [{self.containers_manager.get_avg()}] - STD: [{self.containers_manager.get_std()}]")

        print(f"RESULTS: {std_sum_before} - {std_sum_after}")

        print("Done!")

    def optimize(self):

        def optimize_containers_on_final_exam_mark(index):

            first_index = index % self.containers_manager.get_number_of_containers()
            second_index = (index + 1) % self.containers_manager.get_number_of_containers()

            previous_std = self.containers_manager.get_std()

            first_container_original = self.containers_manager.get_container_at_index(first_index)
            first_container_copied = self.containers_manager.clone_container_at_index(first_index)
            first_container_backup = self.containers_manager.clone_container_at_index(first_index)
            second_container_original = self.containers_manager.get_container_at_index(second_index)
            second_container_copied = self.containers_manager.clone_container_at_index(second_index)
            second_container_backup = self.containers_manager.clone_container_at_index(second_index)

            while True:
                first_container_student = first_container_copied.get_random_student()
                second_container_student = second_container_copied.get_random_student()

                if first_container_student.eligible_to_swap(self.configuration.sex_priority) \
                    and second_container_student.eligible_to_swap(self.configuration.sex_priority) \
                    and not first_container_copied.has_desiderata(first_container_student) \
                    and not second_container_copied.has_desiderata(second_container_student):
                        break

            # swap them if possible
            first_container_copied.remove_student(first_container_student)
            second_container_copied.remove_student(second_container_student)

            first_result = first_container_copied.add_student(second_container_student)
            second_result = second_container_copied.add_student(first_container_student)

            if first_result is None and second_result is None:
                self.containers_manager.set_container_at_index(first_container_copied, first_index)
                self.containers_manager.set_container_at_index(second_container_copied, second_index)
                if self.containers_manager.get_std() >= previous_std:
                    self.containers_manager.set_container_at_index(first_container_backup, first_index)
                    self.containers_manager.set_container_at_index(second_container_backup, second_index)
                else:
                    # print(f"STD: [{self.containers_manager.get_std()} - {previous_std}]")
                    pass


        current_optimize_index = 0
        optimize_index_limit = min([self.total_number_of_students**2 // 2, 100000])

        print(f"Optimizing in {optimize_index_limit} passes...")
        while True:
            # print(f"OPTCYCLE: {current_optimize_index + 1}")

            # optimize code init

            optimize_containers_on_final_exam_mark(current_optimize_index)

            # optimize code end

            current_optimize_index += 1
            if current_optimize_index == optimize_index_limit:
                break
        print("Finished optimizing!\nIt should be done!")

    def check_sex_prioritized_array(self, configured_sex_priority_array):
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
            self.default_naz = "ITALIANA"

        cursor.close()

        connection.close()

    def parameters(self):
        return self.__dict__

    def __str__(self):
        return self.config_name


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



class ContainersManager:

    def __init__(self, num_of_containers, configuration):
        self.containers = [ClassContainer(configuration) for _ in range(0, num_of_containers)]
        self.configuration = configuration

    def get_number_of_containers(self):
        return len(self.containers)

    def get_std(self):
        containers_avg = self.get_avg()
        return math.sqrt(sum([math.pow(container.marks_avg - containers_avg, 2) for container in self.containers]) / len(self.containers))


    def get_avg(self):
        return sum([container.marks_avg for container in self.containers]) / len(self.containers)

    def distribute_sex_prioritized_groups_randomly_into_containers(self, input_array):
        print("Distributing sex prioritized groups randomly into containers...")

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

        print("Finished distributing sex prioritized groups randomly into containers!")

        return students_to_reinsert

    def distribute_couples_randomly_into_containers(self, input_array):
        print("Distributing O-O couples randomly into containers...")

        students_to_reinsert = []
        for students_array in input_array:
            while True:
                container_to_fill = random.choice(self.containers)
                if container_to_fill.can_add_desiderata(students_array):
                    print(f'Trying to add students [{students_array[0].matricola}, {students_array[1].matricola}] ...')
                    container_to_fill.add_students(students_array)
                    break

        print("Finished distributing O-O couples randomly into containers!")

        return students_to_reinsert

    def distribute_remaining_students_randomly_into_containers(self, input_array):
        print("Distributing remaining students randomly into containers...")

        remaining_students = len(input_array)

        students_to_reinsert = []
        for student in input_array:
            print("Remaining students:", remaining_students)
            containers_already_filled = []
            while True:
                container_to_fill = random.choice(self.containers)
                if len(containers_already_filled) != len(self.containers) \
                   and container_to_fill not in containers_already_filled:

                    if not container_to_fill.maxed_out:
                        student_not_inserted = container_to_fill.add_student(student)

                        if student_not_inserted is not None:
                            containers_already_filled.append(container_to_fill)
                        else:
                            remaining_students -= 1
                            break
                    else:
                        containers_already_filled.append(container_to_fill)
                else:
                    print(f"Cannot fill this student [{student.matricola}]! Need shuffle!")
                    students_to_reinsert.append(student)
                    break
        print("\nFinished distributing remaining students randomly into containers!")

        return students_to_reinsert


    def get_container_at_index(self, index):
        return self.containers[index]

    def clone_container_at_index(self, index):
        return copy.copy(self.get_container_at_index(index))

    def set_container_at_index(self, container, index):
        self.containers[index] = container

    def show_containers_statistics(self):
        print("Showing all containers statistics...")
        for container in self.containers:
            container.show_container_statistics()
        print("\nFinished showing all containers statistics")


class ClassContainer:

    def __init__(self, configuration):
        self.db_group_configuration = configuration
        self.num_students = 0
        self.num_max_students = 0
        self.num_girls = 0
        self.num_boys = 0
        self.num_104 = 0
        self.num_107 = 0
        self.caps = {}
        self.nationalities = {}
        self.students = []
        self.maxed_out = False
        self.has_legge_104 = False
        self.marks_avg = 6

    def get_std(self):
        container_avg = self.get_avg()
        return math.sqrt(sum([math.pow(student.voto - container_avg, 2) for student in self.students]) / len(self.students))

    def get_avg(self):
        return sum([student.voto for student in self.students]) / len(self.students)

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

        # print(f"Adding student with matricola [{student.matricola}]...", end=" ")

        if student.cap in self.caps.keys():
            if self.caps[student.cap] >= self.db_group_configuration.max_for_cap:
                # print(f"Reached max number of students for this cap [{student.cap}] in this container!")
                return student

        if len(self.nationalities.keys()) >= self.db_group_configuration.max_naz \
            and student.nazionalita not in self.nationalities.keys() \
            and student.nazionalita != self.db_group_configuration.default_naz:
            # print(f"Reached max number of nationalities [{self.db_group_configuration.max_naz}] in this container!")
            return student

        if student.nazionalita in self.nationalities.keys():
            if self.nationalities[student.nazionalita] >= self.db_group_configuration.max_for_naz \
               and student.nazionalita != self.db_group_configuration.default_naz:
                # print(f"Reached max number of students with the same nationality [{student.nazionalita}] in this container!")
                return student

        if self.db_group_configuration.num_girls is not None and student.sesso == 'f':
            if self.num_girls >= self.db_group_configuration.num_girls:
                # print(f"Reached max number of girls [{self.num_girls}] in this container!")
                return student

        if self.db_group_configuration.num_boys is not None and student.sesso == 'm':
            if self.num_boys >= self.db_group_configuration.num_boys:
                # print(f"Reached max number of boys [{self.num_boys}] in this container!")
                return student

        if student.legge_104 and self.num_students -1 < 20:
            self.db_group_configuration.max_students = 20
            self.has_legge_104 = True

        if student.legge_104 and self.has_legge_104:
            return student

        if self.num_students >= self.db_group_configuration.max_students:
            self.maxed_out = True
            # print(f"Reached max number of students [{self.num_students}] in this container!")
            return student

        self.students.append(student)

        # print("Done!")

        self.refresh_statistics()

    def remove_student(self, student):
        self.students.remove(student)
        self.refresh_statistics()

    def can_add_desiderata(self, desiderata_students):
        self.refresh_statistics()

        if desiderata_students[0].legge_104 or desiderata_students[1].legge_104:
            if self.has_legge_104:
                return False

        if desiderata_students[0].cap == desiderata_students[1].cap:
            if desiderata_students[0].cap in self.caps.keys():
                if self.caps[desiderata_students[0].cap] > self.db_group_configuration.max_for_cap -2:
                    # print('Check add_desiderata exited on desiderata max for cap reached while caps are equal')
                    return False
        else:
            if desiderata_students[0].cap in self.caps.keys():
                if self.caps[desiderata_students[0].cap] > self.db_group_configuration.max_for_cap -1:
                    # print('Check add_desiderata exited on desiderata max for cap reached while caps are diverse n.1')
                    return False
            if desiderata_students[1].cap in self.caps.keys():
                if self.caps[desiderata_students[1].cap] > self.db_group_configuration.max_for_cap -1:
                    # print('Check add_desiderata exited on desiderata max for cap reached while caps are diverse n.2')
                    return False


        if desiderata_students[0].nazionalita != self.db_group_configuration.default_naz \
           and desiderata_students[1].nazionalita != self.db_group_configuration.default_naz:
            if desiderata_students[0].nazionalita != desiderata_students[1].nazionalita:
                if desiderata_students[0].nazionalita in self.nationalities.keys():
                    if self.nationalities[desiderata_students[0].nazionalita] > self.db_group_configuration.max_for_naz -1:
                        # print('Check add_desiderata exited on checking max num of nationalities while nationalities are not equal n.1')
                        return False
                if desiderata_students[1].nazionalita in self.nationalities.keys():
                    if self.nationalities[desiderata_students[1].nazionalita] > self.db_group_configuration.max_for_naz -1:
                        # print('Check add_desiderata exited on checking max num of nationalities while nationalities are not equal n.2')
                        return False

                if (desiderata_students[0].nazionalita not in self.nationalities.keys() \
                   and desiderata_students[1].nazionalita in self.nationalities.keys()) \
                   or (desiderata_students[0].nazionalita in self.nationalities.keys() \
                   and desiderata_students[1].nazionalita not in self.nationalities.keys()):
                    if len(self.nationalities.keys()) > self.db_group_configuration.max_naz -1:
                        # print('Check add_desiderata exited on max nationalities while one of them are not already inside')
                        return False

            if desiderata_students[0].nazionalita == desiderata_students[1].nazionalita:
                if desiderata_students[0].nazionalita in self.nationalities.keys():
                    if self.nationalities[desiderata_students[0].nazionalita] > self.db_group_configuration.max_for_naz -2:
                        # print('Check add_desiderata exited on checking max num of nationalities while nationalities are equal')
                        return False

                if desiderata_students[0] not in self.nationalities.keys():
                    if len(self.nationalities.keys()) > self.db_group_configuration.max_naz -1:
                        # print('Check add_desiderata exited on checking max num of nationalities while nationalities are equal')
                        return False

        if self.db_group_configuration.num_girls is not None:
            if desiderata_students[0].sesso == desiderata_students[1].sesso:
                if desiderata_students[0].sesso == 'f' and self.num_girls > self.db_group_configuration.num_girls -2:
                    # print('Check add_desiderata exited on num girls while sex is equal')
                    return False
            else:
                if desiderata_students[0].sesso == 'f' and self.num_girls > self.db_group_configuration.num_girls -1:
                    # print('Check add_desiderata exited on num girls while sex is not equal n.1')
                    return False
                if desiderata_students[1].sesso == 'f' and self.num_girls > self.db_group_configuration.num_girls -1:
                    # print('Check add_desiderata exited on num girls while sex is not equal n.2')
                    return False

        if self.db_group_configuration.num_boys is not None:
            if desiderata_students[0].sesso == desiderata_students[1].sesso:
                if desiderata_students[0].sesso == 'm' and self.num_boys > self.db_group_configuration.num_boys -2:
                    # print('Check add_desiderata exited on num girls while sex is equal')
                    return False
            else:
                if desiderata_students[0].sesso == 'm' and self.num_boys > self.db_group_configuration.num_boys -1:
                    # print('Check add_desiderata exited on num girls while sex is not equal n.1')
                    return False
                if desiderata_students[1].sesso == 'm' and self.num_boys > self.db_group_configuration.num_boys -1:
                    # print('Check add_desiderata exited on num girls while sex is not equal n.2')
                    return False

        if desiderata_students[0].legge_104 == "s" or desiderata_students[1].legge_104 == "s":
            desiderata_with_104 = True

        if self.num_students > self.db_group_configuration.max_students -2 and not desiderata_with_104:
            # print('Check add_desiderata exited on num_students with 104')
            return False

        self.refresh_statistics()

        return True

    def get_random_student(self):
        return random.choice(self.students)

    def has_desiderata(self, student):
        for other in self.students:
            if student.check_desiderata(other):
                return True
        return False

    def refresh_statistics(self):
        self.num_students = len(self.students)
        self.num_girls = len([s for s in self.students if s.sesso == 'f'])
        self.num_boys = len([s for s in self.students if s.sesso == 'm'])
        self.num_104 = len([s for s in self.students if s.legge_104 == 's'])
        self.num_107 = len([s for s in self.students if s.legge_170 == 's'])
        self.caps = {key : len(value) for key, value in self.caps.items()}

        nationalities_with_num_of_students = {}
        nationalities = list(set([s.nazionalita for s in self.students]))
        for nationality in nationalities:
            num_of_students = len([s for s in self.students if s.nazionalita == nationality and s.nazionalita != self.db_group_configuration.default_naz])
            nationalities_with_num_of_students[nationality] = num_of_students

        self.nationalities = nationalities_with_num_of_students

        self.maxed_out = self.db_group_configuration.max_students == self.num_students

        self.has_legge_104 = False
        for student in self.students:
            if student.legge_104:
                self.has_legge_104 = True
                break

        self.marks_avg = sum([student.voto for student in self.students]) / len(self.students) if len(self.students) > 0 else 6

    def show_container_statistics(self):
        print("\n[*] Showing container statistics...")
        for attribute, value in self.__dict__.items():
            if attribute == "students":
                print(attribute, [student.matricola for student in self.students])
            else:
                print(attribute, value)

        print("[*] End of container statistics")


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

    def eligible_to_swap(self, sex_priority):
        return self.legge_104 != "s" and self.legge_170 != "s" and self.sesso != sex_priority


def create_cc_instance(process_id, group_id, config_id):
    cc = CC(process_id, group_id, config_id)
