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

from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur

joueur1 = Player("player1", Attaquant())
joueur2 = Player("player2", Defenseur())

joueur3 = Player("player3", Attaquant())
joueur4 = Player("player4", AttaquantPlus())

team1 = SoccerTeam("Eq1", [joueur1])



team2 = SoccerTeam("Eq2", [joueur3, joueur4])
