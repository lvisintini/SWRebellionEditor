from collections import OrderedDict

from swr_ed.base import SWRDataManager, FieldDef, ProbabilityTableManager, SimpleTableDataManager, GroupedTableManager
from swr_ed.constants import FieldType


class FightersDataDataManager(SWRDataManager):
    filename = "FIGHTSD.DAT"
    expected_header = (1, 8, 28, 32)
    expected_md5_checksum = '572eb17566f6501be1141575f456c7f0'

    id = FieldDef('I', FieldType.READ_ONLY)
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 40
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 41
    family_id = FieldDef('I', FieldType.READ_ONLY)  # always 28
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)
    research_order = FieldDef('I', FieldType.EDITABLE)
    unknown_1 = FieldDef('I', FieldType.UNKNOWN)  # maybe research difficulty
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # maybe moral modifier, always 0
    detection = FieldDef('I', FieldType.EDITABLE)
    shield = FieldDef('I', FieldType.EDITABLE)
    sublight_speed = FieldDef('I', FieldType.EDITABLE)
    maneuverability = FieldDef('I', FieldType.EDITABLE)
    hyperdrive = FieldDef('I', FieldType.EDITABLE)
    unknown_3 = FieldDef('I', FieldType.UNKNOWN)  # backup hyperdrive, always 0
    turbolaser_firepower_front = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_front = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_front = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_rear = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_rear = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_rear = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_left = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_left = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_left = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_right = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_right = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_right = FieldDef('I', FieldType.EDITABLE)
    turbolasers_range = FieldDef('I', FieldType.EDITABLE)
    ion_range = FieldDef('I', FieldType.EDITABLE)
    laser_range = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    ion_firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    laser_firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    torpedo_power = FieldDef('I', FieldType.EDITABLE)
    torpedo_range = FieldDef('I', FieldType.EDITABLE)
    squadron_size = FieldDef('I', FieldType.EDITABLE)  # always 12
    bombardment = FieldDef('I', FieldType.EDITABLE)


class TroopsDataDataManager(SWRDataManager):
    filename = "TROOPSD.DAT"
    expected_header = (1, 10, 16, 20)
    expected_md5_checksum = 'c33fe785bfb1c0a42328009f9d28a68d'

    id = FieldDef('I', FieldType.READ_ONLY)
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 41
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 42
    family_id = FieldDef('I', FieldType.EDITABLE)  # always 16
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)
    research_order = FieldDef('I', FieldType.EDITABLE)
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # maybe research difficulty
    unknown_3 = FieldDef('I', FieldType.UNKNOWN)  # maybe moral modifier, always 0
    detection = FieldDef('I', FieldType.EDITABLE)
    bombardment_defense = FieldDef('I', FieldType.EDITABLE)
    attack = FieldDef('I', FieldType.EDITABLE)
    defense = FieldDef('I', FieldType.EDITABLE)


