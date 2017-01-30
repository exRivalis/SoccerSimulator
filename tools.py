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
		self.co_players = [p  for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
		#can the player shoot in the ball
		self.can_shoot = True if self.my_position.distance(self.ball_position) < 0.82 else False
		
		#est proche de la balle
		self.near_ball = True if self.my_position.distance(self.ball_position) < 20 else False
	
	def aller(self, p) :
		return SoccerAction(p-self.my_position , Vector2D())
	
	def shoot(self, p) :
		return SoccerAction(Vector2D(), p-self.my_position)
	

		
	#recup adv le plus proche
	def adv_nearby(self):
		players = self.adv_players
		"""if len(players) == 1:
			return None"""
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return pp
	
		#recup adv le plus proche
	def coeq_nearby(self):
		players = self.co_players
		"""if len(players) == 1:
			return """
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < self.my_position.distance(self.state.player_state(pp[0], pp[1]).position):
				pp = p
		return pp
	
	#true if player p near ball
	def p_near_ball(self, p):
		return True if self.ball_position.distance(self.state.player_state(p[0], p[1]).position) < 20 else False
				
	def drible(self) :
		adv = self.adv_nearby()
		sens = 1
		if adv[0] == 2 :
			sens = 1
		else:
			sens = -1
		
		if self.my_position.y < self.state.player_state(adv[0], adv[1]).position.y :#passe gauche
				if mstate.can_shoot:
					mstate.shoot(ball_position + sens*Vector2D(5, -5))
				else:
					mstate.aller(ball_position)
		else:
				if mstate.can_shoot:
						mstate.shoot(ball_position + sens*Vector2D(5, 5))
				else:
						mstate.aller(ball_position)
					

