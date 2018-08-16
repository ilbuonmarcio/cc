import math
import random
import copy

class ClassContainer:

    def __init__(self, configuration, containerid):
        self.containerid = containerid
        self.db_group_configuration = configuration
        self.num_students = 0
        self.num_girls = 0
        self.num_boys = 0
        self.num_104 = 0
        self.num_107 = 0
        self.caps = {}
        self.nationalities = {}
        self.students = []
        self.maxed_out = False
        self.minned_out = False
        self.has_legge_104 = False
        self.marks_avg = 6

    def __str__(self):
        return "ContainerID: " + str(self.containerid) + " - Num of students: " + str(len(self.students))

    def get_students_id(self):
        students_id = []
        for student in self.students:
            students_id.append(str(student.id))
        return students_id

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

        # print(f"Adding student with matricola [{student.matricola}]...")

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

        if student.legge_104 == "s" and self.num_students -1 < 20 and self.has_legge_104 is False:
            # print("Changed group type to legge_104 viable")
            self.db_group_configuration.max_students = 20
            self.has_legge_104 = True

        if student.legge_104 == "s" and self.has_legge_104 is True:
            # print("Reached max number of legge_104 in this container!")
            return student

        if self.num_students >= self.db_group_configuration.max_students:
            self.maxed_out = True
            # print(f"Reached max number of students [{self.num_students}] in this container!")
            return student

        self.students.append(student)

        # print(f"Student [{student.matricola}] inserted!")

        self.refresh_statistics()

    def remove_student(self, student):
        self.refresh_statistics()
        for s in self.students:
            if s.matricola == student.matricola:
                self.students.remove(s)
                self.refresh_statistics()
                return

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

        self.minned_out = len(self.students) >= self.db_group_configuration.min_students

    def show_container_statistics(self):
        print("\n[*] Showing container statistics...")
        for attribute, value in self.__dict__.items():
            if attribute == "students":
                print(attribute, [student.matricola for student in self.students])
            else:
                print(attribute, value)

        print("[*] End of container statistics")