class CapitalShipsDataDataManager(SWRDataManager):
    filename = "CAPSHPSD.DAT"
    expected_header = (1, 30, 20, 28)
    expected_md5_checksum = '6ebce9890547475adc09dc2071bd9216'

    id = FieldDef('I', FieldType.READ_ONLY)
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 40
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 41
    family_id = FieldDef('I', FieldType.READ_ONLY)  # 20 for the Capital Ships and 24 for the Death Star
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.READ_ONLY)
    imperial = FieldDef('I', FieldType.READ_ONLY)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)
    research_order = FieldDef('I', FieldType.EDITABLE)
    unknown_1 = FieldDef('I', FieldType.UNKNOWN)  # maybe research difficulty
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # maybe moral modifier, basicly 0.45 * construction_cost
    detection = FieldDef('I', FieldType.EDITABLE)
    shield = FieldDef('I', FieldType.EDITABLE)
    sublight_speed = FieldDef('I', FieldType.EDITABLE)
    maneuverability = FieldDef('I', FieldType.EDITABLE)
    hyperdrive = FieldDef('I', FieldType.EDITABLE)
    unknown_3 = FieldDef('I', FieldType.UNKNOWN)  # backup hyperdrive, always 0
    turbolaser_firepower_front = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_front = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_front = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_rear = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_rear = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_rear = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_left = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_left = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_left = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_right = FieldDef('I', FieldType.EDITABLE)
    ion_firepower_right = FieldDef('I', FieldType.EDITABLE)
    laser_firepower_right = FieldDef('I', FieldType.EDITABLE)
    turbolasers_range = FieldDef('I', FieldType.EDITABLE)
    ion_range = FieldDef('I', FieldType.EDITABLE)
    laser_range = FieldDef('I', FieldType.EDITABLE)
    turbolaser_firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    ion_firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    laser_firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    firepower_sum = FieldDef('I', FieldType.DENORMALIZED)
    hull = FieldDef('I', FieldType.EDITABLE)
    tractor_beam_power = FieldDef('I', FieldType.EDITABLE)
    tractor_beam_range = FieldDef('I', FieldType.EDITABLE)
    gravity_well_1 = FieldDef('H', FieldType.EDITABLE)  # 4 if present
    gravity_well_2 = FieldDef('H', FieldType.EDITABLE)  # 100 if present
    unknown_4 = FieldDef('I', FieldType.READ_ONLY)  # Always 0
    bombardment = FieldDef('I', FieldType.EDITABLE)
    damage_control = FieldDef('I', FieldType.EDITABLE)
    weapon_recharge = FieldDef('I', FieldType.EDITABLE)
    shield_recharge = FieldDef('I', FieldType.EDITABLE)
    fighter_squadrons = FieldDef('I', FieldType.EDITABLE)
    troop_contingents = FieldDef('I', FieldType.EDITABLE)
    unknown_5 = FieldDef('I', FieldType.EDITABLE)


class SectorsDataDataManager(SWRDataManager):
    filename = "SECTORSD.DAT"
    expected_header = (1, 20, 128, 144)
    expected_md5_checksum = '21b49b9e8a0c2829da55e083cab16969'

    id = FieldDef('I', FieldType.READ_ONLY)  # starting from 100
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 0
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 0
    family_id = FieldDef('I', FieldType.READ_ONLY)  # always 128
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    importance = FieldDef('I', FieldType.EDITABLE)  # 1-high 2-medium 3-low
    game_size = FieldDef('I', FieldType.EDITABLE)  # 1-Small 2-Medium 3-Large
    position_x = FieldDef('H', FieldType.EDITABLE)
    position_y = FieldDef('H', FieldType.EDITABLE)


class MissionDataDataManager(SWRDataManager):
    filename = "MISSNSD.DAT"
    expected_header = (1, 25, 64, 128)
    expected_md5_checksum = '3671b7e692a198a042b92a89ad0846c8'

    id = FieldDef('I', FieldType.READ_ONLY)
    active = FieldDef('I', FieldType.UNKNOWN)
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)
    family_id = FieldDef('I', FieldType.READ_ONLY)
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.READ_ONLY)
    imperial = FieldDef('I', FieldType.READ_ONLY)
    special_forces_code = FieldDef('I', FieldType.READ_ONLY)  # Controls available missions to special forces
    tbd_04_1 = FieldDef('H', FieldType.READ_ONLY)  # Always 0
    tbd_04_2 = FieldDef('H', FieldType.READ_ONLY)  # 1 for everyone except recon that gets 0
    length = FieldDef('I', FieldType.READ_ONLY)
    length_variance = FieldDef('I', FieldType.READ_ONLY)
    has_progress_reports = FieldDef('I', FieldType.READ_ONLY)
    tbd_08 = FieldDef('I', FieldType.READ_ONLY)  # Missions non selectable in mission selection screen = 1
    tbd_09 = FieldDef('I', FieldType.READ_ONLY)  # 0 for "Bounty" mission, 1 for the rest of the missions
    tbd_10 = FieldDef('I', FieldType.READ_ONLY)  # Missions selectable in mission selection screen = 0
    tbd_11 = FieldDef('I', FieldType.READ_ONLY)  # 0,1,2
    tbd_12 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_13 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_14 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_15 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_16 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_17 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_18 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_19 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_20 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_21 = FieldDef('I', FieldType.READ_ONLY)  # 1,0
    tbd_22 = FieldDef('I', FieldType.READ_ONLY)  # 1,0


