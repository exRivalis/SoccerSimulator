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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus, SoloStrat, Solo, Gardien, Defense1



#simulation

joueur1 = Player("player1", Attaquant())
joueur2 = Player("player2", Attaquant())

joueur3 = Player("player3", Defenseur())
joueur4 = Player("player4", Gardien())

j5 = Player("def1", Defense1())
j6 = Player("def1_2", Defense1())
j4 = Player("", )
j4 = Player("j4", )

team1 = SoccerTeam("Eq1", [joueur1, joueur2])
team2 = SoccerTeam("Eq2", [joueur3, joueur4])


#soloStrategy
solo1 = Player("Houta", Solo())
solo2 = Player("Hmar", SoloStrat())

team3 = SoccerTeam("Eq1", [solo2])
team4 = SoccerTeam("Eq2", [solo1])

match = Simulation(team1,team2, 2000)
#match = Simulation(team3, team4, 2000)
#print team1.players

show_simu(match)
#team1 = SoccerTeam("Eq1", [solo1])
#team2 = SoccerTeam("Eq2", [joueur3, joueur4])

