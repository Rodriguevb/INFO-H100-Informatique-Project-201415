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
import mas_cell as c
import mas_environment as e
import mas_population as p
import mas_utils as u

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
METABOLISM_MAX = 0.2
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


def get_is_living( agent ):
    return __get_property( agent, IS_LIVING_IDX )


def set_is_living( agent, is_living ):
    __set_property( agent, IS_LIVING_IDX, is_living )



# --- Initialisation ---

def empty_agent ():
    """
        création d 'un agent avec des valeurs de bases
    """
    agent = __empty_instance()
    set_metabolism ( agent , 0.0 )
    set_vision ( agent , 2 )
    set_sugar_level ( agent , 0.0 )
    set_pos ( agent , e.default_cell_ref() )
    set_is_living( agent, True )
    return agent


def new_random ()  :
    agent = empty_agent()
    set_metabolism ( agent , random.uniform(METABOLISM_MIN,METABOLISM_MAX) )
    set_vision ( agent , random.randint(VISION_MIN,VISION_MAX) )
    return agent



    
# --- Others ---

def kill(pop, env, agent):
    cell_ref = get_pos(agent)
    cell = e.get_cell(env, cell_ref)
    c.set_present_agent(cell, None) # Dis qu'il n'y a plus d'agent présent dans la cellule
    p.remove_agent(pop, agent) # On retire l'agent de la liste de la population


def move_to(env, agent, target_cell_ref):
    cell_ref = get_pos(agent)
    cell_old = e.get_cell(env, cell_ref) # Ancienne cellule où l'agent se trouvait
    cell_new = e.get_cell(env, target_cell_ref) # Nouvelle cellule où l'agent se trouve
    
    sz = e.size(env)
    (x, y) = target_cell_ref
    target_cell_ref = ( x%sz, y%sz ) # Permet de passer de gauche à droite et de haut en bas dans la matrice environnement
    
    set_pos(agent, target_cell_ref ) # Indique à l'agent la nouvelle position.
    c.set_present_agent(cell_old, None) # Indique à l'ancienne cellule qu'il n'y a plus d'agent présent.
    c.set_present_agent(cell_new, agent) # Indique à la nouvelle cellule quel agent est présent.
    
   
def eat_all(agent, env):
    cell_ref = get_pos(agent)
    cell = e.get_cell(env, cell_ref )
    sugar = c.get_sugar_level( cell ) # On enregistre le taux de sucre de la cellule
    sugar += get_sugar_level ( agent ) # On ajoute la réserve de l'agent
    c.set_sugar_level( cell , 0 ) # On vide la cellule
    set_sugar_level ( agent , sugar ) # On donne tout à l'agent


def remove_metabolism_on_sugar_level(agent, pop):
    sugar = get_sugar_level( agent ) # Enregistre le taux de sucre de l'agent
    sugar -= get_metabolism( agent ) # On dimine par le metabolism
    set_sugar_level( agent, sugar ) # On donne le nouveau niveau de sucre de l'agent

    if get_sugar_level(agent) < 0:
        env = p.get_env(pop)
        kill(pop, env, agent)


        
        
        
        

# --- Rules ---

def RA1( pop, env, agent ):
    """
        Règle 1: Se dirige vers la cellule avec le plus de sucre.
    """
    agent_ref = get_pos(agent) # Position agent
    cells_refs = get_cells_refs( env, agent )
    
    if len(cells_refs) > 0:                          
        target = e.max_sugar_level_cell_ref( env, cells_refs )  # trouve la cellule (dans la liste) avec le plus grand taux de sucre
        move_to(env, agent, target)


def RA2( pop, env, agent ):
    """
        Règle 2: Se dirige vers la cellule avec le plus de sucre mais de 1 case par 1 case.
    """
    agent_ref = get_pos(agent)
    cells_refs = get_cells_refs( env, agent )
    
    if len(cells_refs) > 0:
        sort_cells_refs_decrease( env, cells_refs )
        
        for target in cells_refs:
            if RA2_is_possible( env, agent, target ):
                result =  u.vector_diff( target, agent_ref )
                target_unit = vector_one_max( result )
                cell_ref = u.vector_sum( agent_ref, target_unit ) # Récupère la position de la cellule à coté de l'agent
                move_to(env, agent, cell_ref) # Bouge l'agent
                return


def RA2_is_possible( env, agent, target ):
    agent_ref = get_pos( agent )
    result =  u.vector_diff( target, agent_ref )
    target_unit = vector_one_max( result )
    cell_ref = u.vector_sum( agent_ref, target_unit )
    cell = e.get_cell( env, cell_ref )
    return ( not c.agent_is_present(cell) ) and get_metabolism(agent) <= get_sugar_level(agent) + c.get_sugar_level(cell)
    