class SystemsDataDataManager(SWRDataManager):
    filename = "SYSTEMSD.DAT"
    expected_header = (1, 200, 144, 152)
    expected_md5_checksum = '6896149fc26d1573118d1193b0d0366d'

    id = FieldDef('I', FieldType.READ_ONLY)  # starting from 100
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 0
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 0
    family_id = FieldDef('I', FieldType.READ_ONLY)  # 144 core systems and 146 for out rim systems
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    sector_id = FieldDef('I', FieldType.EDITABLE)  # starting from 20
    type = FieldDef('I', FieldType.EDITABLE)  # picture? 1-26
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # always 1
    position_x = FieldDef('H', FieldType.EDITABLE)
    position_y = FieldDef('H', FieldType.EDITABLE)
    unknown_3 = FieldDef('I', FieldType.UNKNOWN)  # always 0


class DefensiveFacilitiesDataDataManager(SWRDataManager):
    filename = "DEFFACSD.DAT"
    expected_header = (1, 6, 34, 40)
    expected_md5_checksum = 'ec67675858ebff9a186c7984b63d8d8e'

    id = FieldDef('I', FieldType.READ_ONLY)  # starting from 1
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 42
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 43
    # 34 for ion, 35 for lasers, 36 for shields and 37 for Death Star shield
    family_id = FieldDef('I', FieldType.READ_ONLY)
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)
    research_order = FieldDef('I', FieldType.EDITABLE)
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # maybe research difficulty
    bombardment_defense = FieldDef('I', FieldType.UNKNOWN)
    firepower = FieldDef('I', FieldType.EDITABLE)
    shield_generation = FieldDef('I', FieldType.EDITABLE)


class ManufacturingFacilitiesDataDataManager(SWRDataManager):
    filename = "MANFACSD.DAT"
    expected_header = (1, 6, 40, 44)
    expected_md5_checksum = '75d1e916c00a411ca58b48eb46b055ae'

    id = FieldDef('I', FieldType.READ_ONLY)  # starting from 1
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 42
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 43
    # 40 for shipyards, 41 for training facilities and 42 for construction yards
    family_id = FieldDef('I', FieldType.READ_ONLY)
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)
    research_order = FieldDef('I', FieldType.EDITABLE)
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # maybe research difficulty
    bombardment_defense = FieldDef('I', FieldType.UNKNOWN)  # maybe moral modifier
    manufacturing_rate = FieldDef('I', FieldType.EDITABLE)  # required days to manufacture 1 unit


class SpecialForcesDataDataManager(SWRDataManager):
    filename = "SPECFCSD.DAT"
    expected_header = (1, 9, 60, 64)
    expected_md5_checksum = '310154da0e88381afc602185a545200d'

    id = FieldDef('I', FieldType.READ_ONLY)
    active = FieldDef('I', FieldType.UNKNOWN)
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)
    family_id = FieldDef('I', FieldType.READ_ONLY)
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)
    research_order = FieldDef('I', FieldType.UNKNOWN)  # always 0
    unknown_5 = FieldDef('I', FieldType.UNKNOWN)  # always 0
    diplomacy_base = FieldDef('I', FieldType.EDITABLE)
    diplomacy_variance = FieldDef('I', FieldType.EDITABLE)
    espionage_base = FieldDef('I', FieldType.EDITABLE)
    espionage_variance = FieldDef('I', FieldType.EDITABLE)
    ship_research_base = FieldDef('I', FieldType.EDITABLE)
    ship_research_variance = FieldDef('I', FieldType.EDITABLE)
    troop_research_base = FieldDef('I', FieldType.EDITABLE)
    troop_research_variance = FieldDef('I', FieldType.EDITABLE)
    facility_research_base = FieldDef('I', FieldType.EDITABLE)
    facility_research_variance = FieldDef('I', FieldType.EDITABLE)
    combat_base = FieldDef('I', FieldType.EDITABLE)
    combat_variance = FieldDef('I', FieldType.EDITABLE)
    leadership_base = FieldDef('I', FieldType.EDITABLE)
    leadership_variance = FieldDef('I', FieldType.EDITABLE)
    loyalty_base = FieldDef('I', FieldType.EDITABLE)
    loyalty_variance = FieldDef('I', FieldType.EDITABLE)
    mission_available = FieldDef('I', FieldType.EDITABLE)  # related to MISSIONSD ?


