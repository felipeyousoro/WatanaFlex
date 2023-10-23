SLASH_CHARS = ['\'', '\"', '\\', '[', ']', '(', ')', '^', '$', '?', '*', '+', '.', '|', '{', '}']


def get_transition_from_slash(char: str) -> str:
    if char in SLASH_CHARS:
        return char
    if char == 't':
        return '\t'
    elif char == 'n':
        return '\n'
    elif char == 'r':
        return '\r'
    raise Exception(f'Invalid slash character: {char}')


def get_transitions_from_brackets(brackets: str) -> list[str]:
    transitions: list[str] = []

    # if brackets[1] == '^':
    #     for i in range(ord(brackets[2]), ord(brackets[4]) + 1):
    #         transitions.append(chr(i))

    i = 0
    while i < len(brackets):
        char = brackets[i]
        if char == '^' and i == 0:
            i += 1
            continue
        if char != '\\':
            # If there is a '-' after the current char, then it is a range
            if i + 1 < len(brackets) and brackets[i + 1] == '-':
                for j in range(ord(char), ord(brackets[i + 2]) + 1):
                    transitions.append(chr(j))
                i += 2
            else:
                transitions.append(char)
        else:
            transitions.append(get_transition_from_slash(brackets[i + 1]))
            i += 1
        i += 1

    if brackets[0] == '^':
        transitions = [chr(i) for i in range(256) if chr(i) not in transitions]

    return transitions
