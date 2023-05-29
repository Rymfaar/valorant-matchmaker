from enum import Enum
from enum import IntEnum

class Roles(Enum):
  FLEX = 0
  CONTROLLER = 1
  INITIATOR = 2
  DUELIST = 3
  SENTINEL = 4

class Rank(IntEnum):
  UNRANKED = 0
  IRON = 150
  BRONZE = 450
  SILVER = 750
  GOLD = 1050
  PLATINIUM = 1350
  DIAMOND = 1650
