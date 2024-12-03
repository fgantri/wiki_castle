class AsciiSprite:

    def __init__(self, path):
        self._lines = []
        self._width = 0
        self._height = 0
        with open(path, "r") as f:
            lines = f.readlines()
            self._height = len(lines)
            for line in lines:
                if len(line) > self._width:
                    self._width = len(line)
                self._lines.append(line)

    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @property
    def lines(self):
        return self._lines

    def add_left_margin(self, units):
        for i in range(self._height):
            self._lines[i] = " " * units + self._lines[i]

    def __str__(self):
        out = ""
        for line in self._lines:
            out += line
        return out


class Text(AsciiSprite):
    pass