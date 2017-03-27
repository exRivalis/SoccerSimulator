from soccersimulator import settings,SoccerTeam, Simulation, show_simu, KeyboardStrategy
from soccersimulator import Strategy, SoccerAction, Vector2D, load_jsonz,dump_jsonz,Vector2D
import logging
from arbres_utils import build_apprentissage,affiche_arbre,DTreeStrategy,apprend_arbre,genere_dot
from sklearn.tree 	import export_graphviz
from sklearn.tree import DecisionTreeClassifier

#toolbox
from tools import MyState

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus, SoloStrat, Solo, Gardien, Shooter, Defense, GardienB, Passeur

from tools import MyState


import os.path
## Strategie aleatoire
class FonceStrategy(Strategy):
    def __init__(self):
        super(FonceStrategy,self).__init__("Fonce2")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction(state.ball.position-state.player_state(id_team,id_player).position,\
                Vector2D((2-id_team)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.)-state.ball.position)

class StaticStrategy(Strategy):
    def __init__(self):
        super(StaticStrategy,self).__init__("Static")
    def compute_strategy(self,state,id_team,id_player):
        return SoccerAction()

#######
## Constructioon des equipes
#######

team1 = SoccerTeam("team1")
strat_j1 = KeyboardStrategy()
strat_j1.add('p',Passeur())
strat_j1.add('z',StaticStrategy())
strat_j1.add('g', GardienB())
strat_j1.add('s', Shooter())

team1.add("Jexp 1",strat_j1)
team1.add("Jexp 2",StaticStrategy())
team2 = SoccerTeam("team2")
strat_j2 = KeyboardStrategy()
strat_j2.add('e',Attaquant())
strat_j2.add('r',StaticStrategy())
strat_j2.add('h', Gardien())
strat_j2.add('d', Defense())
team2.add("rien 1", strat_j2)
team2.add("rien 2", StaticStrategy())


### Transformation d'un etat en features : state,idt,idp -> R^d
def my_get_features(state,idt,idp):
    """ extraction du vecteur de features d'un etat, ici distance a la balle, distance au but, distance balle but """
    mstate = MyState(state,idt,idp)
    p_pos = mstate.my_position
    f1 = p_pos.distance(state.ball.position + mstate.v_ball*10) #ma distance de la balle
    f2 = p_pos.distance( Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))#dist but
    adv = mstate.adv_nearby()
    adv_pos = state.player_state(adv[0], adv[1]).position
    adv_ball = adv_pos.distance(mstate.ball_position + mstate.v_ball*10)
    f3 = state.ball.position.distance(Vector2D((2-idt)*settings.GAME_WIDTH,settings.GAME_HEIGHT/2.))#dist but ball
    ballmine = f1<adv_ball
    camp_attaque = (mstate.sens == 1 and mstate.ball_position.x > 75) or (mstate.sens == -1 and mstate.ball_position.x < 75)
    adv = mstate.adv_pball()
    co = mstate.co_pball()
    our_ball = state.player_state(co[0], co[1]).position.distance(mstate.ball_position) < state.player_state(adv[0], adv[1]).position.distance(mstate.ball_position)
    
    #on aura besoin si la balle est dans mon camp, alor si je suis le plus proche alor si j'y suis deja je fait un truck 
    return [camp_attaque, our_ball, ballmine]


def entrainement(fn):
    simu = Simulation(team1,team2,3000)
    show_simu(simu)
    # recuperation de tous les etats
    training_states = strat_j1.states
    # sauvegarde dans un fichier
    dump_jsonz(training_states,fn)

def apprentissage(fn):
    ### chargement d'un fichier sauvegarder
    states_tuple = load_jsonz(fn)
    ## Apprentissage de l'arbre
    data_train, data_labels = build_apprentissage(states_tuple,my_get_features)
    dt = apprend_arbre(data_train,data_labels,depth=10)
    # Visualisation de l'arbre
    affiche_arbre(dt)
    genere_dot(dt,"test_arbre.dot")
    return dt

def jouer_arbre(dt):
    ####
    # Utilisation de l'arbre
    ###
    dic = {"Attaquant":Attaquant(),"Static":StaticStrategy(), "Gardien":Gardien()}
    treeStrat1 = DTreeStrategy(dt,dic,my_get_features)
    treeStrat2 = DTreeStrategy(dt,dic,my_get_features)
    team3 = SoccerTeam("Arbre Team")
    team3.add("Joueur 1",treeStrat1)
    team3.add("Joueur 2",treeStrat2)
    simu = Simulation(team2,team1,300)
    show_simu(simu)

if __name__=="__main__":
    fn = "test_states.jz"
    #if not os.path.isfile(fn):
    #for i in range(0, 10):
    entrainement(fn)
    dt = apprentissage(fn)
    jouer_arbre(dt)
    
   
#cpickle.load/dump pour lecture/ecriture dans un fichier, fin je crois hein!
