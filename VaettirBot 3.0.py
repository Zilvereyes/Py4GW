from Py4GWCoreLib import *
import time
from time import sleep

MODULE_NAME = "VaettirBot 3.0"
#region paths

path_points_to_merchant = [(-23041, 14939)]
path_points_to_leave_outpost = [(-24380, 15074), (-26375, 16180)]
path_points_to_traverse_bjora_marches = [
    (17810, -17649), (16582, -17136), (15257, -16568), (14084, -15748), (12940, -14873),
    (11790, -14004), (10640, -13136), (9404 , -12411), (8677 , -11176), (8581 , -9742 ),
    (7892 , -8494 ), (6989 , -7377 ), (6184 , -6180 ), (5384 , -4980 ), (4549 , -3809 ),
    (3622 , -2710 ), (2601 , -1694 ), (1185 , -1535 ), (-251 , -1514 ), (-1690, -1626 ),
    (-3122, -1771 ), (-4556, -1752 ), (-5809, -1109 ), (-6966,  -291 ), (-8390,  -142 ),
    (-9831,  -138 ), (-11272, -156 ), (-12685, -198 ), (-13933,  267 ), (-14914, 1325 ),
    (-15822, 2441 ), (-16917, 3375 ), (-18048, 4223 ), (-19196, 4986 ), (-20000, 5595 ),
    (-20300, 5600 )
]

path_points_to_bounty_giver = [(13367, -20771)]

path_points_to_farming_route1 = [
    (12496, -22600), (11375, -22761), (10925, -23466), (10917, -24311), (9910, -24599),
    (8995, -23177), (8307, -23187), (8213, -22829), (8307, -23187), (8213, -22829),
    (8740, -22475), (8880, -21384), (8684, -20833), (9665, -20415)
]

path_points_to_farming_route2 = [
    (10196, -20124), (9976, -18338, 150), (11316, -18056), (10392, -17512), (10114, -16948),
    (10729, -16273), (10810, -15058), (11120, -15105, 150), (11670, -15457), (12604, -15320),
    (12476, -16157)
]

path_points_to_killing_spot = [
    (13070, -16911), (12938, -17081), (12790, -17201), (12747, -17220),
    (12703, -17239), (12684, -17184), (12526, -17275),
]

#endregion

#region globals
class build:
    deadly_paradox:int = 0
    shadow_form:int = 0
    shroud_of_distress:int = 0
    way_of_perfection:int = 0
    heart_of_shadow:int = 0
    wastrels_demise:int = 0
    arcane_echo:int = 0
    channeling:int = 0

class InventoryConfig:
    def __init__(self):
        self.leave_free_slots = 4
        self.keep_id_kit = 2
        self.keep_salvage_kit = 2
        self.keep_gold_amount = 5000
        
class SellConfig:
    def __init__(self):
        self.sell_whites = True
        self.sell_blues = True
        self.sell_purples = True
        self.sell_golds = False
        self.sell_materials = True
        self.sell_wood = True
        self.sell_iron = True
        self.sell_dust = True
        self.sell_bones = True
        self.sell_cloth = True
        self.sell_granite = True
        
class IDConfig:
    def __init__(self):
        self.id_blues = True
        self.id_purples = True
        self.id_golds = False
        
class SalvageConfig:
    def __init__(self):
        self.salvage_whites = True
        self.salvage_blues = True
        self.salvage_purples = True
        self.salvage_golds = False
        self.salvage_glacial_stones = False
        self.salvage_purple_with_sup_kit = False
        self.salvage_gold_with_sup_kit = False
        
class Botconfig:
    def __init__(self):
        self.in_killing_routine = False
        self.in_waiting_routine = False
        self.in_looting_routine = False

class BOTVARIABLES:
    def __init__(self):
        self.is_script_running = False
        self.log_to_console = True # Controls whether to print to console
        self.action_queue = ActionQueueNode(50)
        self.merchant_queue = ActionQueueNode(750)
        self.salvage_queue = ActionQueueNode(350)
        self.inventory_config = InventoryConfig()
        self.sell_config = SellConfig()
        self.id_config = IDConfig()
        self.salvage_config = SalvageConfig()
        self.config = Botconfig()
        
        self.skillbar = build()
        
