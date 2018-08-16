import random
import math
import time
import mysql.connector
import copy
import json

from .components.DBConfig import DBConfig
from .components.Configuration import Configuration
from .components.StudentsManager import StudentsManager
from .components.ContainersManager import ContainersManager


class CC:

    def __init__(self, process_id, group_id, config_id):
        self.process_id = process_id
        self.group_id = group_id
        self.config_id = config_id

    def run(self):
        print("Running CC...")

        if self.group_id == "" or self.config_id == "":
            return "NoGroupOrConfigSelected"

        self.students_manager = StudentsManager(self.group_id)
        self.configuration = Configuration(self.config_id)
        self.containers_manager = ContainersManager(
            14, # TODO: Set dynamic num of containers based on db configuration
            # math.ceil(self.students_manager.get_number_of_students() / self.configuration.max_students),
            self.configuration,
            self.students_manager
        )

        self.total_number_of_students = self.students_manager.get_number_of_students()

        print(f"\n\nCURRENT NUMBER OF STUDENTS INTO CONTAINERS: {self.containers_manager.get_number_of_total_students_into_containers()}\n\n")

        if self.total_number_of_students == 0:
            return "ZeroStudentsIntoGroup"

        print(f"Loaded students from db with id {self.students_manager.group_id}:",
              self.total_number_of_students)

        print(f"Loaded config from db with id {self.configuration.config_id}:",
              self.configuration.config_name)

        if self.is_already_generated():
            print('Class Composition already generated! Exiting...')
            return "CCAlreadyGenerated"

        print(f"Created {self.containers_manager.get_number_of_containers()} empty classes")

        print(f"Sex priority: {self.configuration.sex_priority}")

        configured_sex_priority_array = self.students_manager.get_sex_prioritized_students_array(
            self.configuration.sex_priority,
            self.configuration.num_sex_priority
        )

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

        if len(configured_sex_priority_array) > self.containers_manager.get_number_of_containers():
            print('<---WARNING---> Sex prioritized groups are more than possible containers!')
            print('ABORT!')
            return "TooManySexPrioritizedPeople"

        students_not_inserted = self.containers_manager.distribute_sex_prioritized_groups_randomly_into_containers(
            configured_sex_priority_array
        )


        print("Remaining students into StudentsManager:", self.students_manager.get_number_of_remaining_students())

        print(f"\n\nCURRENT NUMBER OF STUDENTS INTO CONTAINERS: {self.containers_manager.get_number_of_total_students_into_containers()}\n\n")

        if len(students_not_inserted) > 0:
            print("Some students from prioritized group weren't inserted!")
            for student in students_not_inserted:
                print(f"Student with matricola {student.matricola} was not inserted!")
        else:
            print("No students need to be reinserted, this is a good sign! :))")

        # self.containers_manager.show_containers_statistics()
        self.containers_manager.print_all_containers_current_dimensions()

        print("Pairing and getting remaining students, matching by desiderata when possible...")

        remaining_desiderata_students_array = self.students_manager.get_remaining_desiderata_students_array()

        print(f"Found {len(remaining_desiderata_students_array)} paired students!")

        students_not_inserted = self.containers_manager.distribute_couples_randomly_into_containers(remaining_desiderata_students_array)

        print(f"\n\nCURRENT NUMBER OF STUDENTS INTO CONTAINERS: {self.containers_manager.get_number_of_total_students_into_containers()}\n\n")

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
            print(f"We need to fill these {len(remaining_students_after_random_insert)} students somewhere!")

            if not self.containers_manager.fill_remaining_students_shuffling_classcontainers(remaining_students_after_random_insert):
                return "CannotShuffleStudents"

        print(f"\n\nCURRENT NUMBER OF STUDENTS INTO CONTAINERS: {self.containers_manager.get_number_of_total_students_into_containers()}\n\n")

        """
        print("BEFORE OPTIMIZATION:")
        std_sum_before = 0
        for container in self.containers_manager.containers:
            print(f"ContainerID: {container.containerid} - Container AVG: {container.get_avg()} - Container STD: {container.get_std()}")
            std_sum_before += container.get_avg()
        print(f"AVG: [{self.containers_manager.get_avg()}] - STD: [{self.containers_manager.get_std()}]")
        """

        self.optimize()

        """
        print("AFTER OPTIMIZATION:")
        std_sum_after = 0
        for container in self.containers_manager.containers:
            print(f"ContainerID: {container.containerid} - Container AVG: {container.get_avg()} - Container STD: {container.get_std()}")
            std_sum_after += container.get_avg()
        print(f"AVG: [{self.containers_manager.get_avg()}] - STD: [{self.containers_manager.get_std()}]")

        print(f"RESULTS: {std_sum_before} - {std_sum_after}")"""

        print(f"\n\nCURRENT NUMBER OF STUDENTS INTO CONTAINERS: {self.containers_manager.get_number_of_total_students_into_containers()}\n\n")

        uninserted_students_by_matricola = self.students_manager.get_uninserted_students(self.containers_manager)

        if len(uninserted_students_by_matricola) > 0:
            print(f"\nWe found {len(uninserted_students_by_matricola)} students not loaded, inserted and/or elaborated!")
            print("Is it a correct number (TotalStudents == StudentsIntoContainers + UninsertedStudents)? -->", self.total_number_of_students == self.containers_manager.get_number_of_total_students_into_containers() + len(uninserted_students_by_matricola))
            for matricola in uninserted_students_by_matricola:
                print(f"Hey! Student with matricola {matricola} not loaded, inserted and/or elaborated!")
            print("Remaining students into StudentsManager:", self.students_manager.get_number_of_remaining_students())
            return "StudentsNotInsertedAfterShuffling"
        else:
            print("All students were inserted and elaborated correctly, good work!")

        print("Saving CC to database...")
        self.save_students_to_db()

        print("Done!")

        return True

    def optimize(self):

        def get_two_random_containers():
            while True:
                first_container = random.choice(self.containers_manager.containers)
                second_container = random.choice(self.containers_manager.containers)
                if first_container is not second_container:
                    break

            return first_container, second_container

        def get_std_of_two_containers(first_container, second_container):
            first_container_avg = first_container.get_avg()
            second_container_avg = second_container.get_avg()

            containers_avg = (first_container_avg + second_container_avg) / 2

            return math.sqrt(
                (
                    math.pow(first_container_avg - containers_avg, 2) +
                    math.pow(second_container_avg - containers_avg, 2)
                ) / 2)

        def optimize_random_couple_of_containers_fixed_cycles(num_of_cycles):
            first_container, second_container = get_two_random_containers()

            previous_swap_std = get_std_of_two_containers(first_container, second_container)

            effective_changes = 0

            for _ in range(num_of_cycles):

                first_container_student = first_container.get_random_student()
                second_container_student = second_container.get_random_student()

                first_container_student_copy = copy.deepcopy(first_container_student)
                second_container_student_copy = copy.deepcopy(second_container_student)

                if first_container_student.eligible_to_swap(self.configuration.sex_priority) \
                and second_container_student.eligible_to_swap(self.configuration.sex_priority) \
                and not first_container.has_desiderata(first_container_student) \
                and not second_container.has_desiderata(second_container_student):

                    first_container.remove_student(first_container_student)
                    second_container.remove_student(second_container_student)

                    first_result = first_container.add_student(second_container_student)
                    second_result = second_container.add_student(first_container_student)

                    after_swap_std =  get_std_of_two_containers(first_container, second_container)

                    if first_result == None and second_result == None:
                        if after_swap_std >= previous_swap_std:

                            first_container.remove_student(second_container_student)
                            second_container.remove_student(first_container_student)

                            first_result = first_container.add_student(first_container_student_copy)
                            second_result = second_container.add_student(second_container_student_copy)

                        else:
                            effective_changes += 1

                    else:
                        first_container.remove_student(second_container_student)
                        second_container.remove_student(first_container_student)

                        first_result = first_container.add_student(first_container_student_copy)
                        second_result = second_container.add_student(second_container_student_copy)

            return effective_changes


        print("Optimizing...")

        num_of_optimizations = self.total_number_of_students
        num_of_effective_optimizations = 0
        for i in range(0, num_of_optimizations):
            num_of_effective_optimizations += optimize_random_couple_of_containers_fixed_cycles(25)
            if i % 25 == 0:
                print(f"{round(i / num_of_optimizations * 100, 2)}%\t\t{i} \toptcycle\toptsdone\t{num_of_effective_optimizations}\tstudents\t{self.containers_manager.get_number_of_total_students_into_containers()}")

        print(f"100%! Effective swaps done: {num_of_effective_optimizations}\n")

    def save_students_to_db(self):
        connection = mysql.connector.connect(
                        user=DBConfig.user,
                        password=DBConfig.password,
                        host=DBConfig.host,
                        database=DBConfig.database)

        cursor = connection.cursor()

        for container in self.containers_manager.containers:
            container_ids = container.get_students_id()
            # print(f'Inserting container {container.containerid} with ids {container_ids}')
            for student_id in container_ids:
                query = f"INSERT INTO classi_composte (`groupid`, `configid`, `studentid`, `classid`) VALUES ({self.group_id}, {self.config_id}, {student_id}, {container.containerid})"
                cursor.execute(query)
                connection.commit()

        cursor.close()

        connection.close()

    def is_already_generated(self):
        connection = mysql.connector.connect(
                        user=DBConfig.user,
                        password=DBConfig.password,
                        host=DBConfig.host,
                        database=DBConfig.database)

        cursor = connection.cursor()

        query = f"SELECT COUNT(*) FROM classi_composte WHERE groupid = {self.group_id} AND configid = {self.config_id}"

        cursor.execute(query)

        num_of_students_already_inserted = cursor.fetchall()[0][0]

        cursor.close()

        connection.close()

        return num_of_students_already_inserted > 0



