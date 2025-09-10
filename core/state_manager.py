# Gerencia os estados (menu, tutorial, fases, etc.)

class StateManager:
    def __init__(self):
        self.states = {}
        self.current_state = None

    def add_state(self, name, state):
        self.states[name] = state

    def set_state(self, name):
        self.current_state = self.states[name]

    def handle_events(self, events):
        if self.current_state:
            self.current_state.handle_events(events)

    def update(self):
        if self.current_state:
            self.current_state.update()

    def draw(self, screen):
        if self.current_state:
            self.current_state.draw(screen)
