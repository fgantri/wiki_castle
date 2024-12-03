class Castle:

    def __init__(self):
        self._first_room = None
        self._current_room = None

    @property
    def current_room(self):
        return self._current_room

    def add_room(self, room):
        if self._first_room is None:
            self._first_room = room

        current = self._first_room
        while current.next_room is not None:
            current = current.next_room

        current.next_room = room



    def play(self):
        self._current_room = self._first_room
        self.current_room.run()
