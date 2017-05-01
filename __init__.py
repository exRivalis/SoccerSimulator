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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, SoloStrat, Solo, Gardien, GardienB, Defense1, Atta2

jean = Player("Drexor", Attaquant())
sydney = Player("Keeper", GardienB())

solo = Player("miche-miche", Solo())

maestro = Player("Maestro", Atta2())
leonardo = Player("Leo", Defenseur())

ahmed = Player("chef", Defense1())


team1 = SoccerTeam("Curly", [solo])



team2 = SoccerTeam("Two", [jean, sydney])

team4 = SoccerTeam("GangOfFour",[jean, sydney, maestro, ahmed])


def get_team(i):
	if i == 1:
		return team1
	elif i == 4:
		return team4
	return team2
