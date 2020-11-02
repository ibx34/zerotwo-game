import dataclasses
import enum


class Rarity(enum.Enum):
    MYSTIC = "Mystic"
    LEGENDDARY = "Legendary"
    SUPER_RARE = "Super Rare"
    RARE = "Rare"
    UNCOMMON = "Uncommon"
    COMMON = "Common"

@dataclasses.dataclass
class Stats:
    health: int
    damage: int
    price: int

@dataclasses.dataclass
class Card:
    url: str
    type: Rarity
    stats: Stats
    name: str
    series: strs
    id: int