def create_cc_instance(process_id, group_id, config_id):
    cc = CC(process_id, group_id, config_id)
    result_value = cc.run()
    if result_value == True:
        good_status_json = {
            "querystatus" : "good",
            "message" : "Composizione Classi completata!"
        }

        return json.dumps(good_status_json)
    elif result_value == "ZeroStudentsIntoGroup":
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Gruppo vuoto, non e' possibile generare alcuna configurazione!"
        }
        return json.dumps(bad_status_json)
    elif result_value == "CCAlreadyGenerated":
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Composizione Classi già generata per questo gruppo e configurazione!"
        }
        return json.dumps(bad_status_json)
    elif result_value == "NoGroupOrConfigSelected":
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Nessun gruppo e/o configurazione selezionato/a!"
        }
        return json.dumps(bad_status_json)
    elif result_value == "CannotShuffleStudents":
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Impossibile distribuire gli studenti con questa configurazione!"
        }
        return json.dumps(bad_status_json)
    elif result_value == "TooManySexPrioritizedPeople":
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Troppi utenti con priorità di sesso per questa richiesta!"
        }
        return json.dumps(bad_status_json)
    elif result_value == "StudentsNotInsertedAfterShuffling":
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Inserimento degli studenti tramite shuffling non possibile!"
        }
        return json.dumps(bad_status_json)
    else:
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Errore nella Composizione Classi! Contattare l'amministratore."
        }
        return json.dumps(bad_status_json)
