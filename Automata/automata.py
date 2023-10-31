import time

from .State import state as st
from . import build_transitions as btrn
from . import build_tables as btbl


class Automata:
    def __init__(self):
        self.states: list[st.State] = []
        self.states.append(st.State(0, False))
        self.states.append(st.State(1, False))

        self.no_states: int = 2
        self.deterministic: bool = True

    def add_state(self, is_final: bool = False, token: str = None) -> st.State:
        self.states.append(st.State(self.no_states, is_final, token))
        self.no_states += 1

        return self.states[-1]

    def get_automata(self) -> tuple[list[list[int]], list[bool], list[str], list[str]]:
        if not self.deterministic:
            raise Exception("Automata is not deterministic")
        tokens, state_tokens = btbl.build_tokens_table(self.states)
        return btbl.build_transition_table(self.states), btbl.build_final_states_table(
            self.states), tokens, state_tokens

    def add_expression(self, regex_groups: list, token: str) -> None:
        current_state: int = self.states[1].name

        no_groups: int = len(regex_groups)

        new_states: list[st.State] = [st.State(i + self.no_states, False) for i in range(no_groups)]
        self.no_states += no_groups

        for i in range(0, no_groups, 1):
            group: list = regex_groups[i]
            transitions: list[str] = []

            # Parenthesis case, will be handled later
            if group[2] == True:
                break

            if group[0][0] == '[':
                transitions = btrn.get_transitions_from_brackets(group[0][1:-1])
            elif group[0][0] == '.':
                transitions = [chr(i) for i in range(256)]
            elif group[0][0] == '\\':
                transitions.append(btrn.get_transition_from_slash(group[0][1]))
            else:
                transitions.append(group[0])

            #print group and transitions
            self.states.append(new_states[i])
            self.states[current_state].add_transitions(transitions, new_states[i])

            if(group[1] == '*'):
                loop_state = new_states[i]
                new_states[i].add_transitions(transitions, loop_state)

            current_state = new_states[i].name

        new_states[-1].is_final = True
        new_states[-1].token = token

        for i in range(no_groups - 1, 0, -1):
            if new_states[i].is_final and regex_groups[i][1] == '*':
                new_states[i - 1].is_final = True
                new_states[i - 1].token = token

        for i in range(no_groups - 1, 0, -1):
            if regex_groups[i][1] == '*':
                new_states[i - 1].extend_transitions(new_states[i])

        if regex_groups[0][1] == '*':
            self.states[1].is_final = new_states[1].is_final
            self.states[1].token = new_states[1].token
            self.states[1].extend_transitions(new_states[1])

        self.check_automata_deterministic()

    def check_automata_deterministic(self):
        # print('Checking automata determinism')
        for state in self.states:
            if not state.deterministic:
                # print(f'\tAutomata is not deterministic, interrupting')
                self.deterministic = False
                return

        # print('\tAutomata is deterministic')
        self.deterministic = True

    def print_all_states(self):
        for state in self.states:
            print(f'{state.name}\n')
            for transition in state.transitions:
                if(transition[0] != '\n' and transition[0] != '\r' and transition[0] != '\t' and transition[0] != ' '):
                    print(f'\t{transition[0]} -> {transition[1].name}\n')



    def convert_nfa_to_dfa(self):
        # self.check_automata_deterministic()
        # if self.deterministic:
        #     print('Already deterministic')
        #     return self

        new_automata: Automata = Automata()

        full_transition_table: list[list[list[int]]] = []
        full_tokens_table: list[str] = []
        full_finals_table: list[bool] = []

        for i in range(0, self.no_states):
            full_transition_table.append([[] for i in range(256)])
            for transition in self.states[i].transitions:
                trn_char = transition[0]
                trn_name = transition[1].name
                full_transition_table[i][ord(trn_char)].append(trn_name)

            full_tokens_table.append(self.states[i].token)
            full_finals_table.append(self.states[i].is_final)

        total_states: int = self.no_states

        dict_states: dict[str, int] = {}
        for i in range(0, total_states):
            dict_states[str(self.states[i].name)] = i

        # print('\t', end='')
        # for i in range(97, len(full_transition_table[0])):
        #     print(chr(i), end='\t')
        #
        # for i in range(0, total_states):
        #     print('\n')
        #     print(i, end='\t')
        #     for j in range(97, len(full_transition_table[i])):
        #         print(full_transition_table[i][j], end="\t")
        # print('\n')

        #print('Total de estados: ', total_states)
        i: int = 0
        while i < total_states:
            for j in range(0, len(full_transition_table[i])):
                # Checking if is not deterministic
                if len(full_transition_table[i][j]) > 1:
                    # If not, then we need to create the composed state
                    composed_state_name: str = ''
                    # Just saving in the dictionary the composed state
                    states = full_transition_table[i][j]
                    #print(states)
                    composed_state_name = str(states)
                    if composed_state_name in dict_states:
                        #print('contido: ', composed_state_name)
                        full_transition_table[i][j] = [dict_states[composed_state_name]]
                        continue

                    dict_states[composed_state_name] = total_states
                    total_states += 1
                    print('Novo estado: ', composed_state_name, ' -> ', dict_states[composed_state_name], ' valor: ', ord(chr(j)))

                    # Adding the transition to the new automata
                    full_transition_table.append([[] for i in range(len(full_transition_table[0]))])
                    full_finals_table.append(False)

                    for state in states:
                        if full_finals_table[state]:
                            full_finals_table[dict_states[composed_state_name]] = True
                            full_tokens_table[dict_states[composed_state_name]] = full_tokens_table[state]
                            break

                    # Changing the transition to the composed state
                    full_transition_table[i][j] = [dict_states[composed_state_name]]
                    # The composed state transitions are the same as the transitions of the states that compose it
                    for state in states:
                        for k in range(0, len(full_transition_table[state])):
                            for state_to in full_transition_table[state][k]:
                                full_transition_table[dict_states[composed_state_name]][k].append(state_to)

            i += 1

        # print('\t', end='')
        # for i in range(97, len(full_transition_table[0])):
        #     print(chr(i), end='\t')
        #
        # for i in range(0, total_states):
        #     print('\n')
        #     print(i, end='\t')
        #     for j in range(97, len(full_transition_table[i])):
        #         print(full_transition_table[i][j], end="\t")
        # print('\n')

        # for key in dict_states:
        #     print(f'{key} -> {dict_states[key]}')

        # new_automata.check_automata_deterministic()
        # if new_automata.deterministic:
        #     print('Now deterministic')
        #     return new_automata

        return self.array_to_automata(full_transition_table, full_tokens_table, full_finals_table)

    def array_to_automata(self, transitions: list[list[list[int]]], tokens: list[str], finals: list[bool]):
        #print('Convertendo')
        new_automata: Automata = Automata()

        total = len(transitions)

        new_automata.states[1].token = tokens[1]
        new_automata.states[1].is_final = finals[1]
        for i in range(2, total):
            new_automata.add_state(finals[i], tokens[i])

        for i in range(0, total):
            #print(i)
            for j in range(0, 256):
                if len(transitions[i][j]) > 1:
                    raise Exception('O QUE A FODA?!')
                if len(transitions[i][j]) > 0:
                    new_automata.states[i].add_transitions([chr(j)], new_automata.states[transitions[i][j][0]])

        return new_automata
