from . import expression_tables as et


class RegexLexer:
    def __init__(self, regex: str = ''):
        self.current_index: int = 0
        self.regex: str = regex

    def __del__(self):
        pass

    def set_regex(self, regex: str) -> None:
        self.regex = regex

    def get_next_token(self) -> [int, str]:
        last_final_state: int = 0
        last_final_state_index: int = self.current_index
        current_state: int = 0

        for i in range(self.current_index, len(self.regex)):
            next_state: int = et.TRANSITION_TABLE[current_state][et.CHAR_INDEX_MAP[self.regex[i]]]

            if next_state != -1 and et.STATES_TABLE[next_state] == True:
                last_final_state = next_state
                last_final_state_index = i

            if next_state == -1:
                token_content: str = self.regex[self.current_index: i]
                self.current_index = last_final_state_index + 1
                return [last_final_state, token_content]

            current_state = next_state

        token_content: str = self.regex[self.current_index: len(self.regex)]
        self.current_index = last_final_state_index + 1

        return [last_final_state, token_content]

    def get_tokens(self) -> list[[int, str]]:
        self.current_index = 0

        tokens: list[[int, str]] = []

        while self.current_index < len(self.regex):
            tokens.append(self.get_next_token())

        return tokens
