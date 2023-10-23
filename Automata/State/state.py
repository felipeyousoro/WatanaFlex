class State:

    def __init__(self, name: int, is_final: bool = False, token: str = None):
        if name < 0:
            raise ValueError("State name must be a positive integer")

        self.name: int = name
        self.is_final: bool = is_final
        self.token: str = token
        self.transitions: list[str, State] = []
        self.deterministic: bool = True

    def add_transitions(self, transitions: list[str], to):
        for t in transitions:
            flag = True
            for transition in self.transitions:
                if t == transition[0]:
                    # Transition already exists and goes to different state
                    if transition[1].name != to.name:
                        self.deterministic = False
                    else:
                        flag = False
            if flag:
                self.transitions.append([t, to])

    def extend_transitions(self, _from):
        for transition in _from.transitions:
            self.add_transitions([transition[0]], transition[1])
