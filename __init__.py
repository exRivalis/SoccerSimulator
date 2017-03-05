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

joueur1 = Player("player1", Attaquant())
joueur2 = Player("player2", Gardien())

joueur3 = Player("player3", Solo())
joueur4 = Player("player4", AttaquantPlus())

team1 = SoccerTeam("Eq1", [joueur3])



team2 = SoccerTeam("Eq2", [joueur1, joueur2])
