import time

from . import regex_lexer as rl
class RegexParser:
    def __init__(self, regex: str = ''):
        self.current_index: int = 0
        self.regex_lexer: rl.RegexLexer = rl.RegexLexer(regex)
        self.tokens: list[str] = []

    def __del__(self):
        pass

    def set_regex(self, regex: str) -> None:
        self.regex_lexer.set_regex(regex)

    # Format is the token string and the post token value
    # 0 nothing
    # 1 plus
    # 2 star
    # 3 question
    def get_next_group(self) -> [str, str]:
        group: str = ''
        post_token: str = ''

        # Char
        if self.tokens[self.current_index][0] == 1:
            group += self.tokens[self.current_index][1]
            self.current_index += 1

            post_token = self.eat_post_token()

        # Backslash
        elif self.tokens[self.current_index][0] == 3:
            group += self.tokens[self.current_index][1]
            self.current_index += 1

            post_token = self.eat_post_token()

        # # Caret
        # elif self.tokens[self.current_index][0] == 5:
        #     group += self.tokens[self.current_index][1]
        #     self.current_index += 1

        # Left square brack
        elif self.tokens[self.current_index][0] == 7:
            group += self.tokens[self.current_index][1]
            self.current_index += 1
            while self.tokens[self.current_index][0] != 8:
                group += self.tokens[self.current_index][1]
                self.current_index += 1

            group += self.tokens[self.current_index][1]
            self.current_index += 1

            post_token = self.eat_post_token()

        # Left parenthesis
        elif self.tokens[self.current_index][0] == 9:
            group += self.tokens[self.current_index][1]
            self.current_index += 1
            while self.tokens[self.current_index][0] != 10:
                next_group = self.get_next_group()
                group += next_group[0] + next_group[1]

            group += self.tokens[self.current_index][1]
            self.current_index += 1

            post_token = self.eat_post_token()

        # Dot
        elif self.tokens[self.current_index][0] == 14:
            group += self.tokens[self.current_index][1]
            self.current_index += 1

            post_token = self.eat_post_token()

        # # Left curly brack
        # elif self.tokens[self.current_index][0] == 19:

        return [group, post_token]

    def eat_post_token(self) -> str:

        if self.current_index >= len(self.tokens):
            return ''

        # Plus
        if self.tokens[self.current_index][0] == 12:
            self.current_index += 1
            return '+'

        # Star
        elif self.tokens[self.current_index][0] == 13:
            self.current_index += 1
            return '*'

        # Question
        elif self.tokens[self.current_index][0] == 11:
            self.current_index += 1
            return '?'

        return ''

    def get_groups(self) -> list:
        self.current_index = 0
        self.tokens = self.regex_lexer.get_tokens()

        groups: list = []
        while self.current_index < len(self.tokens):
            groups.append(self.get_next_group())

        # if any group has '+', split it into two groups,
        # one normal without the '+', and one with *
        while any('+' in group[1] for group in groups):
            for i in range(len(groups)):
                if '+' in groups[i][1]:
                    groups[i][1] = groups[i][1].replace('+', '')
                    groups.insert(i+1, [groups[i][0], '*'])
                    break

        for i in range(len(groups)):
            if groups[i][0][0] == '(':
                groups[i].append(True)
                groups[i][0] = groups[i][0][1:-1]
                parser = RegexParser(groups[i][0])
                groups[i][0] = parser.get_groups()
            else:
                groups[i].append(False)

        return groups


