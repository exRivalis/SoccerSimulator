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

class MyState(object):
	
	def __init__(self,state,idteam,idplayer) :
		self.state = state
		self.key = (idteam, idplayer)
		
		self.my_position = self.state.player_state(self.key[0], self.key[1]).position
		self.ball_position = self.state.ball.position
		self.but_adv = Vector2D(150, 45) if self.key[0] == 1 else Vector2D(0, 45)	
		#recup joueur 
		self.all_players = self.state.players
		self.co_players = [ p  for p in self.all_players if p[0] == self.key[0]]
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
	
	def aller(self, p) :
		return SoccerAction(p-self.my_position, Vector2D())
	
	def shoot(self, p) :
		return SoccerAction(Vector2D(), p-self.my_position)
		
	#recup adv le plus proche
	def adv_nearby(self):
		players = self.adv_players
		if len(players) == 0:
			return None
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return self.state.player_state(pp[0], pp[1])
				

		
