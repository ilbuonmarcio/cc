import random

with open("spaggiari_output.csv", 'r') as input_file:
    input_array = []
    for line in input_file:
        input_array.append(line.split(';'))

        # NULL, 1, 2, AUTOINC, 0, NULL, 4, 3, 9, 10, NULL, NULL, NULL, NULL, NULL, 8, RANDOM, TEST_GROUPID

with open("spaggiari_output_elab.csv", 'w') as output_file:
    i = 1
    for line in input_array:
        record = [
            'NULL',
            line[1],
            line[2],
            i,
            line[0],
            'NULL',
            line[4],
            line[3],
            line[9],
            line[10],
            'NULL',
            'NULL',
            'NULL',
            'NULL',
            'NULL',
            line[8],
            random.randint(6, 10),
            1
        ]
        print(i, record, end="\n\n")

        for column in record:
            output_file.write(str(column) + ";")

        output_file.write("\n")

        i+= 1
