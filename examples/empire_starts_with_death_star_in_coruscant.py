from swr_ed import MANAGERS_BY_FILE

manager_class = MANAGERS_BY_FILE['CMUNEFTB.DAT']
manager = manager_class()
manager.load()


# The structure for this file is hierarchical in the sense that, depending of the position, the line
# contents would have different interpretations.
# This is in contrast to most other files were each line is self-contained.


# [1] The first line of a "group". The first and third numbers in this line are the "id" of the group.
#     In this case this is group 1.
#     If there were more groups, you would have to have sequentially increment this number for each new group
#     (2, 3, 4, etc.)

# [2] This line defines the "length" of the group. In this case, the next 43 items in the file form group 1.
#     The next 43 lines after this one list the actual units in a group
#     This works well for fleets, as capital ships may be able to contain troops and fighter squadrons.
#     If the capital ship does not have capacity for troops and or squadrons, the length of the group should be 1.

# [3] The first unit in a group should be a the capital ship.
#     136 is the Death Star in this case 24 is the family_id of the Death Star

# [4] The remaining 42 entries in this group relate the units inside the capital ship defined in the previous line.
#     In this case, the Death Star is able to contain 24 fighter squadrons and 18 troop units.
#     Therefore we have 24 lines for Tie Fighters (id 5 and family_id 16) followed by 18 lines for Stormtropper
#     regiments (id 6 and family_id 16)

# [5] This is the start of a second group.
# [6] This line defines that group contains 10 units.
# [7] The capital ship for this group is an Imperial Star Destroyer (id 133 and family_id 20)
# [8] Much like the previous group, this group has Stormtroppers and Tie Fighters


# The family_id values tell the Rebellion program on which file the unit is located (16 is TROOPSD.DAT and 28 is for
# FIGHTSD.DAT)
# The id numbers relate to the identifier for each unit within their file

manager.data = [
    [1, 1, 1, 0, 0],     # [1]
    [1, 1, 43, 0, 0],    # [2]
    [1, 0, 136, 0, 24],  # [3]
    [1, 0, 5, 0, 28],    # [4]
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [2, 1, 2, 0, 0],     # [5]
    [1, 1, 10, 0, 0],    # [6]
    [1, 0, 133, 0, 20],  # [7]
    [1, 0, 5, 0, 28],    # [8]
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 5, 0, 28],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
    [1, 0, 6, 0, 16],
]

manager.save()
