from config import MAP_WIDTH, MAP_HEIGHT, FLOOR

class Room:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.center = (x + width // 2, y + height // 2)

    def apply_to_map(self, tilemap):
        for y in range(self.y, self.y + self.height):
            for x in range(self.x, self.x + self.width):
                tilemap[y][x] = FLOOR


