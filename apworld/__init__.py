
import settings
import typing
#from .Options import MyGameOptions  # the options we defined earlier
from .Items import item_table, BuckshotItem  # data used below to add items to the World
from .Locations import BuckshotLocation  # same as above
from AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, RegionType, ItemClassification



class BuckshotRouletteWorld(World):
    """Play Russian roulette with a 12-gauge shotgun."""

    game = "Buckshot Roulette"  # name of the game/world
    # Add options 
    topology_present = True  # show path to required location checks in spoiler

    # ID of first item and location, could be hard-coded but code may be easier
    # to read with this as a property.
    base_id = 622888000
    # instead of dynamic numbering, IDs could be part of data

    # Items can be grouped using their names to allow easy checking if any item
    # from that group has been collected. Group names can also be used for !hint
    item_name_groups = {
        "ItemUnlocks": {
            "BurnerUnlock",
            "AdrenalineUnlock",
            "MagnifyingUnlock",
            "InverterUnlock",
            "BeerUnlock",
            "CigarettesUnlock",
            "MedicineUnlock",
            "HandSawUnlock",
            "HandcuffsUnlock"
        }
    }



    def create_item(self, name: str) -> BuckshotItem:
        return BuckshotItem(name, item_table[name][0], item_table[name[1]], self.player)
    
    def create_event(self, event: str) -> BuckshotItem:
        return BuckshotItem(event, ItemClassification.progression, None, self.player)
    
    def create_regions(self) -> None:
        # Add regions to the multiworld. One of them must use the origin_region_name as its name ("Menu" by default).
        # Arguments to Region() are name, player, multiworld, and optionally hint_text

        # Base Game: The three rounds against the dealer
        BaseGame = Region("Base Game", self.player, self.multiworld)
        BaseGame.add_locations(Locations.base_locations_table, BuckshotLocation)
        self.multiworld.regions.append(BaseGame)

        # DorN1: Double or nothing 1 (0 to 250,000)
        DorN1_R = Region("Double or Nothing 1", self.player, self.multiworld)
        DorN1_R.add_locations(Locations.DorN1_table, BuckshotLocation)
        self.multiworld.regions.append(DorN1_R)

        # DorN2: Double or nothing 2 (250,000 to beyond)
        DorN2_R = Region("Double or Nothing 2", self.player, self.multiworld)
        DorN2_R.add_locations(Locations.DorN2_table, BuckshotLocation)
        self.multiworld.regions.append(DorN2_R)

        BaseGame.add_exits({"Double or Nothing 1": "Pills"}, {"Double or Nothing 1": lambda state: state.has("Pills", self.player)})
        
        DorN1_R.add_exits({"Double or Nothing 2": "DorN2_R"}, {"Double or Nothing 2": lambda state: state.has("DoubleOrNothingTo500", self.player)})
    
    def create_items(self) -> None:
        # Add items to the Multiworld.
        # If there are two of the same item, the item has to be twice in the pool.
        # Which items are added to the pool may depend on player options, e.g. custom win condition like triforce hunt.
        # Having an item in the start inventory won't remove it from the pool.
        # If an item can't have duplicates it has to be excluded manually.

        # List of items to exclude, as a copy since it will be destroyed below
        exclude = []

        for item in map(self.create_item, item_table.keys()):
            self.multiworld.itempool.append(item)

        # itempool and number of locations should match up.
        # If this is not the case we want to fill the itempool with junk.
        junk = 0  # calculate this based on player options
        self.multiworld.itempool += [self.create_item("nothing") for _ in range(junk)]