class ProductionFacilitiesDataDataManager(SWRDataManager):
    filename = "PROFACSD.DAT"
    expected_header = (1, 2, 44, 48)
    expected_md5_checksum = 'eb5418ffb7dcea3eb8a4ed70b003a3cd'

    id = FieldDef('I', FieldType.READ_ONLY)  # 1 for both
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 42
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 43
    family_id = FieldDef('I', FieldType.READ_ONLY)  # 44 for mines and 45 for refineries
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.EDITABLE)
    maintenance = FieldDef('I', FieldType.EDITABLE)  # 0 for both
    research_order = FieldDef('I', FieldType.EDITABLE)   # 0 for both
    unknown_2 = FieldDef('I', FieldType.UNKNOWN)  # maybe research difficulty
    bombardment_defense = FieldDef('I', FieldType.UNKNOWN)  # maybe moral modifier
    production_rate = FieldDef('I', FieldType.EDITABLE)  # required days to manufacture 1 unit


class CharacterBaseDataDataManager(SWRDataManager):
    id = FieldDef('I', FieldType.READ_ONLY)  # starting from 576
    active = FieldDef('I', FieldType.UNKNOWN)  # maybe the active flag, always 1
    producing_facility_family_id = FieldDef('I', FieldType.READ_ONLY)  # always 0
    producing_facility_family_id_one_based = FieldDef('I', FieldType.READ_ONLY)  # always 0
    # 48 for Mon Mothma, 49 for Leia Organa, 50 for Luke Skywalker, 51 for Han Solo, 52 for Emperor Palpatine,
    # 52 for Darth Vader  and 56 for Minor characters
    family_id = FieldDef('I', FieldType.READ_ONLY)
    name_id_1 = FieldDef('H', FieldType.READ_ONLY)  # can be used get the name from Textstrat.dll
    name_id_2 = FieldDef('H', FieldType.READ_ONLY)  # always 2
    alliance = FieldDef('I', FieldType.EDITABLE)
    imperial = FieldDef('I', FieldType.EDITABLE)
    construction_cost = FieldDef('I', FieldType.UNKNOWN)  # always 0
    maintenance = FieldDef('I', FieldType.UNKNOWN)  # always 0
    research_order = FieldDef('I', FieldType.UNKNOWN)  # always 0
    unknown_5 = FieldDef('I', FieldType.UNKNOWN)  # always 0
    diplomacy_base = FieldDef('I', FieldType.EDITABLE)
    diplomacy_variance = FieldDef('I', FieldType.EDITABLE)
    espionage_base = FieldDef('I', FieldType.EDITABLE)
    espionage_variance = FieldDef('I', FieldType.EDITABLE)
    ship_research_base = FieldDef('I', FieldType.EDITABLE)
    ship_research_variance = FieldDef('I', FieldType.EDITABLE)
    troop_research_base = FieldDef('I', FieldType.EDITABLE)
    troop_research_variance = FieldDef('I', FieldType.EDITABLE)
    facility_research_base = FieldDef('I', FieldType.EDITABLE)
    facility_research_variance = FieldDef('I', FieldType.EDITABLE)
    combat_base = FieldDef('I', FieldType.EDITABLE)
    combat_variance = FieldDef('I', FieldType.EDITABLE)
    leadership_base = FieldDef('I', FieldType.EDITABLE)
    leadership_variance = FieldDef('I', FieldType.EDITABLE)
    loyalty_base = FieldDef('I', FieldType.EDITABLE)
    loyalty_variance = FieldDef('I', FieldType.EDITABLE)
    jedi_probability = FieldDef('I', FieldType.EDITABLE)
    known_jedi = FieldDef('I', FieldType.EDITABLE)
    jedi_level_base = FieldDef('I', FieldType.EDITABLE)
    jedi_level_variance = FieldDef('I', FieldType.EDITABLE)
    can_be_admiral = FieldDef('I', FieldType.EDITABLE)
    can_be_commander = FieldDef('I', FieldType.EDITABLE)
    can_be_general = FieldDef('I', FieldType.EDITABLE)
    wont_betray_own_side = FieldDef('I', FieldType.EDITABLE)
    can_train_jedis = FieldDef('I', FieldType.EDITABLE)

    def upgrade_data(self, data_tuple):
        data_dict = OrderedDict(zip(list(self.fields.keys()), data_tuple))
        data_dict.update(
            self.get_texts(
                name=data_dict['name_id_1'],
                name_general=data_dict['name_id_1'] + 28672,
                name_commander=data_dict['name_id_1'] + 26624,
                name_admiral=data_dict['name_id_1'] + 27648,
            )
        )
        return data_dict