def RA3( pop, env, agent ):
    """
        Règle 3: L'agent choisit la cellule qui a le taux de sucre au minimum de ses besoins
    """
    agent_ref = get_pos( agent )
    cells_refs = get_cells_refs( env, agent )
    
    if len(cells_refs) > 0:
        target = min_sugar_level_need( env, agent, cells_refs )
        move_to(env, agent, target)


def RA4( pop, env, agent ):
    """
        Règle 4: Va vers le taux de sucre le plus élevé mais vérifie avant si un agent n'en a pas besoin plus que lui.
    """
    agent_ref = get_pos(agent)
    cells_refs = get_cells_refs( env, agent )
    
    if len(cells_refs) > 0:
        sort_cells_refs_decrease( env, cells_refs )
        
        for target in cells_refs:
            # Va vers la cible si il est dans le besoin ou qu'un autre agent n'en a pas besoin
            if get_metabolism(agent) > get_sugar_level(agent) or not e.friend_need( env, agent, target ):
                move_to(env, agent, target)
                return



# --- Movement ---

def get_cells_refs ( env, agent ):
    """
        Renvoie une liste des mouvements possibles aux alentours de l'agent.
    """
    agent_ref = get_pos(agent) # Position agent
    vision = get_vision ( agent ) # Vision agent
    vectors = [] # Liste de vecteurs
    for move in range(-vision, vision+1):
        if move != 0:
            vectors.append( [move,0] )
            vectors.append( [0,move] )
        
    cells_refs = []
    for vec in vectors:
        cell_ref = u.vector_sum( agent_ref, vec )  # On somme la position de l'agent
        cell = e.get_cell( env, cell_ref ) # La cellule
        if not c.agent_is_present( cell ):
            cells_refs.append( vec )
    
    cells_refs = list( u.vector_list_sum( cells_refs, agent_ref ) )
    cells_refs.append( agent_ref ) # Car la cellule peut rester sur place
    return cells_refs


# --- Others ---
    
def min_sugar_level_need( env, agent, cells_refs ):
    """
        Renvoie la cell_ref minimum que l'agent a besoin parmi la liste des cells_refs
    """
    # On crée une liste des cellules graces à la liste des positions.
    cells = []
    for cell_ref in cells_refs:
        cells.append( e.get_cell( env, cell_ref ) )
    
    # On a deux listes: les cellules et les positions.
    # On ordonne la liste des cellules en fonction du taux de sucre (Et les positions s'ordonneront en fonction aussi)
    u.sort_on_second_list(cells_refs, cells, order_decrease_cell_by_sugar_level)
    
    # On recherche le minimum
    minimal_cell_ref = cells_refs[0]
    minimal_cell = cells[0]
    
    #On parcout tous les éléments
    for temp in range( len(cells) ):
        temp_ref  = cells_refs[temp] #Position
        temp_cell = cells[temp] #Cellule
        
        #Si le taux suffit à la survie et que celui-ci est plus petit que le supposé "minimal".
        if c.get_sugar_level( temp_cell ) >= get_metabolism( agent ) and c.get_sugar_level( minimal_cell ) > c.get_sugar_level( temp_cell ):
            minimal_cell_ref = temp_ref # Nouvelle position minimale
            minimal_cell = temp_cell # Nouvelle cellule minimale
            
    return minimal_cell_ref # Renvoie la position de la cellule


def is_in_vision(agent, env, target):
    """
        Renvoie si la cible est bien dans la vision de l'agent.
    """
    return target in get_cells_refs(env, agent)

# --- Order ---

def sort_cells_refs_decrease( env, cells_refs ):
    """
        Trie la liste des positions.
    """
    # On crée une liste des cellules graces à la liste des positions.
    cells = []
    for cell_ref in cells_refs:
        cells.append( e.get_cell( env, cell_ref ) )
    
    # On a deux listes: les cellules et les positions.
    # On ordonne la liste des cellules en fonction du taux de sucre (Et les positions s'ordonneront en fonction aussi)        
    u.sort_on_second_list(cells_refs, cells, order_decrease_cell_by_sugar_level)


def order_decrease_cell_by_sugar_level( cell1, cell2 ):
    """
        Renvoie vrai si le taux de sucre de la cell1 est plus petit que celui de la cell2.
    """
    return c.get_sugar_level( cell1 ) < c.get_sugar_level( cell2 )


    
# --- Vectors ---

def vector_one_max( vec ):
    """
        On forme un vecteur dont les valeurs sont réduit dans l'intervalle -1 à 1
    """
    vec_unit = [ vec[0], vec[1] ]
    if vec_unit[0] > 0:
        vec_unit[0] = 1
    elif vec_unit[0] < 0:
        vec_unit[0] = -1
    if vec_unit[1] > 0:
        vec_unit[1] = 1
    elif vec_unit[1] < 0:
        vec_unit[1] = -1
    return vec_unit

