"""State to manage all CLI inputs."""

__all__ = ["state"]


class State:
    def __init__(self):
        self.dry_run = False
        self.debug = False


state = State()
