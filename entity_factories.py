from entity import Actor, Item
from components.fighter import Fighter
from components.ai import HostileEnemy
from components import consumable
from components.inventory import Inventory
from components.level import Level

player = Actor(
    char="P",
    color=(255, 255, 255),
    name="Player",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=30, defence=2, power=5),
    inventory=Inventory(capacity=26),
    level=Level(level_up_base=200),
    )

orc = Actor(
    char="o",
    color=(63, 127, 63),
    name="Orc",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=10, defence=0, power=3),
    inventory=Inventory(capacity=26),
    level=Level(xp_given=35),
)

troll = Actor(
    char="T",
    color=(0, 127, 0),
    name="Troll",
    ai_cls=HostileEnemy,
    fighter=Fighter(hp=16, defence=1, power=4),
    inventory=Inventory(capacity=26),
    level=Level(xp_given=75),
    )

health_potion = Item(
    char="8",
    color=(127, 0, 255),
    name="Health Potion",
    consumable=consumable.HealingConsumable(healingamount=5),
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
    consumable=consumable.ConfusionConsumable(number_of_turns=5),
)

fireball_scroll = Item(
    char="~^",
    color=(255, 0, 0),
    name="Fireball Scroll",
    consumable=consumable.FireballDamageConsumable(damage=20, radius=3),
)