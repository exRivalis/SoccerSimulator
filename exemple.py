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
from tools import MyState, Attaquant, Defenseur, AttaquantPlus

v=Vector2D(2.1,-1.4)

w= Vector2D(angle=50, norm=1)

#print v
#print w







##creeer action
vitesse = Vector2D(1, 1)
shoot = Vector2D(1, 1)
act1 = SoccerAction(vitesse, shoot)
act2 = SoccerAction(2*vitesse, 2*shoot)
#print act1.acceleration, act1.shoot



#simulation

joueur1 = Player("player1", Attaquant())
joueur2 = Player("player2", Defenseur())

joueur3 = Player("player3", Attaquant())
joueur4 = Player("player4", AttaquantPlus())

joueur5 = Player("player5", Attaquant())
joueur6 = Player("player6", Attaquant())

team1 = SoccerTeam("Eq1", [joueur1, joueur2])



team2 = SoccerTeam("Eq2", [joueur3, joueur4])

team3 = SoccerTeam("Eq3", [joueur1, joueur6, joueur5])

match = Simulation(team1,team2, 2000)

#print team1.players

show_simu(match)