class MajorCharacterDataManager(CharacterBaseDataDataManager):
    filename = "MJCHARSD.DAT"
    expected_header = (1, 6, 48, 56)
    expected_md5_checksum = '63b9fa47abd1707abbffe1d0a8f03f4b'


class MinorCharacterDataManager(CharacterBaseDataDataManager):
    filename = "MNCHARSD.DAT"
    expected_header = (1, 54, 56, 60)
    expected_md5_checksum = '3df29ab3d514f2824f43527d96c32bbb'


class SystemFacilityTableDataDataManager(SWRDataManager):
    header_struct_format = "III14s"

    id = FieldDef('I', FieldType.READ_ONLY)
    one = FieldDef('I', FieldType.READ_ONLY)  # always 1
    percent = FieldDef('I', FieldType.READ_ONLY)
    level = FieldDef('H', FieldType.READ_ONLY)
    unknown = FieldDef('B', FieldType.READ_ONLY)  # always 0
    family_id = FieldDef('B', FieldType.READ_ONLY)


class SystemFacilityCoreTableDataManager(SystemFacilityTableDataDataManager):
    filename = "SYFCCRTB.DAT"
    expected_header = (1, 8, 14, b'SeedTableEntry')
    expected_md5_checksum = '2aeb4ffebd247b0dc81e29e3d380b9c8'


class SystemFacilityRimTableDataManager(SystemFacilityTableDataDataManager):
    filename = "SYFCRMTB.DAT"
    expected_header = (1, 7, 14, b'SeedTableEntry')
    expected_md5_checksum = '38f60c0ada2af36ab4eb23eab554ba50'


class AssassinationMissionTableDataManager(ProbabilityTableManager):
    filename = "ASSNMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')
    expected_md5_checksum = '50b57a95d01346b92eed3eb457600ad2'


class AbductionMissionTableDataManager(ProbabilityTableManager):
    filename = "ABDCMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')
    expected_md5_checksum = 'b5c809a85ae68ff810a0699116925ff6'


class DiplomacyMissionTableDataManager(ProbabilityTableManager):
    filename = "DIPLMSTB.DAT"
    expected_header = (1, 10, 13, b'IntTableEntry')
    expected_md5_checksum = '2ce657d774bedac233c01612be93000a'


class DeathStarSabotageMissionTableDataManager(ProbabilityTableManager):
    filename = "DSSBMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')
    expected_md5_checksum = 'f9fe00827aa2045d3122aec5f4335b61'


class EspionageMissionTableDataManager(ProbabilityTableManager):
    filename = "ESPIMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')
    expected_md5_checksum = 'f9fe00827aa2045d3122aec5f4335b61'


