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
		self.but = Vector2D(0, 45) if self.key[0] == 1 else Vector2D(150, 45)
		#recup joueur 
		self.all_players = self.state.players
		self.co_players = [p  for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
		self.adv_players = [p  for p in self.all_players if p[0] != self.key[0]]
		
		#can the player shoot in the ball
		self.can_shoot = True if self.my_position.distance(self.ball_position) < 0.82 else False
		
		#side of adv
		self.adv_on_right = 1 if self.state.player_state(self.adv_players[0][0], self.adv_players[0][1]).position.y > self.my_position.y else -1
		
		
		#est proche de la balle
		self.near_ball = True if self.my_position.distance(self.ball_position) < 20 else False
		
		#liste des coeq proche
		self.coeq_proche = [p for p in self.co_players if self.my_position.distance(self.state.player_state(p[0], p[1]).position) < 75]
		
	@property
	def coeq_libre(self) :
		if len(self.coeq_proche) == 0 :
			return [0, 0]
		elif len(self.coeq_proche) == 1 :
			return self.coeq_proche[0]
		else :
			x = mstate.player_state(p[0], p[1]).position.distance(mstate.player_state(p[0], p[1]).adv_nearby())
			pp = coeq_proche[0]
			for p in coeq_proche[1:] :
				d = mstate.player_state(p[0], p[1]).position.distance(mstate.player_state(p[0], p[1]).adv_nearby())
				if x < d :
					x = d
					pp = p
			return pp
	@property
	def aller_ball(self) :
		
		if self.my_position.distance(self.ball_position) > 10:
			return SoccerAction(5*(self.state.ball.vitesse -(self.my_position - self.ball_position)), Vector2D())
		else :
			return SoccerAction((self.state.ball.vitesse -(self.my_position - self.ball_position)), Vector2D())
	
	
	
	def aller(self, p) :
		if (p == self.ball_position) :
			return self.aller_ball
		return SoccerAction(p-self.my_position , Vector2D())
	
	
	def shoot(self, p) :
		if self.can_shoot :
			return SoccerAction(Vector2D(), p-self.my_position)  
		else :
			return self.aller(self.ball_position)
	
	
	"""
	@property
	def attaque_droite(self):
		if self.state.player_state(self.coeq_nearby[0], self.coeq_nearby[1]).position.distance(self.my_position) > 20:
			self.aller(self.ball_position) + shoot(self.state.player_state(self.coeq_nearby[0], self.coeq_nearby[1]).position) + 
		"""
		
	#recup adv le plus proche
	#@property
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
	
	def pos_j(self, p):
		return self.state.player_state(p[0], p[1]).position
		
	
	
	
	def adv_nearbyj(self, idteam, idplayer) :
		if self.idteam == idteam :
			return adv_nearby()
		else :
			return coeq_nearby()
		
	
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
		#print self.state.player_state(self.key[0], self.key[1])._rd_angle(Vector2D(1, 1), 90, 1)
		if self.my_position.y < self.state.player_state(adv[0], adv[1]).position.y :#passe gauche
				if self.can_shoot:
					return self.shoot(self.ball_position + sens*Vector2D(5, -5))
				else:
					return self.aller(self.ball_position)
		else:
				if self.can_shoot:
					p_pos = self.my_position
					angle = self.state.player_state(self.key[0], self.key[1]).acceleration
					#v_but = self.state.player_state(self.key[0], self.key[1])._rd_angle(p_pos, angle, 1)
					#a = self.state.player_state(self.key[0], self.key[1]).acceleration
					#print angle
					return self.shoot(self.but_adv)
				else:
						return self.aller(self.ball_position)
					

