bot_variables = BOTVARIABLES()
#endregion

# Instantiate MultiThreading manager
thread_manager = MultiThreading()

#region helpers

def IsSkillBarLoaded():
    global bot_variables
    global skillbar

    primary_profession, secondary_profession = Agent.GetProfessionNames(Player.GetAgentID())
    if primary_profession != "Assassin" and secondary_profession != "Mesmer":
        frame = inspect.currentframe()
        current_function = frame.f_code.co_name if frame else "Unknown"
        ConsoleLog(MODULE_NAME, f"{current_function} - This bot requires A/Me to work, halting.", Py4GW.Console.MessageType.Error, log=True)
        return False

    bot_variables.skillbar.deadly_paradox = Skill.GetID("Deadly_Paradox")
    bot_variables.skillbar.shadow_form = Skill.GetID("Shadow_Form")
    bot_variables.skillbar.shroud_of_distress = Skill.GetID("Shroud_of_Distress")
    bot_variables.skillbar.way_of_perfection = Skill.GetID("Way_of_Perfection")
    bot_variables.skillbar.heart_of_shadow = Skill.GetID("Heart_of_Shadow")
    bot_variables.skillbar.wastrels_demise = Skill.GetID("Wastrel's_Demise")
    bot_variables.skillbar.arcane_echo = Skill.GetID("Arcane_Echo")
    bot_variables.skillbar.channeling = Skill.GetID("Channeling")
    
    ConsoleLog(MODULE_NAME, f"SkillBar Loaded.", Py4GW.Console.MessageType.Info, log=bot_variables.log_to_console)       
    return True

def SetHardMode():
    global bot_variables
    bot_variables.action_queue.add_action(Party.SetHardMode)
    ConsoleLog(MODULE_NAME, "Hard mode set.", Py4GW.Console.MessageType.Info, log=bot_variables.log_to_console)
    
def reset_environment():
    global bot_variables
    bot_variables.is_script_running = False
    bot_variables.action_queue.clear()
    bot_variables.merchant_queue.clear()
    

def NeedsToHandleInventory():
    global bot_variables
    free_slots_in_inventory = Inventory.GetFreeSlotCount()
    count_of_id_kits = Inventory.GetModelCount(5899) #5899 model for ID kit
    count_of_salvage_kits = Inventory.GetModelCount(2992) #2992 model for salvage kit
    items_to_sell = get_filtered_materials_to_sell()
    
    needs_to_handle_inventory = False
    if free_slots_in_inventory < bot_variables.inventory_config.leave_free_slots:
        needs_to_handle_inventory = True
    if count_of_id_kits < bot_variables.inventory_config.keep_id_kit:
        needs_to_handle_inventory = True
    if count_of_salvage_kits < bot_variables.inventory_config.keep_salvage_kit:
        needs_to_handle_inventory = True
    if len(items_to_sell) > 0:
        needs_to_handle_inventory = True
    
    return needs_to_handle_inventory

def GetIDKitsToBuy():
    global bot_variables
    count_of_id_kits = Inventory.GetModelCount(5899) #5899 model for ID kit
    id_kits_to_buy = bot_variables.inventory_config.keep_id_kit - count_of_id_kits
    return id_kits_to_buy

def GetSalvageKitsToBuy():
    global bot_variables
    count_of_salvage_kits = Inventory.GetModelCount(2992) #2992 model for salvage kit
    salvage_kits_to_buy = bot_variables.inventory_config.keep_salvage_kit - count_of_salvage_kits
    return salvage_kits_to_buy

def IsMaterial(item_id):
    material_model_ids = {946, 948, 929, 921, 925, 955}  # Add all known material IDs
    return Item.GetModelID(item_id) in material_model_ids
	
def IsGranite(item_id):
    """Check if the item is granite."""
    granite_model_ids = {955}  # Granite ID
    return Item.GetModelID(item_id) in granite_model_ids
	
