import random

lines_to_write = []
with open('last_year.csv', 'r') as input_file:

    for line in input_file:
        line = line.split(';')
        output_record = ""
        for i in range(0, 12):
            output_record += line[i] + ";"

        output_record += f"{random.randint(1, 5)};"
        output_record += line[15]

        output_record += "\n"

        lines_to_write.append(output_record)

with open('last_year_UPLOAD.csv', 'w') as output_file:
    for line in lines_to_write:
        output_file.write(line)
