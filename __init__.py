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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, SoloStrat, Solo, Gardien

jean = Player("Drexor", Attaquant())
sydney = Player("Keeper", Gardien())

solo = Player("miche-miche", Solo())

maestro = Player("Maestro", AttaquantPlus())
leanardo = Player("Leo", Defenseur())



team1 = SoccerTeam("Curly", [solo])



team2 = SoccerTeam("Two", [jean, sydney])

team4 = SoccerTeam("GangOfFour",[jean, sydney, maestro, leonardo])


def get_team(i):
	if i == 1:
		return team1
	elif i == 4:
		return team4
	return team2
