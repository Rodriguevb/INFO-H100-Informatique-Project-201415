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
import mas_agent as a
import mas_cell as c
import mas_environment as e
import mas_utils as u
import random 

#==================================================
#  AGENT POPULATION
#==================================================

# --- Constants ---

MAX_IDX = 1
AGENTS_IDX = 0
ENV_IDX = 1

# --- Private functions ---

def __get_property(population, property_idx):
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid population property index.")
    return population[property_idx]
    
def __set_property(population, property_idx, value):
    if not (0 <= property_idx <= MAX_IDX):
        raise Exception("Invalid population property index.")
    population[property_idx] = value

def __empty_instance():
    return [None]*(MAX_IDX+1)

# --- Getters and setters ---

def get_agents(population):
    return __get_property(population, AGENTS_IDX)

def set_agents(population, AGENTS):
    __set_property(population, AGENTS_IDX, AGENTS)

def get_env( population ):
    return __get_property(population, ENV_IDX)

def set_env(population, env):
    __set_property(population, ENV_IDX, env)

# --- Initialisation ---

def new_instance(mas, sz):
    """
        Return a new population instance of size "sz" and 
        "declare" to which MAS it belongs to.
    """
    env = m.get_env( mas )
    
    agents = [] # Les 'sz' agents
    for x in range ( sz ):
        cell_ref = e.random_cell_ref_without_agent(env) # On récupère la position d'une cellule sans agent
        agent = a.new_random()                          # On crée un agent avec des valeurs aléatoires
        a.set_pos( agent, cell_ref )                    # On modifie la position de l'agent
        cell = e.get_cell( env, cell_ref )              # On récupère la cellule (liste) via la position             
        c.set_present_agent( cell, agent )              # On indique à la cellule qu'un agent est présent
        agents.append ( agent )                         # On ajoute l'agent dans la liste des 'sz' agents

    population = __empty_instance()
    set_agents( population, agents )
    set_env( population, env )
    
    return population

# --- Others ---

def remove_agent(population, agent):
    agents = get_agents(population)
    agents.remove(agent)

# --- Rules ---

def apply_rule(pop, agent_rule):
    """
        Applique la fonction agent_rule sur chaque agent de la population.
    """
    env = get_env(pop)
    agents = get_agents(pop)
    
    ########################################################
    
    # On change l'ordre de mouvement des agents
    
    #OA1( agents ) # OA1: l'ordre des agents est choisi aléatoirement à chaque cycle.
    OA2( agents ) # OA2: L'ordre est du plus faible taux de sucre d'agent au plus gros
    
    ########################################################
    
    for agent in agents: # Parcours tous les agents de la population
        agent_rule( pop, env, agent ) # Appel la fonction de l'agent
        a.eat_all( agent, env) # Mange tout
        a.remove_metabolism_on_sugar_level( agent, pop ) # On retire le métabolism dans la réserve


def OA1( agents ):
    """
        OA1: l'ordre des agents est choisi aléatoirement à chaque cycle.
    """
    random.shuffle(agents) # Mélange la liste
    
    
def OA2( agents ):
    """
        OA2: L'ordre est du plus faible taux de sucre d'agent au plus gros
    """
    u.sort_list( agents, order_agent_by_sugar_level )
    
    
def order_agent_by_sugar_level( agent1, agent2 ):
    """
        Renvoie vrai si le taux de sucre de l'agent1 est plus grand que celui de l'agent2.
    """
    return a.get_sugar_level( agent1 ) > a.get_sugar_level( agent2 )
