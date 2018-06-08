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
