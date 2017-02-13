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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus, SoloStrat, Solo, Strat

#from tactic import *

#simulation

joueur1 = Player("player1", Strat())
joueur2 = Player("player2", Strat())

joueur3 = Player("player3", Strat())
joueur4 = Player("player4", Strat())


#team1 = SoccerTeam("Eq1", [joueur1, joueur2])
#team2 = SoccerTeam("Eq2", [joueur3, joueur4])


#soloStrategy
solo1 = Player("Houta", Solo())
solo2 = Player("Hmar", SoloStrat())

#team3 = SoccerTeam("Eq1", [solo1])
#team4 = SoccerTeam("Eq2", [solo2])

#match = Simulation(team1,team2, 2000)
#match = Simulation(team3, team4, 2000)
#print team1.players

#show_simu(match)
team1 = SoccerTeam("Eq1", [joueur1, joueur2])
team2 = SoccerTeam("Eq2", [joueur3, joueur4])

match = Simulation(team1,team2, 2000)
show_simu(match)
