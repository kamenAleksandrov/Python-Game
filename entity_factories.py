import random

from entity import Actor, Item
from components.fighter import Fighter
from components.ai import HostileEnemy
from components import consumable, equippable
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from SpriteManager import Sprite

player_idle_sprite = Sprite("images/0x72_DungeonTilesetII_v1.7/frames/Knight/Male/idle/", frame_duration=0.2)

player = Actor(
    char="P",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, base_defence=1, base_attack=4, precision=1),
    inventory=Inventory(capacity=9),
    level=Level(level_up_base=50),
    equipment=Equipment(),
    sprite=player_idle_sprite,
    )

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=5, base_defence=0, base_attack=2, precision=1),
    inventory=Inventory(capacity=26),
    level=Level(xp_given=35),
    equipment=Equipment(),
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, base_defence=1, base_attack=3, precision=1),
    inventory=Inventory(capacity=26),
    level=Level(xp_given=75),
    equipment=Equipment(),
    )

health_potion = Item(
    char="8",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(healingamount=random.randint(3,9)),
)

lightning_scroll = Item(
    char="~",
    color=(255, 255, 0),
    name="Lightning Scroll",
    consumable=consumable.LightningDamageConsumable(damage=20, maximum_range=5),
)

confusion_scroll = Item(
    char="~@",
    color=(207, 63, 255),
    name="Confusion Scroll",
    consumable=consumable.ConfusionConsumable(number_of_turns=7),
)

fireball_scroll = Item(
    char="~^",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=20, radius=3),
)

dagger = Item(
    char="d-)=>", color=(0, 191, 255), name="Dagger", equippable=equippable.Dagger()
)

sword = Item(
    char="D-(===>", color=(0, 191, 255), name="Sword", equippable=equippable.Sword()
)

leather_armor = Item(
    char="||",
    color=(139, 69, 19),
    name="Leather Armor",
    equippable=equippable.LeatherArmor(),
)

chain_mail = Item(
    char="[]",
    color=(139, 69, 19),
    name="Chain Mail",
    equippable=equippable.ChainMail(),
)