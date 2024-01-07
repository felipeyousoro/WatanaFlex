import sys
import os

from Automata import automata as atmt
from RegexParser import regex_parser as rp

if __name__ == '__main__':
    file = open(os.path.join(sys.path[0], "regex.wfx"), "r")

    lines_list = []
    for line in file:
        regex = " ".join(line.split(" ")[:-1])
        token = line.split(" ")[-1].strip("\n").strip("\t")
        lines_list.append([regex, token])

    regex_parser = rp.RegexParser()
    groups = []

    for line in lines_list:
        regex_parser.set_regex(line[0])
        groups.append(regex_parser.get_groups())

    automaton = atmt.Automata()
    for i in range(len(groups)):
        automaton.add_expression(groups[i], lines_list[i][1])

    # print(tables[1])
    # print(tables[2])

    # build a .c file for the automata with C code
    automaton = automaton.convert_nfa_to_dfa()
    tables = automaton.get_automata()

    file = open(os.path.join(sys.path[0], "automata.c"), "w")

    file.write('/*\n/\tEste arquivo foi gerado pelo software Watanaflex,\n')
    file.write('/\t\tescrito por Felipe Dias Abrahao (Felipe Yousoro)\n')
    file.write('/\t\thttps://github.com/felipeyousoro/WatanaFlex/\n*/\n\n')

    file.write('int TRANSITIONS_TABLE[][256] = {\n')
    for i in range(len(tables[0])):
        file.write('\t{')
        for j in range(len(tables[0][i])):
            file.write(str(tables[0][i][j]))
            if j != len(tables[0][i]) - 1:
                file.write(', ')

        file.write('}')
        if i != len(tables[0]) - 1:
            file.write(',')
        file.write('\n')

    file.write('};\n\n')

    file.write('int FINAL_STATES_TABLE[] = {\n')
    for i in range(len(tables[1])):
        if tables[1][i] == True:
            file.write('\t1')
        else:
            file.write('\t0')
        if i != len(tables[1]) - 1:
            file.write(',')
        file.write('\n')

    file.write('};\n\n')

    file.write('enum TOKENS_TABLE {\n')
    for i in range(len(tables[2])):
        file.write('\t' + str(tables[2][i]))
        if i != len(tables[2]) - 1:
            file.write(',')
        file.write('\n')

    file.write('};\n\n')

    file.write('int STATES_TOKENS_TABLE[] = {\n')
    for i in range(len(tables[3])):
        file.write('\t' + str(tables[3][i]))
        if i != len(tables[3]) - 1:
            file.write(',')
        file.write('\n')

    file.write('};\n\n')

    file.close()
