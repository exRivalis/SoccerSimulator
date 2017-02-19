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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, SoloStrat, Solo

joueur1 = Player("player1", Attaquant())
joueur2 = Player("player2", Attaquant())

<<<<<<< HEAD
joueur3 = Player("player3", Solo()
joueur4 = Player("player4", AttaquantPlus())

=======
joueur3 = Player("player3", Solo())
joueur4 = Player("player4", AttaquantPlus())


>>>>>>> 59b6a135c704a4ee33bc6701ca13491271e18c7b
joueur5 = Player("mnms", Attaquant())

team1 = SoccerTeam("Eq1", [joueur3])



team2 = SoccerTeam("Eq2", [joueur1, joueur2])

<<<<<<< HEAD
team4 = SoccerTeam("les 4 fantastiques", [joueur1, joueur2, joueur4, jouer5])
=======
team4 = SoccerTeam("les 4 fantastiques", [joueur1, joueur2, joueur4, joueur5])
>>>>>>> 59b6a135c704a4ee33bc6701ca13491271e18c7b
#gang of four

def get_team(i):
	if i == 1:
		return team1
	elif i == 4:
		return team4
	return team2