def IsWood(item_id):
    """Check if the item is wood."""
    wood_model_ids = {946}  # Replace with the correct IDs for wood
    return Item.GetModelID(item_id) in wood_model_ids

def IsIron(item_id):
    """Check if the item is iron."""
    iron_model_ids = {948}  # Replace with the correct IDs for iron
    return Item.GetModelID(item_id) in iron_model_ids

def IsDust(item_id):
    """Check if the item is glittering dust."""
    dust_model_ids = {929}  # Replace with the correct IDs for dust
    return Item.GetModelID(item_id) in dust_model_ids

def IsBones(item_id):
    """Check if the item is bones."""
    bone_model_ids = {921}  # Replace with the correct IDs for bones
    return Item.GetModelID(item_id) in bone_model_ids

def IsCloth(item_id):
    """Check if the item is cloth."""
    cloth_model_ids = {925}  # Replace with the correct IDs for cloth
    return Item.GetModelID(item_id) in cloth_model_ids


def get_filtered_materials_to_sell():
    global bot_variables
    # Get items from the specified bags
    bags_to_check = ItemArray.CreateBagList(1, 2, 3, 4)
    items_to_sell = ItemArray.GetItemArray(bags_to_check)

    # Filter materials first using the centralized definition
    items_to_sell = ItemArray.Filter.ByCondition(items_to_sell, lambda item_id: IsMaterial(item_id))

    # Apply individual material filters
    filtered_items = []
    if bot_variables.sell_config.sell_wood:
        filtered_items.extend(ItemArray.Filter.ByCondition(items_to_sell, IsWood))
    if bot_variables.sell_config.sell_iron:
        filtered_items.extend(ItemArray.Filter.ByCondition(items_to_sell, IsIron))
    if bot_variables.sell_config.sell_dust:
        filtered_items.extend(ItemArray.Filter.ByCondition(items_to_sell, IsDust))
    if bot_variables.sell_config.sell_bones:
        filtered_items.extend(ItemArray.Filter.ByCondition(items_to_sell, IsBones))
    if bot_variables.sell_config.sell_cloth:
        filtered_items.extend(ItemArray.Filter.ByCondition(items_to_sell, IsCloth))
    if bot_variables.sell_config.sell_granite:
        filtered_items.extend(ItemArray.Filter.ByCondition(items_to_sell, IsGranite))
        
    return filtered_items

def filter_identify_array():
    global bot_variables
    bags_to_check = ItemArray.CreateBagList(1,2,3,4)
    unidentified_items = ItemArray.GetItemArray(bags_to_check)
    unidentified_items = ItemArray.Filter.ByCondition(unidentified_items, lambda item_id: not Item.Rarity.IsWhite(item_id))
    unidentified_items = ItemArray.Filter.ByCondition(unidentified_items, lambda item_id: not Item.Usage.IsIdentified(item_id))

    if not bot_variables.id_config.id_blues:
        unidentified_items = ItemArray.Filter.ByCondition(unidentified_items, lambda item_id: not Item.Rarity.IsBlue(item_id))
    if not bot_variables.id_config.id_purples:
        unidentified_items = ItemArray.Filter.ByCondition(unidentified_items, lambda item_id: not Item.Rarity.IsPurple(item_id))
    if not bot_variables.id_config.id_golds:
        unidentified_items = ItemArray.Filter.ByCondition(unidentified_items, lambda item_id: not Item.Rarity.IsGold(item_id))          
    return unidentified_items

def filter_salvage_array():
    global bot_variables
    bags_to_check = ItemArray.CreateBagList(1,2,3,4)
    salvageable_items = ItemArray.GetItemArray(bags_to_check)
    salvageable_items = ItemArray.Filter.ByCondition(salvageable_items, lambda item_id: Item.Usage.IsIdentified(item_id))
    salvageable_items = ItemArray.Filter.ByCondition(salvageable_items, lambda item_id: Item.Usage.IsSalvageable(item_id))

    if not bot_variables.salvage_config.salvage_blues:
        salvageable_items = ItemArray.Filter.ByCondition(salvageable_items, lambda item_id: not Item.Rarity.IsBlue(item_id))
    if not bot_variables.salvage_config.salvage_purples:
        salvageable_items = ItemArray.Filter.ByCondition(salvageable_items, lambda item_id: not Item.Rarity.IsPurple(item_id))
    if not bot_variables.salvage_config.salvage_golds:
        salvageable_items = ItemArray.Filter.ByCondition(salvageable_items, lambda item_id: not Item.Rarity.IsGold(item_id))
    return salvageable_items
        
