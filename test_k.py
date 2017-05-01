from strategy import RandomStrategy, Attaquant, AttaquantPlus, Defenseur, DefenseurPlus, SoloStrat, Solo, Gardien, Shooter, StratARien
#les objets de base
from soccersimulator import Vector2D, SoccerState, SoccerAction

#objets pour un match
from soccersimulator import Simulation, SoccerTeam, Player, show_simu, SoccerTournament, SoccerState, PlayerState, Ball

#importer la strategie de base
from soccersimulator import Strategy

#toutes les constantes
from soccersimulator import settings

#toutes les tactiques
from tactic import TTactic, FTactic, STactic
#module math
import math
from observer import Observer
from tools import MyState
import logging
logging.basicConfig(level = logging.DEBUG)
#for k in range(0, 50):# k allant de 0 a 50 par pas de 1
#	for i in range(0, 1000): #pour 1000 tirs
		#								(idteam, idplayer) : player, ball = Ball(pos, vit)
"""
posB = Vector2D(20, 30)
posP = Vector2D(18, 28)
vB	= Vector2D(0, 0)
state = SoccerState(states = {(1, 0) : PlayerState(posP, Vector2D(0, 0)), (2, 0) : PlayerState(posP, Vector2D(0, 0))}, ball = Ball(posB, vB))
"""

p1 = Player("Houta", Shooter())
p2 = Player("Hmar", StratARien())

p3 = Player("vvvv", Attaquant())
p4 = Player("wwww", Gardien())

team1 = SoccerTeam("Bill", [p1])
team2 = SoccerTeam("Boule", [p2])

match = Simulation(team1, team2, 500)

Observer(match)
show_simu(match)
		
		 
