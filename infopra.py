import mas_population as p


AGENT_MAX_IDX = 3
AGENT_METABOLISM_IDX = 0
AGENT_VISION_IDX = 1
AGENT_SUGAR_LEVEL_IDX = 2
AGENT_POSITION_IDX = 3

# --- Private functions --- 

def __get_property(agent, property_idx):
    if not (0 <= property_idx <= AGENT_MAX_IDX):
        raise Exception("Invalid agent property index.")
    return agent[property_idx]

def __set_property(agent, property_idx, value):
    if not (0 <= property_idx <= AGENT_MAX_IDX):
        raise Exception("Invalid agent property index.")
    agent[property_idx] = value    

def __agent_empty_instance():
    return [None]*(AGENT_MAX_IDX+1)

# --- Getters and setters ---

def new_agent():
    agent = __agent_empty_instance()
    agent[AGENT_METABOLISM_IDX] = 0.0
    agent[AGENT_VISION_IDX] = 2
    agent[AGENT_SUGAR_LEVEL_IDX] = 0.0
    agent[AGENT_POSITION_IDX] = (0,0)
    return agent
# --- getters and setters ---

def get_metabolism(agent):
    """
       return the metabolism of the agent.

    """
    return __get_property ( agent, AGENT_METABOLISM_IDX )
    

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
    __set_property ( agent, AGENT_METABOLISM_IDX, metabolism )

def get_vision ( agent ):
    """
       return the vision of the agent.

    """
    return __get_property ( agent, AGENT_VISION_IDX )
   
def set_vision ( agent, vision ):
    """
       Set the vision of the agent
    """
    __set_property ( agent, AGENT_VISION_IDX, vision )
    
def get_sugar_level(agent):
    """
       return the metabolism of the agent.

    """
    return __get_property(agent, AGENT_SUGAR_LEVEL_IDX)
    

def set_sugar_level ( agent, sugar_level ):
    """
       Set the sugar level of the agent
    """
    if sugar_level < 0 :
        raise Exception ("Error:The sugar_level of an agent cannot be negative.")
    elif sugar_level > get_metabolism (agent) :
        raise Exception("Error: The sugar level of an agent cannot exceed its metabolism.")
    __set_property ( agent, AGENT_SUGAR_LEVEL_IDX, sugar_level )

    
def get_position ( agent ):
    """
       return the position of the agent.

    """
    return __get_property ( agent, AGENT_POSITION_IDX )
    

def set_position ( agent, position ):
    """
       Set the position of the agent
    """
    
    
    
