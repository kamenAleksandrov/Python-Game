from __future__ import annotations #this speed up load times

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity

class Action:

    # this forces other extenders to implement their own perform
    def perform(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()

class EscapeAction(Action):

    def perform(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()
        self.dx = dx
        self.dy = dy

    def perform(self, engine: Engine, entity: Entity)-> None:
        destination_x = entity.x + self.dx
        destination_y = entity.y + self.dy

        if not engine.game_map.in_bounds(destination_x, destination_y):
            return # Destination is out of bounds
        if not engine.game_map.tiles["walkable"][destination_x, destination_y]:
            return # Destination is blocked by a tile.
        entity.move(self.dx, self.dy)