def filter_items_to_deposit():
    bags_to_check = ItemArray.CreateBagList(1,2,3,4)
    items_to_deposit = ItemArray.GetItemArray(bags_to_check)
    banned_models = {2992,5899}
    items_to_deposit = ItemArray.Filter.ByCondition(items_to_deposit, lambda item_id: Item.GetModelID(item_id) not in banned_models)
    return items_to_deposit

def player_is_dead_or_map_loading():
    return Agent.IsDead(Player.GetAgentID()) or Map.IsMapLoading()
    
def player_is_dead():
    return Agent.IsDead(Player.GetAgentID())

def handle_death():
    if Agent.IsDead(Player.GetAgentID()):
        ConsoleLog(MODULE_NAME, f"Player is dead while traversing {Map.GetMapName(Map.GetMapID())} . Reseting Environment.", Py4GW.Console.MessageType.Error, log=bot_variables.log_to_console)
        reset_environment()
        return True
    return False
#endregion
  

#region Sequential coding
def RunBotSequentialLogic():
    """Thread function that manages counting based on ImGui button presses."""
    global MAIN_THREAD_NAME, bot_variables

    while True:
        if not bot_variables.is_script_running:
            sleep(1)
            continue
        
        #movement and follow objects
        path_to_merchant = Routines.Movement.PathHandler(path_points_to_merchant)
        path_to_leave_outpost = Routines.Movement.PathHandler(path_points_to_leave_outpost)
        path_to_traverse_bjora_marches = Routines.Movement.PathHandler(path_points_to_traverse_bjora_marches)
        path_to_quest_giver = Routines.Movement.PathHandler(path_points_to_bounty_giver)
        path_to_farming_route1 = Routines.Movement.PathHandler(path_points_to_farming_route1)
        path_to_farming_route2 = Routines.Movement.PathHandler(path_points_to_farming_route2)
        path_to_killing_spot = Routines.Movement.PathHandler(path_points_to_killing_spot)
        follow_object = Routines.Movement.FollowXY()
        action_queue = bot_variables.action_queue
        merchant_queue = bot_variables.merchant_queue
        salvage_queue = bot_variables.salvage_queue
        log_to_console = bot_variables.log_to_console
        
        
        longeyes_ledge = 650 #Longeyes Ledge
        Routines.Sequential.Map.TravelToOutpost(longeyes_ledge, action_queue, log_to_console)
        Routines.Sequential.Skills.LoadSkillbar("OwVUI2h5lPP8Id2BkAiAvpLBTAA", action_queue,log_to_console)
        
        if not IsSkillBarLoaded():
            reset_environment()
            ConsoleLog(MODULE_NAME, "You need the following build: OwVUI2h5lPP8Id2BkAiAvpLBTAA", Py4GW.Console.MessageType.Error, log=True)
            break
        
        Routines.Sequential.Map.SetHardMode(action_queue, log_to_console)
        Routines.Sequential.Player.SetTitle(TitleID.Norn.value, action_queue, log_to_console)
                
        #inventory management  
        if NeedsToHandleInventory():
            #going to merchant
            Routines.Sequential.Movement.FollowPath(path_to_merchant, 
                                                    follow_object, 
                                                    bot_variables.action_queue)        
            Routines.Sequential.Agents.TargetNearestNPC(Range.Earshot.value,bot_variables.action_queue)
            Routines.Sequential.Player.InteractTarget(bot_variables.action_queue)
            
            if bot_variables.sell_config.sell_materials:
                items_to_sell = get_filtered_materials_to_sell()
                #sell materials to make space
                Routines.Sequential.Merchant.SellItems(items_to_sell, merchant_queue, log_to_console)
            Routines.Sequential.Merchant.BuyIDKits(GetIDKitsToBuy(),merchant_queue, log_to_console)
            Routines.Sequential.Merchant.BuySalvageKits(GetSalvageKitsToBuy(),merchant_queue, log_to_console)
            
            items_to_idenfity = filter_identify_array()
            Routines.Sequential.Items.IdentifyItems(items_to_idenfity, salvage_queue, log_to_console)
            
            items_to_salvage = filter_salvage_array()
            Routines.Sequential.Items.SalvageItems(items_to_salvage, salvage_queue, log_to_console)
            
            if bot_variables.sell_config.sell_materials:
                items_to_sell = get_filtered_materials_to_sell()
                Routines.Sequential.Merchant.SellItems(items_to_sell, merchant_queue,log_to_console)
                
            items_to_deposit = filter_items_to_deposit()
            Routines.Sequential.Items.DepositItems(items_to_deposit,salvage_queue,log_to_console)
            Routines.Sequential.Items.DepositGold(bot_variables.inventory_config.keep_gold_amount,salvage_queue, log_to_console)
        
        #exit outpost
        Routines.Sequential.Movement.FollowPath(path_handler= path_to_leave_outpost, movement_object = follow_object, action_queue = action_queue, custom_exit_condition=lambda: Map.IsMapLoading())
        bjora_marches = 482 #Bjora Marches
        Routines.Sequential.Map.WaitforMapLoad(bjora_marches, bot_variables.log_to_console)
        #traverse bjora marches
        Routines.Sequential.Movement.FollowPath(path_to_traverse_bjora_marches, follow_object, action_queue, custom_exit_condition=lambda: player_is_dead_or_map_loading())
        
        if handle_death():
            continue
        
        jaga_moraine = 546 #Jaga Moraine
        Routines.Sequential.Map.WaitforMapLoad(jaga_moraine, bot_variables.log_to_console)
        #take bounty
        
        Routines.Sequential.Movement.FollowPath(path_to_quest_giver, follow_object,action_queue)
        Routines.Sequential.Agents.TargetNearestNPC(Range.Earshot.value, bot_variables.action_queue)
        Routines.Sequential.Player.InteractTarget(bot_variables.action_queue)
        Routines.Sequential.Player.SendDialog("0x84", bot_variables.action_queue)
        
        Routines.Sequential.Movement.FollowPath(path_to_farming_route1,follow_object,action_queue,custom_exit_condition=lambda: player_is_dead())
        if handle_death():
            continue
        
        #wait for aggro ball'
        ConsoleLog(MODULE_NAME, "Waiting for left aggro ball", Py4GW.Console.MessageType.Info, log=log_to_console)
        sleep (15)
        
        Routines.Sequential.Movement.FollowPath(path_to_farming_route2,follow_object,action_queue,custom_exit_condition=lambda: player_is_dead())
        if handle_death():
            continue
        
        ConsoleLog(MODULE_NAME, "Waiting for right aggro ball", Py4GW.Console.MessageType.Info, log=log_to_console)
        sleep (15)
        
        Routines.Sequential.Movement.FollowPath(path_to_killing_spot,follow_object,action_queue)
        bot_variables.config.in_killing_routine = True
        player_pos = Player.GetXY()
        enemy_array = Routines.Agents.GetFilteredEnemyArray(player_pos[0],player_pos[1],Range.Spellcast.value)
        while len(enemy_array) > 3: #sometimes not all enemies are killed
            sleep(1)
            enemy_array = Routines.Agents.GetFilteredEnemyArray(player_pos[0],player_pos[1],Range.Spellcast.value)
        
        bot_variables.config.in_killing_routine = False
        
        #loot
        #salvage
        #exit jaga
        #return to jaga
        #restart loop
 
        
        bot_variables.is_script_running = False
        ConsoleLog(MODULE_NAME, "Script finished.", Py4GW.Console.MessageType.Info, log=bot_variables.log_to_console)
        time.sleep(0.1)
