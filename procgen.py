from __future__ import annotations
from typing import Tuple, Iterator, List, TYPE_CHECKING

if TYPE_CHECKING:
    from entity import Entity

from game_map import GameMap
import tile_types
import tcod
import random


class RectangularRoom:
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x1 = x
        self.y1 = y
        self.x2 = x + width
        self.y2 = y + height

    @property
    def center(self) -> Tuple[int, int]:
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)

        return center_x, center_y

    @property
    def inner(self) -> Tuple[slice, slice]:
        return slice(self.x1 + 1, self.x2), slice(self.y1 + 1, self.y2)

    def intersects(self, other: RectangularRoom) -> bool:
        return (
                self.x1 <= other.x2
                and self.x2 >= other.x1
                and self.y1 <= other.y2
                and self.y2 >= other.y1
        )


def tunnel_between(
        start: Tuple[int, int], end: Tuple[int, int]
) -> Iterator[Tuple[int, int]]:
    x1, y1 = start
    x2, y2 = end
    if random.random() < 0.5:  # 50% chance
        # Move horizontally, then vertically.
        corner_x, corner_y = x2, y1
    else:
        # Move vertically, then horizontally.
        corner_x, corner_y = x1, y2

    for x, y in tcod.los.bresenham((x1, y1), (corner_x, corner_y)).tolist():
        yield x, y
    for x, y in tcod.los.bresenham((corner_x, corner_y), (x2, y2)).tolist():
        yield x, y

def generate_dungeon(
    max_rooms: int,
    room_min_size: int,
    room_max_size: int,
    map_width: int,
    map_height: int,
    player: Entity,
) -> GameMap:
    dungeon = GameMap(map_width, map_height)
    rooms: List[RectangularRoom] = []

    for _ in range(max_rooms):
        new_room = create_room(dungeon, room_min_size, room_max_size)

        if not is_room_valid(new_room, rooms):
            continue

        add_room_to_dungeon(dungeon, new_room)

        if not rooms:
            place_player(player, new_room)
        else:
            connect_rooms(dungeon, rooms[-1], new_room)

        rooms.append(new_room)

    return dungeon

def create_room(dungeon: GameMap, room_min_size: int, room_max_size: int) -> RectangularRoom:
    room_width = random.randint(room_min_size, room_max_size)
    room_height = random.randint(room_min_size, room_max_size)
    x = random.randint(0, dungeon.width - room_width - 1)
    y = random.randint(0, dungeon.height - room_height - 1)
    return RectangularRoom(x, y, room_width, room_height)


def is_room_valid(new_room: RectangularRoom, rooms: List[RectangularRoom]) -> bool:
    return not any(new_room.intersects(other_room) for other_room in rooms)


def place_player(player: Entity, room: RectangularRoom) -> None:
    player.x, player.y = room.center


def connect_rooms(dungeon: GameMap, room1: RectangularRoom, room2: RectangularRoom) -> None:
    for x, y in tunnel_between(room1.center, room2.center):
        dungeon.tiles[x, y] = tile_types.floor


def add_room_to_dungeon(dungeon: GameMap, room: RectangularRoom) -> None:
    dungeon.tiles[room.inner] = tile_types.floor