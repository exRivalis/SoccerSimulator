#les objets de base
from soccersimulator import Vector2D, SoccerState, SoccerAction

#objets pour un match
from soccersimulator import Simulation, SoccerTeam, Player, show_simu, SoccerTournament

#importer la strategie de base
from soccersimulator import Strategy

#toutes les constantes
from soccersimulator import settings

#module math
import math

#toolbox
from tools import MyState

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus, SoloStrat, Solo, Strat,SoloTac

#from tactic import *

#simulation

joueur1 = Player("player1", Strat())
joueur2 = Player("player2", Strat())

joueur3 = Player("player3", Strat())
joueur4 = Player("player4", Strat())


#team1 = SoccerTeam("Eq1", [joueur1, joueur2])
#team2 = SoccerTeam("Eq2", [joueur3, joueur4])


#soloStrategy
solo1 = Player("Houta", SoloTac())
solo2 = Player("Hmar", SoloStrat())

STeam1 = SoccerTeam("strat", [solo1])
STeam2 = SoccerTeam("Eq2", [solo2])

#match = Simulation(team1,team2, 2000)
#match = Simulation(team3, team4, 2000)
#print team1.players

#show_simu(match)
TTeam1 = SoccerTeam("Strart", [joueur1, joueur2])
TTeam2 = SoccerTeam("base", [joueur3, joueur4])

#match = Simulation(STeam1, STeam2, 2000) #solo match
match = Simulation(TTeam1, TTeam2, 2000) #Two match

show_simu(match)