#endregion

#region SkillCasting
def BjoraMarchesSkillCasting():
    global bot_variables
    #we only need to cast skills in bjora marches if we are in danger
    if not Routines.Checks.Agents.InDanger(Range.Earshot):
        sleep(0.1)
        return
    
    player_agent_id = Player.GetAgentID()
    deadly_paradox = bot_variables.skillbar.deadly_paradox
    shadow_form = bot_variables.skillbar.shadow_form
    shroud_of_distress = bot_variables.skillbar.shroud_of_distress
    heart_of_shadow = bot_variables.skillbar.heart_of_shadow

    action_queue = bot_variables.action_queue
    log_to_console = bot_variables.log_to_console
    

    #we need to cast deadly paradox and shadow form and mantain it
    has_shadow_form = Routines.Checks.Effects.HasBuff(player_agent_id,shadow_form)
    shadow_form_buff_time_remaining = Effects.GetEffectTimeRemaining(player_agent_id,shadow_form) if has_shadow_form else 0

    has_deadly_paradox = Routines.Checks.Effects.HasBuff(player_agent_id,deadly_paradox)
    if shadow_form_buff_time_remaining <= 3500: #about to expire, recast
        #** Cast Deadly Paradox **
        if Routines.Sequential.Skills.CastSkillID(deadly_paradox,action_queue,extra_condition=(not has_deadly_paradox), log=log_to_console):             
            sleep(0.1)   
        # ** Cast Shadow Form **
        if Routines.Sequential.Skills.CastSkillID(shadow_form,action_queue, log=log_to_console):
            sleep(1.25)
        
    #if were hurt, we need to cast shroud of distress 
    if Agent.GetHealth(player_agent_id) < 0.45:
        # ** Cast Shroud of Distress **
        if Routines.Sequential.Skills.CastSkillID(shroud_of_distress,action_queue, log=log_to_console):
            sleep(1.25)

    #if we have an enemy behind us, we can escape with Heart of Shadow
    nearest_enemy = Routines.Agents.GetNearestEnemy(Range.Earshot.value)
    if nearest_enemy:
        # ** Cast Heart of Shadow **
        is_enemy_behind = Routines.Checks.Agents.IsEnemyBehind(player_agent_id)
        if Routines.Sequential.Skills.CastSkillID(heart_of_shadow,action_queue, extra_condition=is_enemy_behind, log=log_to_console):
            sleep(0.350)
            
     # ** Killing Routine **
    if bot_variables.config.in_killing_routine:
        arcane_echo_slot = 7
        wastrels_demise_slot = 6
        both_ready = Routines.Checks.Skills.IsSkillSlotReady(wastrels_demise_slot) and Routines.Checks.Skills.IsSkillSlotReady(arcane_echo_slot)
        if Routines.Sequential.Skills.CastSkillSlot(arcane_echo_slot,action_queue, extra_condition=both_ready, log=log_to_console):
            sleep(0.350)
            
        if Routines.Sequential.Skills.CastSkillSlot(wastrels_demise_slot,action_queue, extra_condition=both_ready, log=log_to_console):
            sleep(0.350)


