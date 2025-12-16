from BaseClasses import Item, ItemClassification

class BuckshotItem(Item):
    game = "Buckshot Roulette"


item_table = {
    # Core Progression
    "Pills": (ItemClassification.progression, 622888001),
    "DoubleOrNothingTo500": (ItemClassification.progression, 622888002),

    # Helper progression
    # Note: Not really true "progression" but i'm keeping it as is for now
    "BurnerUnlock": (ItemClassification.progression, 622888004),
    "AdrenalineUnlock": (ItemClassification.progression, 622888005),
    "MagnifyingUnlock": (ItemClassification.progression, 622888006),
    "InverterUnlock": (ItemClassification.progression, 622888007),
    "BeerUnlock": (ItemClassification.progression, 622888008),
    "CigarettesUnlock": (ItemClassification.progression, 622888009),
    "MedicineUnlock": (ItemClassification.progression, 622888010),
    "HandSawUnlock": (ItemClassification.progression, 622888011),
    "HandcuffsUnlock": (ItemClassification.progression, 622888012),

    # Helpful items
    "Burner": (ItemClassification.useful, 622888013),
    "Adrenaline": (ItemClassification.useful, 622888014),
    "Magnifying Glass": (ItemClassification.useful, 622888015),
    "Inverter": (ItemClassification.useful, 622888016),
    "Beer": (ItemClassification.useful, 622888017),
    "Cigarettes": (ItemClassification.useful, 622888018),
    "Medicine": (ItemClassification.useful, 622888019),
    "Hand Saw": (ItemClassification.useful, 622888020),
    "Handcuffs": (ItemClassification.useful, 622888021),

    # Traps
    "Shell Inversion": (ItemClassification.trap, 622888022),
    "Health Loss": (ItemClassification.trap, 622888023),
}




