#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================



#==================================================
#  AGENT
#==================================================

# --- Constants ---

MAX_IDX = 3
METABOLISM_IDX = 0
VISION_IDX = 1
SUGAR_LEVEL_IDX = 2
POSITION_IDX = 3

# --- Private functions --- 

def __get_property(agent, property_idx):
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid agent property index.")
    return agent[property_idx]

def __set_property(agent, property_idx, value):
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid agent property index.")
    agent[property_idx] = value    

def __empty_instance():
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---

def get_metabolism(agent):
    """
       return the metabolism of the agent.

    """
    return __get_property ( agent, METABOLISM_IDX )
    

def set_metabolism ( agent, metabolism ):
    """
       Set the metabolism of the agent
    """
    pop = get_pop(agent)
    if metabolism < 0:
        raise Exception("The metabolism of an agent cannot be negative.")
    if metabolism > p.get_max_metabolism(pop):
        print("meta = ",metabolism,"   max = ",p.get_max_capacity(pop))
        raise Exception("The metabolism of a cell cannot exceed the maximum metabolism for the population.")
    __set_property ( agent, METABOLISM_IDX, metabolism )

def get_vision ( agent ):
    """
       return the vision of the agent.

    """
    return __get_property ( agent, VISION_IDX )
   
def set_vision ( agent, vision ):
    """
       Set the vision of the agent
    """
    __set_property ( agent, VISION_IDX, vision )
    
def get_sugar_level(agent):
    """
       return the metabolism of the agent.

    """
    return __get_property(agent, SUGAR_LEVEL_IDX)

def set_sugar_level ( agent, level ):
    """
       Set the sugar level of the agent
    """
    if level < 0 :
        raise Exception ("Error:The sugar level of an agent cannot be negative.")
    elif level > get_metabolism (agent) :
        raise Exception("Error: The sugar level of an agent cannot exceed its metabolism.")
    __set_property ( agent, SUGAR_LEVEL_IDX, level )

def get_position ( agent ):
    """
       return the position of the agent.

    """
    print("mas_agent.", "get_position()")
    return __get_property (agent, POSITION_IDX)
    
def set_position ( agent, position ):
    """
       Set the position of the agent
    """
    print("mas_agent.", "set_position()")
    __set_property(agent, POSITION_IDX, position)
    
def new_instance():
    print("mas_agent.", "new_instance()")
    agent = __empty_instance()
    agent[METABOLISM_IDX] = 0.0
    agent[VISION_IDX] = 2
    agent[SUGAR_LEVEL_IDX] = 0.0
    agent[POSITION_IDX] = (0,0)
    return agent