def JagaMoraineSkillCasting():
    player_agent_id = Player.GetAgentID()
    deadly_paradox = bot_variables.skillbar.deadly_paradox
    shadow_form = bot_variables.skillbar.shadow_form
    shroud_of_distress = bot_variables.skillbar.shroud_of_distress
    way_of_perfection = bot_variables.skillbar.way_of_perfection
    heart_of_shadow = bot_variables.skillbar.heart_of_shadow
    wastrels_demise = bot_variables.skillbar.wastrels_demise
    arcane_echo = bot_variables.skillbar.arcane_echo
    channeling = bot_variables.skillbar.channeling
    
    action_queue = bot_variables.action_queue
    log_to_console = bot_variables.log_to_console
    
    if Routines.Checks.Agents.InDanger(Range.Spellcast):
        #we need to cast deadly paradox and shadow form and mantain it
        has_shadow_form = Routines.Checks.Effects.HasBuff(player_agent_id,shadow_form)
        shadow_form_buff_time_remaining = Effects.GetEffectTimeRemaining(player_agent_id,shadow_form) if has_shadow_form else 0

        has_deadly_paradox = Routines.Checks.Effects.HasBuff(player_agent_id,deadly_paradox)
        if shadow_form_buff_time_remaining <= 3500: #about to expire, recast
            #** Cast Deadly Paradox **
            if Routines.Sequential.Skills.CastSkillID(deadly_paradox,action_queue,extra_condition=(not has_deadly_paradox), log=log_to_console):
                sleep(0.1)
            
            # ** Cast Shadow Form **
            if Routines.Sequential.Skills.CastSkillID(shadow_form,action_queue, log=log_to_console):
                sleep(1.25)
                
    #if were hurt, we need to cast shroud of distress 
    if Agent.GetHealth(player_agent_id) < 0.45:
        # ** Cast Shroud of Distress **
        if Routines.Sequential.Skills.CastSkillID(shroud_of_distress,action_queue, log =log_to_console):
            sleep(1.25)
            
    #need to keep Channeling up
    has_channeling = Routines.Checks.Effects.HasBuff(player_agent_id,bot_variables.skillbar.channeling)
    if not has_channeling:
        # ** Cast Channeling **
        if Routines.Sequential.Skills.CastSkillID(channeling,action_queue, log =log_to_console):
            sleep(1.25)
            
    #Keep way of perfection up on recharge
    # ** Cast Way of Perfection **
    if Routines.Sequential.Skills.CastSkillID(way_of_perfection,action_queue, log=log_to_console):
        sleep(0.350)
        
    # ** Heart of Shadow to Stay Alive **
    if not bot_variables.config.in_killing_routine:
        if Agent.GetHealth(player_agent_id) < 0.35:
            if bot_variables.config.in_waiting_routine:
                Routines.Sequential.Agents.ChangeTarget(player_agent_id, bot_variables.action_queue)
            else:
                Routines.Sequential.Agents.TargetNearestEnemy(Range.Earshot.value,bot_variables.action_queue)

            if Routines.Sequential.Skills.CastSkillID(heart_of_shadow,action_queue, log=log_to_console):
                sleep(0.350)
                
    # ** Killing Routine **
    if bot_variables.config.in_killing_routine:
        arcane_echo_slot = 7
        wastrels_demise_slot = 6
        both_ready = Routines.Checks.Skills.IsSkillSlotReady(wastrels_demise_slot) and Routines.Checks.Skills.IsSkillSlotReady(arcane_echo_slot)
        if Routines.Sequential.Skills.CastSkillSlot(arcane_echo_slot,action_queue, extra_condition=both_ready, log=log_to_console):
            sleep(0.350)
            
        if Routines.Sequential.Skills.CastSkillSlot(wastrels_demise_slot,action_queue, extra_condition=both_ready, log=log_to_console):
            sleep(0.350)

