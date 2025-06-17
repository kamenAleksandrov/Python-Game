from __future__ import annotations

from typing import TYPE_CHECKING

from components.base_component import BaseComponent
from equipment_types import EquipmentType

if TYPE_CHECKING:
    from entity import Item

class Equippable(BaseComponent):
    parent: Item

    def __init__(
            self,
            equipment_type: EquipmentType,
            attack_bonus: int = 0,
            defence_bonus: int = 0,
    ):
        self.equipment_type = equipment_type
        self.attack_bonus = attack_bonus
        self.defense_bonus = defence_bonus

class Dagger(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=2)

class Sword(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.WEAPON, attack_bonus=4)

class LeatherArmor(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defence_bonus=1)

class ChainMail(Equippable):
    def __init__(self) -> None:
        super().__init__(equipment_type=EquipmentType.ARMOR, defence_bonus=3)