from __future__ import annotations  # this speed up load times

from typing import Optional, Tuple, TYPE_CHECKING

import color
import exceptions

if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity, Actor, Item


class Action:

    def __init__(self, entity: Actor) -> None:
        super().__init__()
        self.entity = entity

    @property
    def engine(self) -> Engine:
        """Return the engine this action belongs to."""
        return self.entity.gamemap.engine

    def perform(self) -> None:
        def perform(self, engine: Engine, entity: Entity) -> None:
            """Perform this action with the objects needed to determine its scope.

            `self.engine` is the scope this action is being performed in.
            `engine` is the scope this action is being performed in.

            `self.entity` is the object performing the action.
            `entity` is the object performing the action.

            This method must be overridden by Action subclasses.
            """
            raise NotImplementedError()


class PickupAction(Action):

    def __init__(self, entity: Actor):
        super().__init__(entity)

    def perform(self) -> None:
        actor_location_x = self.entity.x
        actor_location_y = self.entity.y
        inventory = self.entity.inventory

        for item in self.engine.game_map.items:
            if actor_location_x == item.x and actor_location_y == item.y:
                if len(inventory.items) >= inventory.capacity:
                    raise exceptions.Impossible("Your inventory is full.")

                # item.parent = self.entity.inventory
                for inv_item in inventory.items:
                    if inv_item.name == item.name:
                        inv_item.quantity += item.quantity
                        self.engine.game_map.entities.remove(item)
                        self.engine.message_log.add_message(f"You picked up another {item.name}! (x{item.quantity})")
                        return
                    else:
                        item.parent = inventory
                        inventory.items.append(item)
                        self.engine.game_map.entities.remove(item)
                        self.engine.message_log.add_message(f"You picked up {item.name}!")
                    return
                # if any(inv_item.name == item.name for inv_item in inventory.items):
                #     item.quantity += 1
                #     item.parent = inventory
                #     inventory.items.append(item)



        raise exceptions.Impossible("There is nothing to pick up.")


class ItemAction(Action):
    def __init__(
            self, entity: Actor, item: Item, target_xy: Optional[Tuple[int, int]] = None
    ):
        super().__init__(entity)
        self.item = item
        if not target_xy:
            target_xy = entity.x, entity.y
        self.target_xy = target_xy

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.target_xy)

    def perform(self) -> None:
        """Invoke the items ability, this action will be given to provide context."""
        self.item.consumable.activate(self)


class ActionWithDirection(Action):
    def __init__(self, entity: Actor, dx: int, dy: int):
        super().__init__(entity)

        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        """Returns this actions destination."""
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        """Return the blocking entity at this actions destination.."""
        return self.engine.game_map.get_blocking_entity_at_location(*self.dest_xy)

    @property
    def target_actor(self) -> Optional[Actor]:
        return self.engine.game_map.get_actor_at_location(*self.dest_xy)

    def perform(self) -> None:
        raise NotImplementedError()


class BumpAction(ActionWithDirection):
    def perform(self) -> None:
        if self.target_actor:
            return MeleeAction(self.entity, self.dx, self.dy).perform()
        else:
            return MoveAndPickUpAction(self.entity, self.dx, self.dy).perform()


class MeleeAction(ActionWithDirection):
    def perform(self) -> None:
        target = self.target_actor
        if not target:
            raise exceptions.Impossible("Nothing to attack.")

        damage = self.entity.fighter.power - target.fighter.defence

        attack_desc = f"{self.entity.name.capitalize()} attacks {target.name}"
        if self.entity is self.engine.player:
            attack_color = color.player_attack
        else:
            attack_color = color.npc_attack

        if damage > 0:
            self.engine.message_log.add_message(
                f"{attack_desc} for {damage} damage.", attack_color
            )
            target.fighter.hp -= damage
        else:
            self.engine.message_log.add_message(
                f"{attack_desc} but does no damage.", attack_color
            )


class MovementAction(ActionWithDirection):

    def perform(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            # Destination is out of bounds.
            raise exceptions.Impossible("That way is blocked.")
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            # Destination is blocked by a tile.
            raise exceptions.Impossible("That way is blocked.")
        if self.engine.game_map.get_blocking_entity_at_location(dest_x, dest_y):
            # Destination is blocked by an entity.
            raise exceptions.Impossible("That way is blocked.")

        self.entity.move(self.dx, self.dy)


class MoveAndPickUpAction(MovementAction):
    def perform(self) -> None:
        super().perform()
        if self.entity is self.engine.player:
            try:
                PickupAction(self.entity).perform()
            except exceptions.Impossible:
                pass


class WaitAction(Action):
    def perform(self) -> None:
        pass


class DropItem(ItemAction):
    def perform(self) -> None:
        self.entity.inventory.drop(self.item)


class TakeStairsAction(Action):
    def perform(self) -> None:
        if (self.entity.x, self.entity.y) == self.engine.game_map.stairsdown_location:
            self.engine.game_world.generate_floor()
            self.engine.message_log.add_message(
                "You delve deeper into the dungeon!", color.descend
            )
        else:
            raise exceptions.Impossible("There are ne stair here.")
