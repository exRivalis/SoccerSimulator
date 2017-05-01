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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, Atta2, SoloStrat, Solo, Gardien, Defense1, Attaqtaq, Defense, GardienB, Shooter



#simulation

j1 = Player("player1", Attaquant())
j2 = Player("player2", Attaquant())

j3 = Player("player3", Defenseur())
j4 = Player("player4", GardienB())

j5 = Player("def1", Defense1())
j6 = Player("gard", GardienB())
j7 = Player("attaqtaq", Attaquant())
j8 = Player("attaq", Atta2())

team1 = SoccerTeam("Eq1", [j1, j2])
team2 = SoccerTeam("Eq2", [j3, j4])

#soloStrategy
solo1 = Player("Houta", Solo())
solo2 = Player("Hmar", Shooter())

team41 = SoccerTeam("Eq1", [j1, j2, j3, j4])
team42 = SoccerTeam("Eq2", [j5, j6, j7, j8])
team_s1 = SoccerTeam("winner", [solo1])
team_s2 = SoccerTeam("looser", [solo2])
#match = Simulation(team1,team2, 2000)
match = Simulation(team_s1, team_s2, 2000)
#print team1.players

show_simu(match)
#team1 = SoccerTeam("Eq1", [solo1])
#team2 = SoccerTeam("Eq2", [joueur3, joueur4])

