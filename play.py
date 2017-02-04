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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus



#simulation

joueur1 = Player("player1", Attaquant())
joueur2 = Player("player2", Attaquant())

joueur3 = Player("player3", Attaquant())
joueur4 = Player("player4", Attaquant())


team1 = SoccerTeam("Eq1", [joueur1, joueur2])
team2 = SoccerTeam("Eq2", [joueur3, joueur4])

match = Simulation(team1,team2, 2000)

#print team1.players

show_simu(match)

