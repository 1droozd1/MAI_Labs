file = open("my_tree.ged", "r", encoding='utf-8')
relative = {}

for string in file.readlines():

    if string.find('INDI') != -1:
        ID = string.split(' ')[1].rstrip()
    elif (string.find('GIVN')) != -1:
        name_and_surname = string.split(' ')[2].rstrip()
    elif string.find('SURN') != -1:
        name_and_surname = name_and_surname + ' ' + string.split(' ')[2].rstrip()
    elif string.find('SEX') != -1:
        if string.split(' ')[2].rstrip() == 'F':
            relative[ID] = [name_and_surname, '-1', '-1', 'female']
        else:
            relative[ID] = [name_and_surname, '-1', '-1', 'male']

    if string.find('HUSB') != -1:
        father = relative[string.split(' ')[2].rstrip()][0]
    elif string.find('WIFE') != -1:
        mother = relative[string.split(' ')[2].rstrip()][0]
    elif string.find('CHIL') != -1:
        relative[string.split(' ')[2].rstrip()][1] = father
        relative[string.split(' ')[2].rstrip()][2] = mother

file.close()

outfile = open("my_tree.pl", "w")

for i in relative:
    if relative[i][1] != '-1':
        outfile.write("child('" + relative[i][0] + "','" + relative[i][1] + "').\n")
    if relative[i][2] != '-1':
        outfile.write("child('" + relative[i][0] + "','" + relative[i][2] + "').\n")

for i in relative:
    if relative[i][3] == 'male':
        outfile.write(relative[i][3] + "('" + relative[i][0] + "').\n")

for i in relative:
    if relative[i][3] == 'female':
        outfile.write(relative[i][3] + "('" + relative[i][0] + "').\n")

outfile.close()