class InciteUprisingMissionTableDataManager(ProbabilityTableManager):
    filename = "INCTMSTB.DAT"
    expected_header = (1, 13, 13, b'IntTableEntry')
    expected_md5_checksum = '1f1df0a27ab78493c33816bd9c2dbdf3'


class ReconnaissanceMissionTableDataManager(ProbabilityTableManager):
    filename = "RCRTMSTB.DAT"
    expected_header = (1, 11, 13, b'IntTableEntry')
    expected_md5_checksum = '25aed57916a6e3d37fbc3de5874235fe'


class RescueMissionTableDataManager(ProbabilityTableManager):
    filename = "RESCMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')
    expected_md5_checksum = 'f9fe00827aa2045d3122aec5f4335b61'


class SabotageMissionTableDataManager(ProbabilityTableManager):
    filename = "SBTGMSTB.DAT"
    expected_header = (1, 12, 13, b'IntTableEntry')
    expected_md5_checksum = 'f9fe00827aa2045d3122aec5f4335b61'


class SubdueUprisingMissionTableDataManager(ProbabilityTableManager):
    filename = "SUBDMSTB.DAT"
    expected_header = (1, 13, 13, b'IntTableEntry')
    expected_md5_checksum = '1f1df0a27ab78493c33816bd9c2dbdf3'


class TroopDecoyTableDataManager(ProbabilityTableManager):
    filename = "TDECOYTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')
    expected_md5_checksum = '54fce80164c1df2687658f97a9f6a052'


class FleetDecoyTableDataManager(ProbabilityTableManager):
    filename = "FDECOYTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')
    expected_md5_checksum = '54fce80164c1df2687658f97a9f6a052'


class FoilMissionTableDataManager(ProbabilityTableManager):
    filename = "FOILTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')
    expected_md5_checksum = '9529c4f5933bbfe6784126c3423500cc'


class Uprising1TableDataManager(SimpleTableDataManager):
    filename = "UPRIS1TB.DAT"
    expected_header = (1, 3, 13, b'IntTableEntry')
    expected_md5_checksum = 'dc62ec45b75e57822e48dbe6ace4404f'


class Uprising2TableDataManager(SimpleTableDataManager):
    filename = "UPRIS2TB.DAT"
    expected_header = (1, 4, 13, b'IntTableEntry')
    expected_md5_checksum = 'c50c36b5be1684524bfc62c889654916'


class InformantsTableDataManager(SimpleTableDataManager):
    filename = "INFORMTB.DAT"
    expected_header = (1, 8, 13, b'IntTableEntry')
    expected_md5_checksum = '711482e9e194f98ad33979d83a1b183f'


class EscapeAttemptTableDataManager(ProbabilityTableManager):
    filename = "ESCAPETB.DAT"
    expected_header = (1, 9, 13, b'IntTableEntry')
    expected_md5_checksum = 'a58848ece67376e2250ac628a2436de6'


class ResearchMissionTableDataManager(SimpleTableDataManager):
    filename = "RESRCTB.DAT"
    expected_header = (1, 4, 13, b'IntTableEntry')
    expected_md5_checksum = 'a4f540cdd3f44779c7b7a4f7e876a05d'


class EvadeCaptureTableDataManager(ProbabilityTableManager):
    filename = "RLEVADTB.DAT"
    expected_header = (1, 14, 13, b'IntTableEntry')
    expected_md5_checksum = '46d6a46ac8a4da3ef7ad9ebabfecd067'


class EmpireFleetHomeTableDataManager(GroupedTableManager):
    filename = "CMUNEFTB.DAT"
    expected_header = (1, 1, 20, b'SeedFamilyTableEntry')
    expected_md5_checksum = 'b60d31a01f65232001bac5119e8873f7'


class AllianceFleetHomeTableDataManager(GroupedTableManager):
    filename = "CMUNAFTB.DAT"
    expected_header = (1, 2, 20, b'SeedFamilyTableEntry')
    expected_md5_checksum = '83fd5f8a0d3f067df788d7dab1fff684'