#endregion

def SkillHandler():
    """Thread function that manages counting based on ImGui button presses."""
    global MAIN_THREAD_NAME, bot_variables
    while True:
        bjora_marches = 482 #Bjora Marches
        jaga_moraine = 546 #Jaga Moraine
        
        if not (Map.IsMapReady() and Party.IsPartyLoaded() and Map.IsExplorable()):
            #if not in explorable area, no need to cast skills, skip this iteration
            sleep(1)
            continue
        
        #if we are occupied with something else, skip this iteration
        if not Routines.Checks.Skills.CanCast():
            sleep(0.1)
            continue
        
        if Map.GetMapID() == bjora_marches:
            BjoraMarchesSkillCasting()
            sleep(0.1)
        elif Map.GetMapID() == jaga_moraine:    
            JagaMoraineSkillCasting()

        


#region Watchdog
def watchdog_fn():
    """Daemon thread that monitors all active threads and shuts down unresponsive ones."""
    global MAIN_THREAD_NAME

    Py4GW.Console.Log("Watchdog", "Watchdog started.", Py4GW.Console.MessageType.Info)

    while True:
        current_time = time.time()
        expired_threads = []

        if Map.IsMapLoading():
            Py4GW.Console.Log("Watchdog", "Map is loading - refreshing keepalive for all threads.", Py4GW.Console.MessageType.Notice)
            with thread_manager.lock:
                # Refresh all threads' keepalive timestamps
                for name, info in thread_manager.threads.items():
                    if name == "watchdog":
                        continue
                    thread_manager.threads[name]["last_keepalive"] = current_time
        else:
            # Normal operation: check for expiration
            with thread_manager.lock:
                for name, info in thread_manager.threads.items():
                    if name == "watchdog":
                        continue

                    last_keepalive = info["last_keepalive"]
                    if current_time - last_keepalive > thread_manager.timeout:
                        expired_threads.append(name)

        # First, log and stop any expired threads (other than main thread)
        for name in expired_threads:
            if name != MAIN_THREAD_NAME:
                ConsoleLog("Watchdog", f"Thread '{name}' timed out. Stopping it.", Console.MessageType.Warning, log=True)
                thread_manager.stop_thread(name)

        # Special case: if MAIN_THREAD_NAME itself timed out → stop EVERYTHING
        if MAIN_THREAD_NAME in expired_threads:
            ConsoleLog("Watchdog", f"Main thread '{MAIN_THREAD_NAME}' timed out! Stopping all threads.", Console.MessageType.Error, log=True)
            thread_manager.stop_all_threads()
            break  # Exit Watchdog itself naturally

        time.sleep(1)  # Adjust interval as needed
