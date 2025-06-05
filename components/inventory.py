from __future__ import annotations

import copy
from typing import List, TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor, Item

class Inventory(BaseComponent):
    parent: Actor

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items: List[Item] = []

    def drop(self, item: Item) -> None:
        """
        Drop item from the inventory on to the game map at the player's location.
        """
        if item.quantity > 1:
            item.quantity -= 1
            # Create a new item entity on the ground with quantity = 1
            dropped_item = copy.deepcopy(item)
            dropped_item.quantity = 1
            dropped_item.place(self.parent.x, self.parent.y, self.gamemap)
        else:
            self.items.remove(item)
            item.place(self.parent.x, self.parent.y, self.gamemap)

        self.engine.message_log.add_message(f"You dropped {item.name}.")