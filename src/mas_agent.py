#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

import random
import mas_environment as e
import mas_cell as c

#==================================================
#  AGENT
#==================================================

# --- Constants ---

MAX_IDX = 4
METABOLISM_IDX = 0
VISION_IDX = 1
SUGAR_LEVEL_IDX = 2
POS_IDX = 3
IS_LIVING_IDX = 4

#------ Defaults--------

METABOLISM_MIN = 0.1
METABOLISM_MAX = 0.3
VISION_MIN=3
VISION_MAX=10


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
    

def set_sugar_level ( agent, sugar_level ):
    """
       Set the sugar level of the agent
    """
    __set_property ( agent, SUGAR_LEVEL_IDX, sugar_level )

    
def get_pos ( agent ):
    """
       return the pos of the agent.

    """
    return __get_property ( agent, POS_IDX )
    

def set_pos ( agent, pos ):
    """
       Set the pos of the agent
    """
    __set_property ( agent, POS_IDX, pos )

def get_is_living (agent):
    return __get_property(agent, IS_LIVING_IDX)

def set_is_living(agent, is_living):
    __set_property(agent, IS_LIVING_IDX, is_living)
    
# --- Initialisation ---


def empty_agent():
    """
        création d 'un agent avec des valeurs de bases
    """
    agent = __empty_instance()
    set_metabolism(agent, 0.0)
    set_vision(agent, 2)
    set_sugar_level(agent, 0.0)
    set_pos(agent, (0,0))
    set_is_living(agent, True )
    return agent
    
def random_agent():
    agent = empty_agent()
    set_metabolism(agent, random.uniform(METABOLISM_MIN, METABOLISM_MAX))
    set_vision(agent, random.randint(VISION_MIN, VISION_MAX))
    return agent
      
# --- Vectors operators ---

def vector_sum(vec1,vec2):
    dim = len(vec1)
    res = []
    for i in range(dim):
        res.append(vec1[i] + vec2[i])
    return res
    
def vector_list_sum(vec_list, vec_add):
    # Adds vec_add to each vector in vec_list
    res = []
    for vec in vec_list:
        res.append(vector_sum(vec,vec_add))
    return res

# --- Rules ---

def move_to_highest_sugar_level_cell( env, agent ):
    agent_pos = get_pos(agent)
    moves_list = possible_moves( env, agent )
    if len(moves_list) > 0:
        possible_cell_refs = vector_list_sum(moves_list, agent_pos)
        target_cell_ref = e.max_sugar_level_cell_ref(env,possible_cell_refs)
        agent_move_to(env, agent, target_cell_ref)
    else:
        print(agent, "meurs")#agent_kill(mas,agent_ref)
    
    
# --- Movement ---

def possible_moves( env, agent ):
    vision = get_vision(agent)
    moves_list = []
    for move in range(-vision,vision+1):
        if move!=0:
            if move_is_possible( env, agent, (move,0) ):
                moves_list.append( (move,0) )
            if move_is_possible( env, agent, (0,move) ):
                moves_list.append( (0,move) )
    return moves_list
    
def move_is_possible( env, agent, move_vec):
    cell_ref = get_pos(agent)
    cell_ref = vector_sum(cell_ref, move_vec)
    return agent_move_to_is_possible(env, agent, cell_ref)
    
def agent_move_to_is_possible(env, agent, cell_ref):
    cell = e.get_cell( env, cell_ref )
    move_possible = not c.agent_is_present(cell) and get_metabolism(agent) < c.get_sugar_level(cell)
    return move_possible    

def agent_move_to(env, agent, target_cell_ref):
    if agent_move_to_is_possible(env, agent, target_cell_ref):
        cell_ref = get_pos(agent)
        cell_old = e.get_cell(env, cell_ref)
        cell_new = e.get_cell(env, target_cell_ref)
        # "Clean-up" the cell when leaving
        c.set_present_agent(cell_old, None)
        # Move and "declare" presence to target cell 
        set_pos(agent, target_cell_ref)
        c.set_present_agent(cell_new, agent)
    else:
        raise Exception("Error: An agent has tried to move to a cell that is not allowed!")