#endregion


MAIN_THREAD_NAME = "RunBotSequentialLogic"
thread_manager.add_thread(MAIN_THREAD_NAME, RunBotSequentialLogic)
thread_manager.add_thread("SkillHandler", SkillHandler)
thread_manager.add_thread("watchdog", watchdog_fn)

#region ImGui
def DrawWindow():
    """ImGui draw function that runs every frame."""
    global bot_variables, MAIN_THREAD_NAME
    
    flags = PyImGui.WindowFlags.NoScrollbar | PyImGui.WindowFlags.NoScrollWithMouse | PyImGui.WindowFlags.AlwaysAutoResize
    if PyImGui.begin("Py4GW", flags):       
        button_text = "Start script" if not bot_variables.is_script_running else "Stop script"
        if PyImGui.button(button_text):
            bot_variables.is_script_running = not bot_variables.is_script_running      
            if bot_variables.is_script_running:
                # --- ONLY start threads, they are already added at script load ---
                thread_manager.start_thread(MAIN_THREAD_NAME)
                thread_manager.start_thread("SkillHandler")
                thread_manager.start_thread("watchdog")
            else:
                # Stop all threads
                reset_environment()
                thread_manager.stop_all_threads()
                     

    PyImGui.end()
#endregion


def main():
    global MAIN_THREAD_NAME
    global bot_variables
    try:
        if bot_variables.is_script_running:
            thread_manager.update_keepalive(MAIN_THREAD_NAME)
            thread_manager.update_keepalive("SkillHandler")

        DrawWindow()
        
        if bot_variables.action_queue.action_queue_timer.HasElapsed(bot_variables.action_queue.action_queue_time):
            bot_variables.action_queue.execute_next()
        
        if bot_variables.salvage_queue.action_queue_timer.HasElapsed(bot_variables.salvage_queue.action_queue_time):
            if not bot_variables.salvage_queue.is_empty():
                bot_variables.salvage_queue.execute_next()
        
        if bot_variables.merchant_queue.action_queue_timer.HasElapsed(bot_variables.merchant_queue.action_queue_time):
            if not bot_variables.merchant_queue.is_empty():
                bot_variables.merchant_queue.execute_next()
                ConsoleLog(MODULE_NAME, "Item sold.", Py4GW.Console.MessageType.Info, log=bot_variables.log_to_console)
            
    except Exception as e:
        ConsoleLog(MODULE_NAME,f"Error: {str(e)}",Py4GW.Console.MessageType.Error,log=True)

if __name__ == "__main__":
    main()