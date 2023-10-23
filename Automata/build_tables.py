def build_transition_table(states) -> list[list[int]]:
    transitions: list[list[int]] = []

    POSSIBLE_TRANSITIONS: int = 256

    for state in states:
        transitions.append([-1 for _ in range(POSSIBLE_TRANSITIONS)])
        for transition in state.transitions:
            transitions[state.name][ord(transition[0])] = transition[1].name

    return transitions

def build_final_states_table(states) -> list[bool]:
    final_states: list[bool] = []

    for state in states:
        final_states.append(state.is_final)

    return final_states

def build_tokens_table(states) -> [list[str], list[str]]:
    tokens: list[str] = []
    state_tokens: list[str] = []

    tokens.append('ERRO')

    for state in states:
        if state.token not in tokens:
            if state.token is not None:
                tokens.append(state.token)
        if state.token == None:
            state_tokens.append('ERRO')
        else:
            state_tokens.append(state.token)

    return [tokens, state_tokens]
