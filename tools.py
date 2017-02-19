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
		#all co_players except me
		self.co_players = [self.state.player_state(p[0], p[1]).position for p in self.all_players if (p[0] == self.key[0] and p[1] != self.key[1])]
		self.adv_players = [self.state.player_state(p[0], p[1]).position for p in self.all_players if p[0] != self.key[0]]
		#can the player shoot in the ball
		self.can_shoot = True if self.my_position.distance(self.ball_position) < 0.82 else False
		
		#sens de la marche
		self.sens = 1 if idteam == 1 else -1
		#side of adv
		self.adv_on_right = 1 if self.adv_players[0].y > self.my_position.x else -1
		
		
		#suis-je proche de la balle
		self.near_ball = True if self.my_position.distance(self.ball_position) < 7 else False
	
	#return vect vitesse ball
	@property
	def v_ball(self):
		return self.state.ball.vitesse
	
	#vect vitesse coeq
	@property
	def v_coeq(self):
		return self.state.player_state(self.key[0], (self.key[1] + 1)%2).vitesse
	#return ma distance de la balle
	@property
	def dist_ball(self):
		return self.my_position.distance(self.ball_position)
	
	
	def aller(self, p) :
		"""coefficient pour ralentir pres de la balle"""
		coef = 0.005	
		v = Vector2D(0, 0) if self.ball_position.distance(self.my_position) < 6 else self.v_ball
		#si je suis proche de la balle ralentir
		if self.dist_ball < 5 :
			return SoccerAction((p-self.my_position)/10)
		return SoccerAction(p-self.my_position)# + coef*p.distance(self.my_position) + v*4)

		
	
	def shoot(self, p) :
		if p.distance(self.my_position) < 10:
			return SoccerAction(Vector2D(), p-self.my_position)
		return SoccerAction(Vector2D(), (p-self.my_position)/20)
	
	#pour determiner le facteur k
	def tirer(self, p, k):
		return SoccerAction(Vector2D(), k*(p - self.my_position))
		
	#passer la balle a un coeq
	def passe(self, p) :
		if p.distance(self.but_adv) < 50:#si je suis proche des buts faire des passe douces
			if p.distance(self.but_adv) > 20:
				if self.my_position.y < 55 and self.my_position.y > 35 and p.distance(self.but_adv) < 1:# si je vide but_adv
					return SoccerAction(Vector2D(), (self.sens*Vector2D(10, 0)))# si je suis face au but je tir fort
			
				if self.my_position.distance(p) < 30: #mon coeq est proche
					return SoccerAction(Vector2D(), (p - self.my_position + Vector2D(self.sens*7, 0))/10)#sinon doucement
				
			return SoccerAction(Vector2D(), (p - self.my_position))
		# math.fabs
		#dx = (self.my_position.x - p.x)
		#dy = (self.my_position.y - p.y)
			return SoccerAction(Vector2D(), (p - self.my_position))
		if self.my_position.distance(p) < 30:
				return SoccerAction(Vector2D(), (p - self.my_position)/15)#sinon doucement
		return SoccerAction(Vector2D(), (p - self.my_position))
	
	@property
	def aller_ball(self) :
		#print self.state.ball.vitesse
		return self.aller(self.ball_position)
	
	#la balle dans mon camp?
	@property
	def ball_in_my_side(self):
		if self.sens == 1 and self.ball_position.x < 75:
			return True
		elif self.sens == -1 and self.ball_position.x > 75:
			return True
		return False 
	
	#aller but adv et marquer quand possible
	@property
	def aller_but_adv(self):
		if self.my_position.distance(self.but_adv) < 20:
			if self.can_shoot:
				return self.shoot(self.but_adv)
			return self.aller(self.but_adv )#- self.sens*Vector2D(8, ))
		else :
			if self.can_shoot:
				return self.passe((self.but_adv - self.my_position)/10)	
			return self.aller(self.but_adv)
			
	#recup adv le plus proche
	@property
	def adv_nearby(self):
		players = self.adv_players
		"""if len(players) == 1:
			return None"""
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(players[0]) < self.my_position.distance(players[1]):
				pp = p
		return pp
	
		#recup adv le plus proche
	@property
	def coeq_nearby(self):
		players = self.co_players
		"""if len(players) == 1:
			return """
		pp = players[0]
		for p in players:
			#print self.my_position.distance(self.state.player_state(p[0], p[1]).position)
			#print self.my_position.distance(self.state.player_state(pp[0], pp[1]).position)
			if self.my_position.distance(p) < self.my_position.distance(pp):
				pp = p
		return pp

	#true if player p near ball
	def p_near_ball(self, p):
		return True if self.ball_position.distance(p) < 10 else False
	
	#any coeq near ball
	@property
	def co_near_ball(self):
		for p in self.co_players:
			if p.distance(self.my_position) < 7:
				return True
		return False
		
	
	@property
	def me_near_ball(self):
		return True if self.my_position.distance(self.ball_position) < 4 else False
	
	#je suis a cote de mon coeq
	@property
	def me_near_co(self):
		return True if self.my_position.distance(self.coeq_nearby) < 5 else False
	"""def drible(self) :
		adv = self.adv_nearby()
		sens = 1
		if adv[0] == 2 :
			sens = 1
		else:
			sens = -1
		print self.state.player_state(self.key[0], self.key[1])._rd_angle(Vector2D(1, 1), 90, 1)
		if self.my_position.y < adv.y :#passe gauche
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
					print angle
					return self.shoot(self.but_adv)
				else:
						return self.aller(self.ball_position)
			"""		

