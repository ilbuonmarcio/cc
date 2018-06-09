import random
import math
import time
import mysql.connector
import copy
import json

from components.DBConfig import DBConfig
from components.Configuration import Configuration
from components.StudentsManager import StudentsManager
from components.ContainersManager import ContainersManager


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
    else:
        bad_status_json = {
            "querystatus" : "bad",
            "message" : "Errore nella Composizione Classi! Contattare l'amministratore."
        }
        return json.dumps(bad_status_json)


class CC:

    def __init__(self, process_id, group_id, config_id):
        self.process_id = process_id
        self.group_id = group_id
        self.config_id = config_id
        self.students_manager = StudentsManager(self.group_id)
        self.configuration = Configuration(self.config_id)
        self.containers_manager = ContainersManager(
            math.ceil(self.students_manager.get_number_of_students() / self.configuration.max_students + 1),
            self.configuration
        )

    def run(self):
        print("Running CC...")

        self.total_number_of_students = self.students_manager.get_number_of_students()

        if self.total_number_of_students == 0:
            return "ZeroStudentsIntoGroup"

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

        return True

    def optimize(self):

        def _get_two_random_containers():
            while True:
                first_container = random.choice(self.containers_manager.containers)
                second_container = random.choice(self.containers_manager.containers)
                if first_container is not second_container:
                    break

            return first_container, second_container

        def _get_std_of_two_containers(first_container, second_container):
            first_container_avg = first_container.get_avg()
            second_container_avg = second_container.get_avg()

            containers_avg = (first_container_avg + second_container_avg) / 2

            return math.sqrt(
                (
                    math.pow(first_container_avg - containers_avg, 2) +
                    math.pow(second_container_avg - containers_avg, 2)
                ) / 2)

        def _optimize_random_couple_of_containers_fixed_cycles(num_of_cycles):
            first_container_copied, second_container_copied = _get_two_random_containers()

            previous_swap_std = _get_std_of_two_containers(first_container_copied, second_container_copied)

            for _ in range(num_of_cycles):

                first_container_student = first_container_copied.get_random_student()
                second_container_student = second_container_copied.get_random_student()

                if first_container_student.eligible_to_swap(self.configuration.sex_priority) \
                and second_container_student.eligible_to_swap(self.configuration.sex_priority) \
                and not first_container_copied.has_desiderata(first_container_student) \
                and not second_container_copied.has_desiderata(second_container_student):


                    first_container_copied.remove_student(first_container_student)
                    second_container_copied.remove_student(second_container_student)

                    first_result = first_container_copied.add_student(second_container_student)
                    second_result = second_container_copied.add_student(first_container_student)

                    after_swap_std =  _get_std_of_two_containers(first_container_copied, second_container_copied)

                    if first_result is None and second_result is None:
                        if after_swap_std >= previous_swap_std:
                            first_container_copied.remove_student(second_container_student)
                            second_container_copied.remove_student(first_container_student)

                            first_result = first_container_copied.add_student(first_container_student)
                            second_result = second_container_copied.add_student(second_container_student)
                            return 0
                        else:
                            return 1

                return 0


        print("Optimizing...")

        num_of_optimizations = min([15000, self.total_number_of_students**2])
        num_of_effective_optimizations = 0
        for i in range(0, num_of_optimizations):
            if i % 250 == 0:
                print(f"{round(i / num_of_optimizations * 100, 2)}%\t\t{i} \toptcycle")
            num_of_effective_optimizations += _optimize_random_couple_of_containers_fixed_cycles(25)

        print(f"Effective swaps done: {num_of_effective_optimizations}")

    def upload_students_to_db(self):
        pass
