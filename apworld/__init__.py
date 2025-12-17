from Rules import add_rule, set_rule, forbid_item, add_item_rule #@TODO: fix this later for proper pathway once in archipelago (should be worlds.generic.rules)
import settings
import typing
from .options import BuckshotOptions  
from .Items import item_table, BuckshotItem  # data used below to add items to the World
from .Locations import base_locations_table, DorN1_table, DorN2_table, shoot_self_table, BuckshotLocation  # same as above
from AutoWorld import World
from BaseClasses import Region, Location, Entrance, Item, ItemClassification

'''
Current build actually has the imports in a compatible way. 
This current directory is just my test environment so the paths are different.
This will be fixed in the future when this is playable
'''


# All structure here copied from example in "world api" docs. Other inspiration taken from other implemented worlds & APQuest

class BuckshotRouletteWorld(World):
    """Play Russian roulette with a 12-gauge shotgun."""

    game = "Buckshot Roulette"  # name of the game/world

    topology_present = True  # show path to required location checks in spoiler

    base_id = 622888000
    # base id chosen at random. dont know if i need this anymore but ive memorized it

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

    item_name_to_id = {name: item_table[name][1] for name
                        in item_table.keys()}
    
    options_dataclass = BuckshotOptions
    options: BuckshotOptions
        


    location_name_to_id = {}

    for table in [base_locations_table, DorN1_table, DorN2_table, shoot_self_table]:
        location_name_to_id.update(table)

            


    def create_item(self, name: str) -> BuckshotItem:
        return BuckshotItem(name, item_table[name][0], item_table[name][1], self.player)
    
    
    def create_regions(self) -> None:
        # Add regions to the multiworld. One of them must use the origin_region_name as its name ("Menu" by default).
        # Arguments to Region() are name, player, multiworld, and optionally hint_text

        # Base Game: The three rounds against the dealer
        BaseGame = Region("Base Game", self.player, self.multiworld)
        BaseGame.add_locations(base_locations_table, BuckshotLocation)
        self.multiworld.regions.append(BaseGame)
        self.origin_region_name = "Base Game"

        # DorN1: Double or nothing 1 (0 to 250,000)
        DorN1_R = Region("Double or Nothing 1", self.player, self.multiworld)
        DorN1_R.add_locations(DorN1_table, BuckshotLocation)
        self.multiworld.regions.append(DorN1_R)

        # DorN2: Double or nothing 2 (250,000 to beyond)
        DorN2_R = Region("Double or Nothing 2", self.player, self.multiworld)
        DorN2_R.add_locations(DorN2_table, BuckshotLocation)
        self.multiworld.regions.append(DorN2_R)

        # Two locked areas: Double or Nothing (up to 250,000) and Double or Nothing (infinite)
        BaseGame.add_exits({"Double or Nothing 1": "Pills"}, {"Double or Nothing 1": lambda state: state.has("Pills", self.player)})
        DorN1_R.add_exits({"Double or Nothing 2": "DorN2_R"}, {"Double or Nothing 2": lambda state: state.has("DoubleOrNothingTo500", self.player)})


        # Optional areas
        match self.options.shoot_self:

            case self.options.shoot_self.option_once:
                BaseGame.add_locations({"Shoot 1 Blank": shoot_self_table["Shoot 1 Blank"], "Shoot 1 Live": shoot_self_table["Shoot 1 Live"]}, BuckshotLocation)
            
            case self.options.shoot_self.option_thrice:
                BaseGame.add_locations(shoot_self_table, BuckshotLocation)
    
    def create_items(self) -> None:

        # Core progression items:
        self.multiworld.itempool.append(map(self.create_item, ["Pills", "DoubleOrNothingTo500"]))

        # Adding progression items: these are required to complete the game
        # can be customized but not implemented yet

        unlockables = Items.unlockable_items.copy()
        for i in range(self.options.starting_items):
            unlockables.pop(self.random.randint(0, len(unlockables) - 1))

        for item in map(self.create_item, unlockables):
            self.multiworld.itempool.append(item)

        junk = len(self.multiworld.get_unfilled_locations(self.player)) - (9 - self.options.starting_items)  # 9 starting items, minus starting items already given as determined by options
        traps = junk * self.options.traps // 100
        filler = junk - traps

        for _ in range(traps):
            trap_item = self.random.choice(Items.trap_items)
            self.multiworld.itempool.append(self.create_item(trap_item))
        
        for _ in range(filler):
            filler_item = self.random.choice(Items.helpful_items)
            self.multiworld.itempool.append(self.create_item(filler_item))
        
        

        
    
    
    def set_rules(self) -> None:

        # Only basic rules for now
        set_rule(self.multiworld.get_region("Double or Nothing 1", self.player),
                 lambda state: state.has("Pills", self.player))
        
        # Need two unlocks to access DorN1 (as well as pills, obviously)
        set_rule(self.multiworld.get_region("Double or Nothing 1", self.player),
                 lambda state: state.count_group(item_name_group="ItemUnlocks", player=self.player) >= 2)
        
        # and 4 items for the next level
        set_rule(self.multiworld.get_region("Double or Nothing 2", self.player),
                 lambda state: state.count_group(item_name_group="ItemUnlocks", player=self.player) >= 4)
        
        endregion = self.multiworld.get_region("Double or Nothing 2", self.player)
        endregion.add_event("1000k", "Victory", location_type=BuckshotLocation, item_type=BuckshotItem)
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Victory", self.player)

        from Utils import visualize_regions
        visualize_regions(self.multiworld.get_region("Double or Nothing 2", self.player), "my_world.puml")




