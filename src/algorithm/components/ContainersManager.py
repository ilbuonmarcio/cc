import math
import random
from .ClassContainer import ClassContainer

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
