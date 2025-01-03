from config import *
import random
from src.room import Room

class BSP:
    def __init__(self, x, y, width, height, rand):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room = None
        self.left_child = None
        self.right_child = None
        self.split_horizontal = False
        self.rand = rand

    def split(self, min_size):
        if self.width > self.height and self.width > min_size * 2:
            self.split_horizontal = False
            split_point = self.rand.randint(min_size, self.width - min_size)
            self.left_child = BSP(self.x, self.y, split_point, self.height, self.rand)
            self.right_child = BSP(self.x + split_point, self.y, self.width - split_point, self.height, self.rand)
            return True
        elif self.height > min_size * 2:
            self.split_horizontal = True
            split_point = self.rand.randint(min_size, self.height - min_size)
            self.left_child = BSP(self.x, self.y, self.width, split_point, self.rand)
            self.right_child = BSP(self.x, self.y + split_point, self.width, self.height - split_point, self.rand)
            return True
        return False

    def create_rooms(self, min_room_size):
        if self.left_child or self.right_child:
            if self.left_child:
                self.left_child.create_rooms(min_room_size)
            if self.right_child:
                self.right_child.create_rooms(min_room_size)
        else:
            min_size = max(min_room_size, CORRIDOR_WIDTH * 2)
            room_width = self.rand.randint(min_size, self.width - 2)
            room_height = self.rand.randint(min_size, self.height - 2)
            room_x = self.x + self.rand.randint(1, self.width - room_width - 1)
            room_y = self.y + self.rand.randint(1, self.height - room_height - 1)
            self.room = Room(room_x, room_y, room_width, room_height)

    def get_rooms(self):
        rooms = []
        if self.room:
            rooms.append(self.room)
        if self.left_child:
            rooms.extend(self.left_child.get_rooms())
        if self.right_child:
            rooms.extend(self.right_child.get_rooms())
        return rooms


class DungeonGenerator:
    def __init__(self, width, height, min_size, min_room_size, seed=None):
        self.width = width
        self.height = height
        self.min_size = max(min_size, CORRIDOR_WIDTH * 2)
        self.min_room_size = max(min_room_size, CORRIDOR_WIDTH * 2)
        self.seed = seed if seed is not None else random.randint(0, 999999999)
        self.rand = random.Random(self.seed)
        self.tilemap = [[BACKGROUND for _ in range(width)] for _ in range(height)]
        self.root = BSP(0, 0, width, height, self.rand)
        self.rooms = []

    def generate_dungeon(self):
        nodes = [self.root]
        while nodes:
            node = nodes.pop(0)
            if node.split(self.min_size):
                nodes.append(node.left_child)
                nodes.append(node.right_child)

        self.root.create_rooms(self.min_room_size)
        self.rooms = self.root.get_rooms()

        self._apply_rooms()
        self._connect_rooms()
        self._finalize_tilemap()

        return self.tilemap, self.rooms, self.root, self.seed

    def _apply_rooms(self):
        def apply_rooms(node):
            if node.room:
                node.room.apply_to_map(self.tilemap)
            if node.left_child:
                apply_rooms(node.left_child)
            if node.right_child:
                apply_rooms(node.right_child)

        apply_rooms(self.root)

    def _connect_rooms(self):
        self._connect_nodes(self.root)

    def _connect_nodes(self, node):
        if node.left_child and node.right_child:
            left_center = self._get_room_center(node.left_child)
            right_center = self._get_room_center(node.right_child)
            if left_center and right_center:
                self._create_corridor(left_center, right_center)
            self._connect_nodes(node.left_child)
            self._connect_nodes(node.right_child)

    def _get_room_center(self, node):
        if node.room:
            return node.room.center
        elif node.left_child:
            return self._get_room_center(node.left_child)
        elif node.right_child:
            return self._get_room_center(node.right_child)
        return None

    def _create_corridor(self, start, end):
        x1, y1 = start
        x2, y2 = end
        offset = CORRIDOR_WIDTH // 2

        for x in range(min(x1, x2), max(x1, x2) + 1):
            for y_offset in range(-offset, offset + 1):
                y = y1 + y_offset
                if self._is_within_bounds(x, y):
                    self.tilemap[y][x] = FLOOR

        for y in range(min(y1, y2), max(y1, y2) + 1):
            for x_offset in range(-offset, offset + 1):
                x = x2 + x_offset
                if self._is_within_bounds(x, y):
                    self.tilemap[y][x] = FLOOR

    def _is_within_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def _finalize_tilemap(self):
        self.tilemap = [
            [
                self._determine_wall_type(x, y)
                if self.tilemap[y][x] != FLOOR
                else FLOOR
                for x in range(self.width)
            ]
            for y in range(self.height)
        ]

    def _determine_wall_type(self, x, y):
        if self.tilemap[y][x] == FLOOR:
            return FLOOR

        return WALL_CENTER if self._should_be_wall(x, y) else BACKGROUND

    def _should_be_wall(self, x, y):
        if not self._is_within_bounds(x, y) or self.tilemap[y][x] == FLOOR:
            return False

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if self._is_within_bounds(nx, ny) and self.tilemap[ny][nx] == FLOOR:
                    return True
        return False