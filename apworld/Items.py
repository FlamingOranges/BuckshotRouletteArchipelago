from typing import List, Dict, Set
from BaseClasses import Item, ItemClassification
from enum import Enum


# come back to this later: base_id = 


class ItemType(Enum):
     
    # Core Progression
    Pills = 0
    DoubleOrNothingTo250 = 1
    DoubleOrNothingTo500 = 2

    # Unlockable items
    BurnerUnlock = 3
    AdrenalineUnlock = 4
    MagnifyingUnlock = 5
    InverterUnlock = 6
    BeerUnlock = 7
    CigarettesUnlock = 8
    MedicineUnlock = 9
    HandSawUnlock = 10
    HandcuffsUnlock = 11

    # Assorted items
    BurnerPhone = 12
    Adrenaline = 13
    Magnifying = 14
    Inverter = 15
    Beer = 16
    Cigarettes = 17
    Medicine = 18
    HandSaw = 19
    Handcuffs = 20

    # Traps
    ShellInvert = 21
    HealthLoss = 22

    # Blessings
    HealthCharge = 23
    



class BuckshotItem(Item):
    game = "Buckshot Roulette"


