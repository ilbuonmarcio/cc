import math
import copy
import random
from .ClassContainer import ClassContainer

class ContainersManager:

    def __init__(self, num_of_containers, configuration, students_manager):
        self.containers = [ClassContainer(configuration, containerid) for containerid in range(1, num_of_containers+1)]
        self.configuration = configuration
        self.students_manager = students_manager

    def print_all_containers_current_dimensions(self):
        for container in self.containers:
            print(container)

    def get_number_of_containers(self):
        return len(self.containers)

    def get_std(self):
        containers_avg = self.get_avg()
        return math.sqrt(sum([math.pow(container.marks_avg - containers_avg, 2) for container in self.containers]) / len(self.containers))

    def get_avg(self):
        return sum([container.marks_avg for container in self.containers]) / len(self.containers)

    def get_number_of_total_students_into_containers(self):
        return sum([len(container.students) for container in self.containers])

    def get_all_inserted_students_matricola(self):
        result_set = []
        for container in self.containers:
            for student in container.students:
                result_set.append(student.matricola)

        return set(result_set)

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
                        print("Warning! Students to reinsert found!")
                        for student in students_not_inserted:
                            print("- Student to reinsert: [" + student.matricola + "]")
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
                    print('Trying to add students [' + students_array[0].matricola + ', ' + students_array[1].matricola + '] ...')
                    container_to_fill.add_students(students_array)
                    break

        print("Finished distributing O-O couples randomly into containers!")

        return students_to_reinsert

    def distribute_remaining_students_randomly_into_containers(self, input_array):
        print("Distributing remaining students [" + str(len(input_array)) + "] randomly into containers...")

        remaining_students = len(input_array)

        students_to_remove_from_students_manager = []

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
                            students_to_remove_from_students_manager.append(student)
                            remaining_students -= 1
                            break
                    else:
                        containers_already_filled.append(container_to_fill)
                else:
                    print("Cannot fill this student [" + student.matricola + "]! Need shuffle!")
                    students_to_reinsert.append(student)
                    break
        print("\nFinished distributing remaining students randomly into containers!")

        for student in students_to_remove_from_students_manager:
            self.students_manager.students.remove(student)

        return students_to_reinsert

    def rebalance_students_to_reach_minimum_number_of_students_per_container(self):
        print("Rebalancing students to reach minimum number of students per container...")

        rebalancing_cycles_left = 10000
        while rebalancing_cycles_left > 0:
            containers_to_rebalance = [container for container in self.containers if not container.minned_out]
            containers_already_balanced = [container for container in self.containers if container.minned_out]
            if len(containers_to_rebalance) == 0:
                break

            # print(f"{rebalancing_cycles_left}\tbalanced: {len(containers_already_balanced)}\tunbalanced: {len(containers_to_rebalance)}")

            for container in containers_to_rebalance:

                attempts_left = 50
                while attempts_left > 0:
                    if len(containers_already_balanced) == 0:
                        attempts_left = 0
                        break

                    possible_student_container = random.choice(containers_already_balanced)
                    possible_student_insert = possible_student_container.get_random_student()

                    student = container.add_student(possible_student_insert)
                    if student is None:
                        possible_student_container.remove_student(possible_student_insert)
                        break

            rebalancing_cycles_left -= 1

        print("Rebalancing done!")
        return len([container for container in self.containers if not container.minned_out]) == 0


    def get_two_random_containers(self):
        while True:
            first_container = random.choice(self.containers)
            second_container = random.choice(self.containers)
            if first_container is not second_container:
                break

        return first_container, second_container

    def fill_remaining_students_shuffling_classcontainers(self, input_array):
        print("\nDistributing remaining students shuffling classcontainers...")

        students_to_remove_from_students_manager = []

        students_to_insert = len(input_array)

        while students_to_insert > 0:

            remaining_attempts_before_trowing_message = 5000

            while remaining_attempts_before_trowing_message > 0:

                first_container, second_container = self.get_two_random_containers()

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

                    if first_result == None and second_result == None:
                        if first_container.add_student(input_array[students_to_insert-1]) == None:
                            print("Student [" + input_array[students_to_insert-1].matricola + "] inserted with shuffling!")
                            students_to_remove_from_students_manager.append(input_array[students_to_insert-1])
                            input_array.remove(input_array[students_to_insert-1])
                            students_to_insert -= 1
                            break

                        elif second_container.add_student(input_array[students_to_insert-1]) == None:
                            print("Student [" + input_array[students_to_insert-1].matricola + "] inserted with shuffling!")
                            students_to_remove_from_students_manager.append(input_array[students_to_insert-1])
                            input_array.remove(input_array[students_to_insert-1])
                            students_to_insert -= 1
                            break

                    else:
                        first_container.remove_student(second_container_student)
                        second_container.remove_student(first_container_student)

                        first_result = first_container.add_student(first_container_student_copy)
                        second_result = second_container.add_student(second_container_student_copy)
                
                remaining_attempts_before_trowing_message -= 1
                
            if remaining_attempts_before_trowing_message == 0:
                return False

        for student in students_to_remove_from_students_manager:
            self.students_manager.students.remove(student)

        print("Distributing remaining students shuffling classcontainers done!")

        return True


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
