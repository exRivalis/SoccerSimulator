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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus, SoloStrat, Solo, Gardien, Defense1, Attaqtaq, Defense



#simulation

j1 = Player("player1", Attaquant())
j2 = Player("player2", Attaquant())

j3 = Player("player3", Defenseur())
j4 = Player("player4", Gardien())

j5 = Player("def1", Defense1())
j6 = Player("gard", Gardien())
j7 = Player("attaqtaq", Attaqtaq())
j8 = Player("attaq", Attaqtaq())

team1 = SoccerTeam("Eq1", [j1, j2])
team2 = SoccerTeam("Eq2", [j3, j4])

#soloStrategy
solo1 = Player("Houta", Solo())
solo2 = Player("Hmar", SoloStrat())

team41 = SoccerTeam("Eq1", [j1, j2, j3, j4])
team42 = SoccerTeam("Eq2", [j5, j6, j7, j8])

match = Simulation(team41,team42, 2000)
#match = Simulation(team3, team4, 2000)
#print team1.players

show_simu(match)
#team1 = SoccerTeam("Eq1", [solo1])
#team2 = SoccerTeam("Eq2", [joueur3, joueur4])

