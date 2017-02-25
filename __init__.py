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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, SoloStrat, Solo, SoloTac, Strat

joueur1 = Player("One", Strat())
joueur2 = Player("Two", Strat())

solo1 = Player("Three", SoloTac())
solo2 = Player("player4", AttaquantPlus())

joueur5 = Player("mnms", Attaquant())

team1 = SoccerTeam("DTeam", [solo1])

team2 = SoccerTeam("None", [joueur1, joueur2])

team4 = SoccerTeam("les 4 fantastiques", [joueur1, joueur2, joueur4, jouer5])
#gang of four

def get_team(i):
	if i == 1:
		return team1
	elif i == 4:
		return team4
	return team2
