from .APOptions import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle
from dataclasses import dataclass

class Traps(Range):
    '''
    Set the amount of traps in the extra item pool (no traps will be added if set too low or there are not enough locations after unlocks).
    0: No traps
    100: All traps
    '''
    display_name = "Traps"
    range_start = 0
    range_end = 100
    default = 10

class ShootSelf(Choice):
    '''
    Adds shooting yourself with lives and blanks as a possible location in the game.
    0: Off
    1: Shooting self once is a check (Once live, once blank)
    2: Shooting self 3 times is a check (Thrice live, thrice blank)
    Selecting option 2 will add both once and three times as separate checks. (total of 4 checks)
    '''
    display_name = "Shoot Self Option"
    option_off = 0
    option_once = 1
    option_thrice = 2
    default = option_off

class StartingItems(Range): 
    # Not currently implemented
    """Sets the amount of items you start with already unlocked. (Assigned Randomly)"""

    # Choosing the items can be an option at a later time
    display_name = "Starting Items"
    range_start = 0
    range_end = 9
    default = 0

@dataclass
class BuckshotOptions(PerGameCommonOptions):
    traps: Traps
    shoot_self: ShootSelf
    starting_items: StartingItems