class Area():
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

class Vector2():
    """ A vector with an x-coordinate and a y-coordinate. """
    def __init__(self, x, y):
        self.x = x
        self.y = y

def get_slice(data, area):
    return data[area.y:area.y+area.dy,
                area.x:area.x+area.dx]

