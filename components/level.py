from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent

if TYPE_CHECKING:
    from entity import Actor

class Level(BaseComponent):
    parent: Actor

    def __init__(
            self,
            current_level: int = 1,
            current_xp: int = 0,
            level_up_base: int = 0,
            level_up_factor: int = 50,
            xp_given: int = 0,
    ):
            self.current_level=current_level
            self.current_xp=current_xp
            self.level_up_base=level_up_base
            self.level_up_factor=level_up_factor
            self.xp_given=xp_given

    @property
    def experience_to_next_level(self) -> int:
        return self.level_up_base + self.current_level * self.level_up_factor

    @property
    def requires_level_up(self) -> bool:
        return self.current_xp > self.experience_to_next_level

    def add_xp(self, xp: int) -> None:
        if xp == 0 or self.level_up_base == 0:
            return
        self.current_xp += xp
        self.engine.message_log.add_message(f"You gain {xp} experience points.")

        if self.requires_level_up:
            self.engine.message_log.add_message(
                f"You advance to level {self.current_level + 1}"
            )

    def increase_level(self) -> None:
        self.current_xp = 0
        self.current_level += 1

    def increase_max_hp(self, amount: int = 10) -> None:
        self.parent.fighter.max_hp += amount
        self.parent.fighter.hp += amount

        self.engine.message_log.add_message("Your constitution rises!")

        self.increase_level()

    def increase_attack(self, amount: int = 1) -> None:
        self.parent.fighter.base_attack += amount
        self.engine.message_log.add_message("Your power rises!")

        self.increase_level()

    def increase_precision(self, amount: int = 1) -> None:
        self.parent.fighter.precision += amount
        self.engine.message_log.add_message("Your precision rises!")

        self.increase_level()

    def increase_defence(self, amount: int = 1) -> None:
        self.parent.fighter.base_defence += amount
        self.engine.message_log.add_message("Your reactions are getting faster!")

        self.increase_level()