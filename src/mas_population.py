#==================================================
# INFO-H-100 - Introduction à l'informatique
# 
# Prof. Thierry Massart
# Année académique 2014-2015
#
# Projet: Système Multi-Agent (SMA)
#
#==================================================

import mas as m
import mas_cell as c
import mas_agent as a
import mas_environment as e

#==================================================
#  AGENT pop
#==================================================

# --- Constants ---

MAX_IDX = 1
AGENTS_IDX = 0
ENV_IDX = 1

# --- Private functions ---

def __get_property(pop, property_idx):
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid pop property index.")
    return pop[property_idx]
    
def __set_property(pop, property_idx, value):
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid pop property index.")
    pop[property_idx] = value

def __empty_instance():
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---

def get_agents(pop):
    return __get_property(pop, AGENTS_IDX)

def set_agents(pop, agents):
    __set_property(pop, AGENTS_IDX, agents)

def get_env( pop ):
    return __get_property(pop, ENV_IDX)

def set_env(pop, env):
    __set_property(pop, ENV_IDX, env)

# --- Initialisation ---

def new_instance(mas, sz):
    """
        Return a new pop instance of size "sz" and 
        "declare" to which MAS it belongs to.
    """
    env = m.get_env(mas)
    
    agents = []
    for i in range( sz ):
        agent = a.random_agent()
        cell_ref = e.random_cell_ref_without_agent(env)
        a.set_pos(agent, cell_ref )
        cell = e.get_cell(env, cell_ref )
        c.set_present_agent(cell, agent)
        
        agents.append(agent)
    
    pop = __empty_instance()
    set_agents(pop, agents)
    set_env(pop, env)
    
    return pop


# --- Rules ---
def apply_rule(pop, agent_rule):
    """
        Apply the function agent_rule to all agent of the population.
    """
    for agent in get_agents(pop):
        agent_rule( get_env(pop), agent)
        
        
        
